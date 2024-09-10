import asyncio
from pebble import ThreadPool
import logging
from fastapi import HTTPException


class RunnerResult:
    def __init__(self, msg):
        self.msg = msg


class Runner:
    def __init__(self) -> None:
        self.futures = {}

    async def predict(self, id, func, request_body):
        if id not in self.futures:
            with ThreadPool() as pool:
                future = pool.schedule(
                    func,
                    kwargs=request_body["input"],
                )
                self.futures[id] = future
                while not future.done():
                    logging.info("sleeping")
                    await asyncio.sleep(0.1)
                del self.futures[id]
                return future.result()
        else:
            return RunnerResult(
                "A prediction is already running with id -> {}".format(id)
            )

    def cancel(self, id) -> bool:
        if id not in self.futures:
            raise HTTPException(status_code=404, detail="id not found")
        result = self.futures[id]
        result.cancel()
        del self.futures[id]
        logging.debug("Cancel result {}".format(result))
        return result

    def clean_up(self):
        for id, future in self.futures.items():
            future.cancel()
