from novara.utils import CONFIG_FILE
from box import Box
import yaml
import click

class Config:
    conf = None
    def _load(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                conf_dict = yaml.safe_load(f)
            self.conf = Box(conf_dict)
        except:
            raise click.ClickException("""*Unable to load config file!!!* -> This will break the functionality of most commands
            Hint: You can create a new config file using 'novara configure'""")

    def __getattr__(self, name: str):
        if self.conf is None:
            self._load()
        return self.conf.__getattr__(name)

config = Config()