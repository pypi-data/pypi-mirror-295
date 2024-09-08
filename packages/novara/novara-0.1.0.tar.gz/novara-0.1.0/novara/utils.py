import yaml
from rich.console import Console
from rich.logging import RichHandler
from pathlib import Path
from random import randrange, seed
import logging
import os
import toml
from box import Box

# -----------------------------------------------------------------

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rich")
console = Console()

# -----------------------------------------------------------------


def print(*args, **kwargs):
    console.print(*args, **kwargs)


# -----------------------------------------------------------------


def color_value(value: str):
    seed(value.lower())
    r, g, b = [str(hex(randrange(25, 255))[2:]) for _ in range(3)]
    value_colored = f"[bold #{r}{g}{b}]{value}[/]"

    return value_colored


# -----------------------------------------------------------------

CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
CONFIG_FILE = CONFIG_HOME / "novara" / "config.yml"
SSHKEY_FILE = CONFIG_HOME / "novara" / "novara.key"

def write_config(config: dict):
    try:
        dot_config = CONFIG_HOME
        if not dot_config.exists():
            logger.info(f"creating directory {dot_config}")
            dot_config.mkdir()
        config_directory = CONFIG_FILE.parent
        if not config_directory.exists():
            logger.info(f"creating directory {config_directory}")
            config_directory.mkdir()
        yaml.dump(config, open(CONFIG_FILE, "w"))
    except OSError:
        logger.error("Couldn't create the config file it's not writable")
        exit()
    # --------------
    try:
        with open(SSHKEY_FILE, "w") as f:
            f.write(config["ssh_privatekey"])
    except OSError:
        logger.error("Couldn't create the SSH-key it's not writable")
    # --------------
    try:
        os.chmod(SSHKEY_FILE, 0o600)
    except OSError:
        logger.error("Couldn't change the SSH-key's permissions")
        exit()

def get_current_config():
    try:
        with open("novara.toml", "r") as f:
            # exploit_config = toml.load(f)
            toml_parsed = toml.load(f)
    except (OSError, FileNotFoundError):
        return None
    return Box(toml_parsed)