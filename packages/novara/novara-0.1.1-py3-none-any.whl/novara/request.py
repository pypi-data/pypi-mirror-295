import requests
from novara.config import config
from urllib.parse import urljoin
import requests.auth
import click
from requests import JSONDecodeError

class request:
    @staticmethod
    def get(*args, **kwargs):
        return request.request("get", *args, **kwargs)

    @staticmethod
    def post(*args, **kwargs):
        return request.request("post", *args, **kwargs)

    @staticmethod
    def delete(*args, **kwargs):
        return request.request("delete", *args, **kwargs)

    def request(type, path: str, *args, **kwargs):
        try:
            if not path.endswith("/"):
                path += "/"
            if not path.startswith("/api/"):
                path = ("/api/" + path).replace("//", "/")
            return requests.request(
                *args,
                method=type,
                auth=requests.auth.HTTPBasicAuth(*config.basic_auth)
                if config.auth_type == "basic"
                else None,
                url=urljoin(config.server_url, path),
                **kwargs,
            )
        except Exception as e:
            raise click.ClickException(
                f"request to remote failed with error {e}. Did you run novara configure?"
            )