import rich_click as click
from novara.utils import write_config
from urllib.parse import urljoin, urlparse
import os
import requests


@click.command()
@click.option(
    "--server_url",
    "-l",
    default=None,
    help="url to api-endpoint of your novara instance",
)
@click.option(
    "--username",
    "-u",
    default=None,
    help="username for basic auth. In the case of oauth this parameter does nothing.",
)
@click.option(
    "--password",
    "-p",
    default=None,
    help="password for basic auth. In the case of oauth this parameter does nothing.",
)
@click.option(
    "--author",
    "-a",
    default=None,
    help="to specify what author to use for the exploits",
)
def configure(server_url, username, password, author):
    """conect to novara backend & configure the cli"""

    # Priority: CLI argument > Environment variable > Prompt

    server_url = (
        server_url
        or os.environ.get("SERVER_URL")
        or click.prompt("Please enter the Novara server URL")
    )

    parsed_server_url = urlparse(server_url)

    username = (
        username
        or parsed_server_url.username
        or click.prompt("Please enter your username")
    )
    password = (
        password
        or parsed_server_url.password
        or os.environ.get("PASSWORD")
        or click.prompt("Please enter your password")
    )

    author = (
        author
        or os.environ.get("AUTHOR_NAME")
        or click.prompt("Please enter your author username")
    )

    # -----------------------------------------------------------------

    r = requests.get(
        urljoin(server_url, "/api/config/"),
        auth=requests.auth.HTTPBasicAuth(username, password),
    )
    if not r.ok:
        raise click.ClickException(f"the remote responded with error:\n{r.text}")
        exit()

    # -----------------------------------------------------------------

    try:
        config = r.json()
    except requests.JSONDecodeError:
        raise click.ClickException(f"unable to decode response as json:\n{r.text}")

    config["server_url"] = server_url
    config["author"] = author

    if config["auth_type"] == "basic":
        config["basic_auth"] = [username, password]

    write_config(config)
