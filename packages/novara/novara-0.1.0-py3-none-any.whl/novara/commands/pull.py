import rich_click as click
from novara.request import request, JSONDecodeError
from novara.utils import logger, get_current_config
from bullet import Bullet, YesNo
from io import BytesIO
from zipfile import ZipFile
import os
import shutil


def download_exploit(exploit_id: str, exploit_name: str, dir):
    if dir is None:
        dir = os.path.normpath(os.path.join(os.getcwd(), exploit_name))
    logger.info(f"exploit id: {exploit_id}")
    logger.info("requesting exploit")

    r = request.get(f"exploits/{exploit_id}/")
    if not r.ok:
        raise click.ClickException(
            f"Requesting exploit from remote failed with error: {r.text}. Did you run novara configure?"
        )
        exit()
    logger.info("extracting exploit")
    zip_template = BytesIO(r.content)
    if os.path.exists(dir):
        overwrite = YesNo(
            prompt=f"Do you want to overwrite the directory '{dir}'? (y/n)",
            prompt_prefix="",
            default="y",
        ).launch()
        if not overwrite:
            raise click.ClickException(
                "Directory already exists and can't be overwritten. Consider using the -d or --dir to specify a different directory."
            )
            exit()
        shutil.rmtree(dir)
    os.mkdir(dir)
    with ZipFile(zip_template) as zip:
        zip.extractall(dir)

    logger.info("Exploit extracted sucessfully")


@click.command()
@click.option(
    "-s", "--service", default=None, help="name of the service the exploit is targeting"
)
@click.option("-n", "--name", default=None, help="full name of the exploit to pull")
@click.option(
    "-d",
    "--directory",
    default=None,
    help="specify a different directory to save the exploit",
)
@click.option("-a", "--all", default=False, help="list all exploits", is_flag=True)
def pull(service, name, directory, all):
    """Pull existing exploits from novara, if no other arguments are provided and there is a novara.toml in the same directory the cli will try to pull the newest version of the exploit"""
    exploit = None
    if service is None and name is None and directory is None and not all:
        exploit = get_current_config()
    if exploit is not None:
        download_exploit(exploit['exploit_id'], f'{exploit['service']['name']}-{exploit['exploit_name']}', os.getcwd())
        exit()
    r = request.get("exploits/")
    if not r.ok:
        raise click.ClickException(
            f"failed requesting a list of exploits from remote with error: {r.text}"
        )
        exit()
    try:
        exploits = r.json()
    except JSONDecodeError:
        raise click.ClickException(f"unable to decode response as json:\n{r.text}")

    # -----------------------------------------------------------------

    # check if any exploits are even available
    if not len(exploits):
        raise click.ClickException("No exploits to pull!")
        exit()

    # pull by name ----------------------------------------------------
    if name and any(i["name"] == name for i in exploits):
        exploit = None
        for exploit in exploits:
            if exploit["name"] == name:
                exploit = exploit
                break

        download_exploit(exploit["id"], name, directory)
        exit()
    elif name:
        raise click.ClickException(f"No exploits named '{name}' available!")
        exit()

    # chose a service -------------------------------------------------

    if not all:
        services = []
        for exploit in exploits:
            if not exploit['service'] in services:
                services.append(exploit['service'])
        service = Bullet(
                prompt="please select a service:",
                choices=services,
            ).launch()

    # pull by service -------------------------------------------------
    if service and any(exploit["service"] == service for exploit in exploits):
        service_exploits = []
        for exploit in exploits:
            service_exploits.append(exploit) if exploit["service"] == service else None

        if len(service_exploits) > 1:
            name, index = Bullet(
                prompt="there are multiple exploits available for this service, please select one:",
                choices=[exploit["name"] for exploit in service_exploits],
                return_index=True,
            ).launch()
            exploit = service_exploits[index]
        else:
            exploit = service_exploits[0]

        download_exploit(exploit["id"], f'{exploit['service']}-{exploit['name']}', directory)
        exit()

    elif name:
        raise click.ClickException(f"No exploits for '{service}' available")
        exit()

    # pull by bullet-selection ----------------------------------------
    else:
        name, index = Bullet(
            prompt="chose a exploit:",
            choices=[f'{exploit["service"]}-{exploit["name"]}' for exploit in exploits],
            return_index=True,
        ).launch()

        exploit = exploits[index]
        download_exploit(exploit["id"], name, directory)
