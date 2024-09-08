import rich_click as click
import subprocess
import os
from novara.utils import logger, SSHKEY_FILE
from novara.config import config


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.pass_context
def docker(ctx):
    """this command allows you to control the docker on the remote with the docker cli"""

    env = {
        **os.environ.copy(),
        "DOCKER_HOST": f"ssh://{config.ssh_user}@{config.ssh_url}:{config.ssh_port}",
        "DOCKER_SSH_KEYPATH": SSHKEY_FILE,
    }

    docker = subprocess.Popen(["docker", *ctx.args], env=env)

    try:
        docker.wait()
    except KeyboardInterrupt:
        logger.warn("terminating tunnel")
    docker.kill()
