import httpx
import asyncio
import json
import os
from logging import getLogger
from typing import List
from gnt_monitoring.helpers import percentage
from dataclasses import dataclass, field
from pathlib import Path

_logger = getLogger(__name__)


@dataclass
class GntRapiAuth:
    """
    Dataclass for httpx auth info

    :param str user: Username
    :param str password: Password for user (UNSECURE)
    :param Path netrc: path to netrc file, containing login info
    """
    user: str = field(repr=False)
    password: str = field(repr=False)
    netrc: Path = field(repr=False)
    auth: httpx.BasicAuth | httpx.NetRCAuth = field(init=False)

    def __post_init__(self) -> None:
        if self.user:
            self.auth = httpx.BasicAuth(username=self.user, password=self.password)
            self.__delattr__("netrc")
            self.__delattr__("user")
            self.__delattr__("password")
            return
        if not os.path.exists(self.netrc):
            raise ValueError(f"File {self.netrc} doesn't exist")
        self.auth = httpx.NetRCAuth(file=self.netrc)


class GntMonitoring():
    """
    Class for ganeti monitoring

    :param str host: Hostname of Ganeti rapi daemon, default localhost
    :param str scheme: scheme protocol to use for requests, default: https
    :param int port: port at which ganeti remote api runs, default: 5080
    :param bool verify_ssl: check if ssl certificate valid, default false
    :param GntRapiAuth auth: Authentication dataclass for rapi
    """

    def __init__(self,
                 host: str,
                 scheme: str,
                 port: int,
                 auth: GntRapiAuth,
                 verify_ssl: bool = False) -> None:
        addr = [scheme]
        addr.append("://")
        addr.append(host)
        addr.append(f":{port}")
        self.address = "".join(addr)
        self.verify_ssl = verify_ssl
        self.auth = auth
        _logger.debug(f"Rapi address: {self.address}")
        with httpx.Client(auth=self.auth.auth, verify=self.verify_ssl) as http_client:
            test = http_client.get(url=self.address)
        if test.status_code == 401:
            msg = "Username and/of password incorrect" if auth.user or auth.password else "Username and/or password not provided"
            raise ValueError(msg)

    def __str__(self) -> str:
        return self.address

    async def _get_uri(self, url: list) -> list:
        """
        AsyncIO based httpx get client
        :param list url: List of url to get
        :return: list of responses
        """
        async with httpx.AsyncClient(auth=self.auth.auth, verify=self.verify_ssl) as http_client:
            tasks = [http_client.get(f"{self.address}{u}") for u in url]
            results = await asyncio.gather(*tasks)
        return results

    async def hosts(self) -> List[dict]:
        """
        Get all nodes
        :return: list of dicts
        """
        response = await self._get_uri(["/2/nodes"])
        return json.loads(response[0].text)

    async def _memory_allocated(self, instances: list) -> int:
        """
        Calculate allocated memory for instance list
        :param list instances: List of instances to sum maxmemory
        :return: sum of max memory
        """
        _logger.debug("Collecting allocated memory")
        uri = [f"/2/instances/{i}" for i in instances]
        response = await self._get_uri(uri)
        instance_info = [json.loads(info.text) for info in response]
        return sum(item["beparams"]["maxmem"] for item in instance_info)

    async def host_memory(self, host: str) -> dict:
        """
        collect host memory usage data
        :param str host: Host id for which collect info
        :returns: Dictionary of memory data
        """
        _logger.info(f"Collecting memory data for {host}")
        results = {}
        response = await self._get_uri([f"/2/nodes/{host}"])
        response = json.loads(response[0].text)
        host_instance_list = response.pop("pinst_list")
        results["total"] = response.pop("mtotal")
        results["used"] = response.pop("mnode")
        results["free"] = response.pop("mfree")
        results["used_perc"] = percentage(results["used"], results["total"])
        results["allocated"] = await self._memory_allocated(instances=host_instance_list)
        results["allocated_perc"] = percentage(results["allocated"], results["total"])
        return results
