import rich_click as click
from string import ascii_lowercase, digits
from novara.utils import logger
from novara.request import request, JSONDecodeError
from random import choices
from io import BytesIO
from bullet import Bullet, YesNo
from zipfile import ZipFile
import os
import shutil
from novara.config import config


def get_service():
    r = request.get("services/")
    if not r.ok:
        raise click.ClickException(
            f"Failed requesting list of services from remote with error: {r.text}"
        )
        exit()
    try:
        services = r.json()
    except JSONDecodeError:
        raise click.ClickException(
            f"failed to decode response as json: {r.text[:20] if len(r.text) > 20 else r.text}"
        )

    service = Bullet(prompt="Please select a service", choices=services).launch()

    return service


@click.command()
@click.option(
    "-s",
    "--service",
    default=None,
    help="the name of the service the exploit will be attacking",
)
@click.option(
    "-n", "--name", default=None, help="the internal name for the exploit identifing it"
)
@click.option("-a", "--author", default=None, help="name of the exploit's author")
@click.option(
    "-d",
    "--directory",
    default=None,
    help="specify a different directory to put the exploit",
)
def init(service, name, author, directory):
    """Initialize a new exploit from a template"""

    # Priority: CLI argument > Environment variable > Prompt

    service = service or get_service()
    name = name or "".join(choices(ascii_lowercase + digits, k=6))
    author = (
        author
        or config.author
        or os.environ.get("AUTHOR")
        or click.prompt("Please enter this exploit author's name")
    )

    # -----------------------------------------------------------------

    directory_name = directory or f"{service}-{name}"
    full_directory = os.path.join(os.getcwd(), directory_name)
    logger.info(f"setting up directory: {full_directory}")

    if os.path.exists(full_directory):
        if YesNo(f"Do you want to overwrite the directory '{full_directory}'? (y/n)"):
            shutil.rmtree(full_directory)
        else:
            logger.info("Directory won't be overwritten, exiting...")
            exit()

    logger.info("requesting template")

    r = request.post(
        f"services/{service}/template/",
        params={"exploit_name": name, "exploit_author": author, "additional_args": ""},
    )
    if not r.ok:
        raise click.ClickException(
            f"Requesting template from remote failed with error: {r.text}. Did you run novara configure?"
        )
        exit()

    logger.info("extracting template")
    zip_template = BytesIO(r.content)
    os.mkdir(full_directory)
    with ZipFile(zip_template) as zip:
        zip.extractall(full_directory)

    
    logger.info(f"Template extracted sucessfully into directory {directory_name}")
    logger.info("To add a new dependency run 'novara generate'")
    logger.info("To run the current exploit run 'novara run [local|remote]'")
    logger.info("Happy exploiting!")
