import json
import asyncio
import time
from tabulate import tabulate
from logging import getLogger
from gnt_monitoring.arguments import arguments
from gnt_monitoring.logger import init_logger
from gnt_monitoring.sentry import Sentry
from gnt_monitoring.rapi import GntMonitoring, GntRapiAuth
from gnt_monitoring.helpers import convert_to_human, check_for_status
from gnt_monitoring.constants import NAGIOS_STATUS_CODES


async def memory_check(**kwargs) -> None:
    """
    Memory monitoring function
    :param float warning: percentage at which return warning
    :param float critical: percentage at which return critical
    """
    _logger = getLogger(__name__)
    _logger.debug(f"Starting {__name__}")
    _logger.debug(f"Received params: {kwargs}")
    warning = kwargs.pop("warning")
    critical = kwargs.pop("critical")
    rapi_host = kwargs.pop("rapi_host")
    rapi_port = kwargs.pop("rapi_port")
    rapi_scheme = kwargs.pop("rapi_scheme")
    monitoring_data = {}
    start = time.perf_counter()
    rapi_auth = GntRapiAuth(
            user=kwargs.pop("rapi_user"),
            password=kwargs.pop("rapi_password"),
            netrc=kwargs.pop("netrc_file"))
    cluster = GntMonitoring(
            host=rapi_host,
            port=rapi_port,
            scheme=rapi_scheme,
            auth=rapi_auth)
    hosts = await cluster.hosts()
    hosts = [h["id"] for h in hosts]
    for host in hosts:
        host_memory = await cluster.host_memory(host=host)
        host_memory["status"] = check_for_status(warning=warning, critical=critical, value=host_memory["allocated_perc"])
        _logger.debug(f"Memory data:\n{json.dumps(host_memory, indent=2)}")
        monitoring_data[host] = host_memory
    end = time.perf_counter()
    exec_time = round(end - start, 2)
    _logger.debug(f"Collecting data took: {exec_time}")
    process_results(monitoring_data)


def process_results(data: dict) -> None:
    """
    Process gathered results
    :param dict data: data collected from rapi
    :return: None
    """
    overal_status = max([s["status"] for _, s in data.items()])
    output = [["Host", "Status", "Usage %", "Total", "Allocated", "Used", "Available"]]
    for host, info in data.items():
        host_line = []
        host_line.append(host)
        status_converted = NAGIOS_STATUS_CODES.get(info["status"])
        host_line.append(status_converted)
        host_line.append(info["allocated_perc"])
        total = convert_to_human(info["total"])
        host_line.append(f"{total[0]} {total[1]}")
        allocated = convert_to_human(info["allocated"])
        host_line.append(f"{allocated[0]} {allocated[1]}")
        used = convert_to_human(info["used"])
        host_line.append(f"{used[0]} {used[1]}")
        free = convert_to_human(info["free"])
        host_line.append(f"{free[0]} {free[1]}")
        output.append(host_line)
    print(tabulate(output, tablefmt="simple", headers="firstrow", numalign="center"))
    exit(overal_status)


def main() -> None:
    """
    Tool entry point
    :returns: None
    """
    args = arguments()
    if args.warning >= args.critical:
        raise ValueError(f"Warning ({args.warning}) value can't be equal or higher then critical ({args.critical})")
    init_logger(level=args.log_level)
    if args.sentry_dsn:
        Sentry(dsn=args.sentry_dsn, env=args.sentry_env)
    asyncio.run(memory_check(**args.__dict__))
