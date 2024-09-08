from rich import traceback

traceback.install(show_locals=True)

import rich_click as click
from novara.commands.init import init
from novara.commands.status import status
from novara.commands.configure import configure
from novara.commands.pull import pull
from novara.commands.docker import docker
from novara.commands.generate import generate
from novara.commands.run import run
from novara.commands.logs import logs


@click.group()
def main():
    """novara is a cli tool to help in A/D CTFs"""


main.add_command(init)
main.add_command(configure)
main.add_command(status)
main.add_command(pull)
main.add_command(docker)
main.add_command(generate)
main.add_command(run)
main.add_command(logs)
