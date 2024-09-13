import asyncio
from collections.abc import Callable
from urllib.parse import urljoin
import pandas as pd
from navconfig.logging import logging
from flowtask.components.abstract import DtComponent
from flowtask.components.interfaces.http import HTTPService
from flowtask.exceptions import ComponentError


class OdooInjector(DtComponent, HTTPService):

    accept: str = "application/json"
    download = None
    # auth_type: str = "api_key"
    _credentials: dict = {
        "HOST": str,
        "PORT": str,
        "APIKEY": str,
        "INJECTOR_URL": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.credentials: dict = {}
        # Initialize parent classes explicitly
        DtComponent.__init__(self, loop=loop, job=job, stat=stat, **kwargs)
        HTTPService.__init__(self, **kwargs)

    async def start(self, **kwargs):
        # self.headers = None
        # self._proxies = None
        # self.auth = ""
        # self.auth_type = ""
        # self.download = None
        # self.timeout = 180
        # self.accept = "application/json"

        # self.auth = {"apikey": self.credentials["APIKEY"]}

        if self.previous and isinstance(self.input, pd.DataFrame):
            self.data = self.input.to_dict(orient="records")

        self.processing_credentials()

        self.headers = {"api_key": self.credentials["APIKEY"]}

        self.url = self.get_url()

        return True

    async def run(self):
        payload = self.get_payload()
        result, error = await self.session(
            url=self.url, method="post", data=payload, use_json=True
        )

        if (
            not error
            and not "error" in result["result"]
            and result["result"].get("ids")
        ):
            logging.debug(result)
            return True

        error_msg = str(
            error or result["result"].get("error") or result["result"]["messages"]
        )
        raise ComponentError(error_msg)

    async def close(self):
        return True

    def get_url(self):
        port = (
            f":{self.credentials['PORT']}" if self.credentials["PORT"] != "80" else ""
        )
        base_url = f"{self.credentials['HOST']}{port}"
        url = urljoin(base_url, self.credentials["INJECTOR_URL"])
        return url

    def get_payload(self):
        return {
            # "model": "res.partner",
            "model": self.model,
            "options": {
                # 'has_headers': True,
                "advanced": False,
                "keep_matches": False,
                # 'name_create_enabled_fields': {'country_id': False},
                "name_create_enabled_fields": {},
                "import_set_empty_fields": [],
                "import_skip_records": [],
                "fallback_values": {},
                "skip": 0,
                "limit": 2000,
                # 'encoding': '',
                # 'separator': '',
                "quoting": '"',
                # 'sheet': 'Sheet1',
                "date_format": "",
                "datetime_format": "",
                "float_thousand_separator": ",",
                "float_decimal_separator": ".",
                "fields": [],
            },
            "data": self.data,
        }

    def processing_credentials(self):
        if self.credentials:
            for value, dtype in self._credentials.items():
                try:
                    if type(self.credentials[value]) == dtype:
                        default = getattr(self, value, self.credentials[value])
                        val = self.get_env_value(
                            self.credentials[value], default=default
                        )
                        self.credentials[value] = val
                except (TypeError, KeyError) as ex:
                    self._logger.error(f"{__name__}: Wrong or missing Credentials")
                    raise ComponentError(
                        f"{__name__}: Wrong or missing Credentials"
                    ) from ex
