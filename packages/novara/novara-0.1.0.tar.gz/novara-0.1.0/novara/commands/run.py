import rich_click as click
from novara.utils import logger
from novara.commands.generate import generate_dockerfile
import docker
import toml
from io import BytesIO
from zipfile import ZipFile
import os
from novara.request import request, JSONDecodeError
import json
import docker.models.containers


@click.group()
def run():
    """run a exploit script either locally or on remote"""


@run.command()
def local():
    """run the exploit script locally"""
    client = docker.from_env()

    generate_dockerfile()

    logger.info("building image")
    image, logs = client.images.build(path=".")
    for docker_log in logs:
        logger.info(f'logs: {docker_log.get("stream", str(docker_log)).strip()}')

    logger.info("starting container")
    container: docker.models.containers.Container = client.containers.run(
        image, detach=True
    )
    try:
        for docker_log in container.logs(stream=True):
            click.echo(docker_log, nl=False)
    except KeyboardInterrupt:
        logger.warn("stopping container")
        container.stop()


@run.command()
@click.option(
    "-k",
    "--keep",
    default=False,
    is_flag=True,
    help="keep container, if it already exists",
)
def remote(keep):
    """upload and run the exploit on the remote server"""

    try:
        with open("novara.toml", "r") as f:
            toml_config = toml.load(f)
    except (OSError, FileNotFoundError):
        raise click.ClickException("novara.toml either not there or unaccessable")
        exit()
    logger.info("read toml file")

    if "exploit_id" not in toml_config:
        raise click.ClickException(
            "no exploit_id in toml found, consider regenerating the toml with novara init"
        )
        exit()

    exploit_id = toml_config.get("exploit_id")

    zip_archive = BytesIO()

    with ZipFile(zip_archive, "w") as zip:
        for root, _, filenames in os.walk(os.getcwd()):
            for name in filenames:
                zip.write(name, name)

    zip_archive.seek(0)

    logger.info("uploading zip...")

    r = request.post(f"exploits/{exploit_id}/", files={"file": zip_archive})
    if not r.ok:
        raise click.ClickException(f"Uploading zip failed with error: {r.text}")
        exit()

    try:
        with open("novara.toml", "r") as toml_file:
            toml_str = toml_file.read()
    except (FileNotFoundError, OSError):
        raise click.ClickException("Failed reading novara toml file")
        exit()

    logger.info("building image...")

    r = request.post(f"build/{exploit_id}/toml/", data=json.dumps(toml_str))
    if not r.ok:
        raise click.ClickException(
            f"Failed building novara toml file with error: {r.text}"
        )
        exit()

    try:
        image = r.json()
    except JSONDecodeError:
        raise click.ClickException(
            f"failed to decode response as json: {r.text[:20] if len(r.text) > 20 else r.text}"
        )

    if image is None:
        raise click.ClickException("Something went wrong while building image")
        exit()

    logger.info(f"image: {image}")

    if not keep:
        logger.info(f"requesting removal of old containers of exploit: {exploit_id}")
        r = request.delete(f"exploits/{exploit_id}/")
        if r.status_code == 404:
            logger.info("No containers found for current exploit")
        if not r.ok:
            logger.warn(f"failed removing container with message: {r.text}")

    logger.info("starting new container...")

    r = request.post("containers/", params={"exploit_id": exploit_id})
    if not r.ok:
        raise click.ClickException(
            f"Failed starting new container with error: {r.text}"
        )
        exit()

    try:
        container_info = r.json()
    except JSONDecodeError:
        raise click.ClickException(
            f"failed to decode response as json: {r.text[:20] if len(r.text) > 20 else r.text}"
        )
    for info in container_info:
        logger.info(f"{info}: {container_info[info]}")

    logger.info(
        "Done deploying new container, to redeploy the container just run 'novara run remote' again"
    )
