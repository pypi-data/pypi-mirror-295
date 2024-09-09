import typer
from rockai.server.http import start_server
from rockai.server.utils import is_valid_name
from pathlib import Path
from typing_extensions import Annotated
from rockai.docker.docker_util import build_docker_image_without_configuration
import requests
import subprocess
import logging
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
import getpass

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

app = typer.Typer()

APP_NAME = "rockai"


def download_file(url: str, save_path: str):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        # Check if the request was successful
        response.raise_for_status()

        # Open the file in binary write mode and write the content
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the file: {str(e)}")


@app.command()
def init():
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Initiating, please wait...", total=None)
        download_file(
            "https://rockai-web-resouce-bucket.s3.ap-northeast-1.amazonaws.com/predictor.py",
            Path.cwd() / "predictor.py",
        )
        download_file(
            "https://rockai-web-resouce-bucket.s3.ap-northeast-1.amazonaws.com/dockerignore",
            Path.cwd() / ".dockerignore",
        )
        print("Init success!")


@app.command(name="build")
def build(
    port: Annotated[int, typer.Option(help="Port of the API server")] = 8000,
    name: Annotated[
        str,
        typer.Argument(
            help="Image name of the docker container --> Example: r.18h.online/jian-yang/hotdog-detector"
        ),
    ] = None,
    file: Annotated[
        str, typer.Option(help="Path to predictor.py file,default is predictor.py")
    ] = "predictor.py",
    gpu: Annotated[bool, typer.Option(help="Is using gpu")] = True,
    platform: Annotated[
        str,
        typer.Option(
            help="Docker image supported platform, `linux/amd64` by default, you can also change it to other platform like `linux/arm64/v8` if you are using MAC M2 chip"
        ),
    ] = "linux/amd64",
    dry_run: Annotated[
        bool, typer.Option(help="Generate Dockerfile without building the image")
    ] = False,
    upload_url: Annotated[
        str,
        typer.Option(
            help="Url for upload model output, Example:-> 'https://api.rockai.online/v1/get_presign_url?file_name=output.png' "
        ),
    ] = "https://api.rockai.online/v1/get_presign_url",
):
    """
    Build the image
    """

    if name is not None:
        if name.startswith("r.18h.online"):
            if is_valid_name(name.split("/")[-1]):
                build_docker_image_without_configuration(
                    name, file, port, gpu, platform, dry_run, upload_url
                )
            else:
                print(
                    f"Invalid model name '{name}'. Model name should start with a letter, contain only alphanumeric characters and hyphens, and be less than or equal to 140 characters long."
                )
        else:
            build_docker_image_without_configuration(
                name, file, port, gpu, platform, dry_run, upload_url
            )


@app.command()
def start(
    auth: Annotated[
        str, typer.Option(help="Bearer auth token of the API server")
    ] = None,
    port: Annotated[int, typer.Option(help="Port of the API server")] = 8000,
    file: Annotated[
        str, typer.Option(help="Path to predictor.py file,default is predictor.py")
    ] = "predictor.py",
    upload_url: Annotated[
        str,
        typer.Option(
            help="Url for upload model output, Example:-> 'https://api.rockai.online/v1/get_presign_url?file_name=output.png' "
        ),
    ] = "https://api.rockai.online/v1/get_presign_url",
):
    """
    start local development server
    """
    start_server(file, port, auth, upload_url)


@app.command("push")
def push_model(
    name: Annotated[
        str,
        typer.Argument(
            help="name of the image you want to push to rockai server,  --> Example: 'r.18h.online/jian-yang/hotdog-detector' "
        ),
    ]
):
    """
    Push the model to the RockAI platform
    """
    subprocess.run(["docker", "image", "push", "{}".format(name)])


@app.command(name="login")
def login_to_docker(
    api_token: Annotated[str, typer.Option(help="Your API token")] = None,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    """
    Login to the RockAI Docker registry
    """
    if api_token is None:
        api_token = getpass.getpass("Paste your API token:")
        print(api_token)
    url = "https://api.rockai.online/v1/user/docker_token"

    if debug:
        print("Debug mode is enabled")
        url = "https://api-dev.rockai.online:9090/v1/user/docker_token"

    headers = {"Authorization": "Bearer {}".format(api_token)}
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Logging in, please wait...", total=None)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        subprocess.run(
            [
                "docker",
                "login",
                "r.18h.online",
                "-u",
                response.json()["data"]["docker_robot_account"],
                "-p",
                response.json()["data"]["docker_token"],
            ]
        )
