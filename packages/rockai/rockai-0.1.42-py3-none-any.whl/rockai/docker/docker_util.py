import json
from pathlib import Path
import logging
import subprocess
import importlib.metadata
import sys
from rockai.server.utils import get_dependencies, load_predictor_class
from rockai.command.openapi_schema import get_openapi_json

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("docker").setLevel(logging.WARNING)


def remove_some_libs(file_name, lib_to_be_deleted):
    try:
        # Open the file in read mode
        with open(file_name, "r") as file:
            lines = file.readlines()

        # Open the file in write mode
        with open(file_name, "w") as file:
            for line in lines:
                if lib_to_be_deleted not in line:
                    file.write(line)

        print("Successfully removed {} from {}".format(lib_to_be_deleted, file_name))
    except FileNotFoundError:
        print("{} not found".format(file_name))


def get_tensorflow_version(filename: str) -> str:
    """
    Reads a pip's requirements.txt file and returns the TensorFlow version specified in it.
    """
    try:
        with open(filename, "r") as file:
            for line in file:
                if line.startswith("tensorflow=="):
                    # Split the line at '==' to get the package and version
                    parts = line.strip().split("==")
                    if len(parts) == 2:
                        return parts[1]
                    else:
                        return "No specific version specified"
        return None
    except FileNotFoundError:
        return "File not found"


def run_command_and_get_output(file_name):
    # Run the command and capture the output
    output = get_openapi_json(file_name)

    return "'{}'".format(
        str(json.dumps(json.dumps(json.loads(output)), separators=(",", ":")))
    )


def build_docker_image_without_configuration(
    image_name: str,
    predictor_file_name: str,
    port: int,
    is_using_gpu: bool,
    platform="linux/amd64",
    is_dry_run: bool = False,
    upload_url: str = "",
):
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    base_image = (
        "nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04"
        if is_using_gpu
        else "python:{}".format(python_version)
    )

    docker_list = []
    docker_list.append(add_base(base_image))
    docker_list.append(add_env("DEBIAN_FRONTEND=noninteractive"))
    docker_list.append(add_cmd("export HF_ENDPOINT=https://hf-mirror.com"))
    docker_list.append(add_work_dir("/src"))
    docker_list.append(copy_files(".", "/src"))
    if is_using_gpu: # gpu support
        docker_list.append(
            add_run(
                "sed -i 's/http:\/\/archive.ubuntu.com\/ubuntu\//http:\/\/mirrors.tuna.tsinghua.edu.cn\/ubuntu\//g' /etc/apt/sources.list"
            )
        )
        docker_list.append(add_run("apt clean"))
        docker_list.append(add_run("apt-get clean"))
        docker_list.append(add_run("apt update && apt-get update"))
        docker_list.append(add_env('PATH="/root/.pyenv/shims:/root/.pyenv/bin:$PATH"'))
        docker_list.append(
            add_run(
                """--mount=type=cache,target=/var/cache/apt apt-get update -qq && apt-get install -qqy --no-install-recommends \
        make \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        libncurses5-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libffi-dev \
        liblzma-dev \
        git \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*
    """
            )
        )
        docker_list.append(
            add_run(
                """curl -s -S -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash && \
	git clone https://github.com/momo-lab/pyenv-install-latest.git "$(pyenv root)"/plugins/pyenv-install-latest && \
	pyenv install-latest {} && \
	pyenv global $(pyenv install-latest --print {}) && \
	pip install "wheel<1"
""".format(
                    python_version,
                    python_version,
                )
            )
        )
    else: # cpu only
        docker_list.append(add_run("apt update && apt-get update"))

    docker_list.append(add_expose(port))
    docker_list.append(
        add_run(f"pip install rockai=={importlib.metadata.version('rockai')}")
    )
    pred = load_predictor_class(predictor_file_name)
    ## install python library if any
    py_libs = get_dependencies(pred, "requirement_dependency")
    print(py_libs)
    for item in py_libs:
        docker_list.append(
            add_run(f"pip install {item} -i https://pypi.tuna.tsinghua.edu.cn/simple")
        )
    docker_list.append(add_run("pip install huggingface_hub hf_transfer"))
    ## install system library if any
    system_libs = get_dependencies(pred, "system_dependency")
    print(system_libs)
    for item in system_libs:
        docker_list.append(add_run(f"apt install -y {item}"))

    docker_list.append(
        add_labels(
            "run.cog.openapi_schema", run_command_and_get_output(predictor_file_name)
        )
    )
    docker_list.append(
        add_cmd(
            "rockai start --port {} --file {} --upload-url {}".format(
                port, predictor_file_name, upload_url
            )
        )
    )

    save_docker_file(docker_list)
    if not is_dry_run:
        subprocess.run(
            [
                "docker",
                "build",
                "--platform",
                platform,
                "-t",
                image_name,
                "-f",
                Path.cwd() / ".rock_temp/Dockerfile",
                Path.cwd(),
            ]
        )





def add_base(base):
    return "FROM {}\n".format(base)


def add_cmd(cmd_list):
    return "CMD {}\n".format(cmd_list)


def add_expose(port):
    return "EXPOSE {}\n".format(port)


def add_work_dir(dir):
    return "WORKDIR {}\n".format(dir)


def add_run(cmd):
    return "RUN {}\n".format(cmd)


def copy_files(src, dest):
    return "COPY {} {}\n".format(src, dest)


def add_env(env):
    return "ENV {}\n".format(env)


def add_labels(key, value):
    return "LABEL {}={}\n".format(key, value)


def save_docker_file(cmd_list):
    result = "".join(cmd_list)
    # Define the directory path
    directory_path = Path(str(Path.cwd() / ".rock_temp"))

    # Check if the directory exists
    if not directory_path.exists():
        # If it does not exist, create the directory
        directory_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")
    try:
        with open(Path.cwd() / ".rock_temp/Dockerfile", "w") as file:
            file.write(result)
    except Exception as e:
        print("An error occurred while writing to the file. Error: ", str(e))
