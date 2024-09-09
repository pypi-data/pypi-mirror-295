import argparse
import os
from pathlib import Path


def base_args() -> argparse.ArgumentParser:
    args = argparse.ArgumentParser()
    general = args.add_argument_group(title="General options")
    sentry = args.add_argument_group(title="Sentry")
    ganeti = args.add_argument_group(title="Ganeti")
    general.add_argument(
            "--log-level",
            help=("Log level, default: %(default)s"),
            default="warning",
            choices=["debug", "info", "warning", "critical", "error"],
            type=str
            )
    general.add_argument(
            "--warning",
            help="Warning value, default: %(default)f",
            default=75,
            type=float
            )
    general.add_argument(
            "--critical",
            help="Critical value, default: %(default)f",
            default=90,
            type=float
            )
    sentry.add_argument(
            "--sentry-dsn",
            help="Sentry dsn for remote error logging",
            type=str
            )
    sentry.add_argument(
            "--sentry-env",
            help="Envronment name for sentry, defaul: %(default)s",
            default="dev",
            type=str
            )
    ganeti.add_argument(
            "--rapi-host",
            help="Gasneti remote api host name, defaul: %(default)s",
            type=str,
            default="localhost"
            )
    ganeti.add_argument(
            "--rapi-port",
            help="Remote api port, default: %(default)i",
            type=int,
            default=5080)
    ganeti.add_argument(
            "--rapi-scheme",
            help="Scheme to use, default: %(default)s",
            default="https",
            type=str
            )
    ganeti.add_argument(
            "--rapi-user",
            help="Username if authentication enabled",
            default=None,
            type=str)
    ganeti.add_argument(
            "--rapi-password",
            help="Password for user (UNSECURE, PLEASE USE netrc)",
            default=None,
            type=str)
    ganeti.add_argument(
            "--netrc-file",
            help="netrc file for authentication, default: %(default)s",
            type=Path,
            default=os.path.join(os.path.expanduser("~"), ".netrc"))
    return args


def arguments() -> argparse.Namespace:
    args = base_args()
    return args.parse_args()
