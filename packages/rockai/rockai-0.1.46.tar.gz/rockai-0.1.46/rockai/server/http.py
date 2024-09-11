from fastapi import FastAPI, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import signal
from rockai.predictor import BasePredictor
import uvicorn
from rockai.parser.config_util import (
    parse_config_file,
    get_predictor_class_name,
    get_predictor_path,
)
from rockai.server.utils import (
    load_class_from_file,
    get_input_type,
    get_output_type,
)
from starlette.responses import StreamingResponse
import rockai.data_class
import typing
import logging
from rockai.data_class import PredictionResponse
from pathlib import Path
from fastapi import Path as FastApiPath
from typing import Any
from rockai.server.runner import Runner, RunnerResult
import uuid
from .json import upload_files
from .files import upload_file
from datetime import datetime
from enum import Enum, auto, unique
from rockai.server.auth import AuthHandler
from rockai.server.utils import load_predictor_class

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Set the initial logging level to INFO

# Create a logger
logger = logging.getLogger(__name__)


@unique
class Health(Enum):
    UNKNOWN = auto()
    STARTING = auto()
    READY = auto()
    BUSY = auto()
    SETUP_FAILED = auto()


class PredictorState:
    health: Health


class MyFastAPI(FastAPI):
    predictor_state: PredictorState


def load_predictor_from_file(path) -> BasePredictor:
    pred: BasePredictor = load_class_from_file(
        Path.cwd() / get_predictor_path(parse_config_file(path / "rock.yaml")),
        get_predictor_class_name(parse_config_file(path / "rock.yaml")),
        BasePredictor,
    )
    return pred


def create_app(
    file_name: str,
    auth: str = None,
    upload_url: str = "https://api.rockai.online/v1/get_presign_url",
) -> MyFastAPI:

    app: MyFastAPI = MyFastAPI()
    app.predictor_state = PredictorState()
    app.predictor_state.health = Health.UNKNOWN
    pred: BasePredictor = load_predictor_class(file_name)

    input_type = get_input_type(pred)

    output_type = get_output_type(pred)

    runner = Runner()

    auth_handler = AuthHandler(auth_token=auth)
    if auth is not None:
        auth_handler.is_using_auth = True

    class PredictionRequest(
        rockai.data_class.PredictionRequest.get_pydantic_model(input_type=input_type)
    ):
        pass

    InfereceResult = PredictionResponse.get_pydantic_model(
        input_type=input_type, output_type=output_type
    )

    @app.on_event("startup")
    async def start_up_event():
        """
        Run the setup function of the predictor and load the model
        """
        logger.debug("setup start...")
        app.predictor_state.health = Health.STARTING
        try:
            pred.setup()
            app.predictor_state.health = Health.READY
            logger.debug("setup finished")
        except Exception as e:
            app.predictor_state.health = Health.SETUP_FAILED
            logger.error(f"Error setting up predictor: {str(e)}")

    @app.post(
        "/predictions",
        response_model=InfereceResult,
        response_model_exclude_unset=True,
    )
    def predict(
        request_body: PredictionRequest = Body(default=None),
        auth=Depends(auth_handler.auth_wrapper),
    ) -> typing.Any:
        """
        Running the prediction.
        """
        logger.debug("prediction called...")
        if request_body is None or request_body.input is None:
            request_body = PredictionRequest(input={})
        request_body = request_body.dict()
        id = uuid.uuid4().hex
        start_time = datetime.now()
        result = pred.predict(**request_body["input"])
        end_time = datetime.now()
        time_taken = (end_time - start_time).total_seconds()
        final_result = upload_files(
            result, upload_file=lambda fh: upload_file(fh, upload_url)  # type: ignore
        )
        return JSONResponse(
            content=jsonable_encoder(
                InfereceResult(
                    input=request_body["input"],
                    inference_time=time_taken,
                    output=final_result,
                    id=id,
                    started_at=start_time,
                    completed_at=end_time,
                )
            )
        )

    @app.post(
        "/predictions/{prediction_id}",
        response_model=InfereceResult,
        response_model_exclude_unset=True,
    )
    def predic_with_id(
        prediction_id: str = FastApiPath(title="prediction ID"),
        request_body: PredictionRequest = Body(default=None),
        auth=Depends(auth_handler.auth_wrapper),
    ) -> typing.Any:
        """
        Running the prediction.
        """
        logger.debug("prediction called... ID -> {}".format(prediction_id))
        if request_body is None or request_body.input is None:
            request_body = PredictionRequest(input={})
        request_body = request_body.dict()
        start_time = datetime.now()
        # result = await runner.get_result(pred,request_body)
        result = pred.predict(**request_body["input"])
        # result = await runner.predict(prediction_id, pred.predict, request_body)
        end_time = datetime.now()
        time_taken = (end_time - start_time).total_seconds()
        final_result = upload_files(
            result, upload_file=lambda fh: upload_file(fh, upload_url)
        )
        if isinstance(result, RunnerResult):
            return JSONResponse(
                content=jsonable_encoder({"msg": result.msg}), status_code=400
            )
        return JSONResponse(
            content=jsonable_encoder(
                InfereceResult(
                    input=request_body["input"],
                    inference_time=time_taken,
                    output=final_result,
                    id=prediction_id,
                    started_at=start_time,
                    completed_at=end_time,
                )
            ),
            status_code=200,
        )

    @app.post("/stream/predictions", response_model_exclude_unset=True)
    def stream_predict(
        request_body: PredictionRequest = Body(default=None),
        auth=Depends(auth_handler.auth_wrapper),
    ) -> typing.Any:
        """
        Running the prediction.
        """
        logger.debug("streamprediction called...")
        if request_body is None or request_body.input is None:
            request_body = PredictionRequest(input={})
        request_body = request_body.dict()

        def stream_fun():
            for data in pred.predict(**request_body["input"]):
                yield f"event: output\ndata: {data}\n\n"
            yield "event: done\ndata: {}\n\n".format({})

        return StreamingResponse(stream_fun(), media_type="text/event-stream")

    @app.post("/predictions/{prediction_id}/cancel")
    async def cancel(prediction_id: str) -> Any:
        result = runner.cancel(prediction_id)
        """Cancel prediction by id"""
        logger.debug("cancel prediction start...{}".format(prediction_id))
        return JSONResponse(
            content={
                "message": "Prediction {} is cancelled -> {}".format(
                    prediction_id, result
                ),
                "is_canceled": result,
                "prediction_id": prediction_id,
            },
            status_code=200,
        )

    @app.post("/shutdown")
    async def shutdown(auth=Depends(auth_handler.auth_wrapper)):
        """
        Shutdown the server.
        """
        runner.clean_up()
        pid = os.getpid()
        os.kill(pid, signal.SIGINT)
        return JSONResponse(content={"message": "Shutting down"}, status_code=200)

    @app.get("/")
    async def root():
        """
        Hello World!, when you see this message, it means the server is up and running.
        """
        return JSONResponse(
            content={"docs_url": "/docs", "model_schema": "/openapi.json"},
            status_code=200,
        )

    @app.get("/health-check")  # type: ignore[return-value]
    async def health_check() -> Any:
        return JSONResponse(content={"status": str(app.predictor_state.health.name)})

    # finally create the application
    return app


def start_server(
    file_name,
    port,
    auth=None,
    upload_url="https://api.rockai.online/v1/get_presign_url",
):
    app = create_app(file_name, auth=auth, upload_url=upload_url)
    uvicorn.run(app, host="0.0.0.0", port=port)
