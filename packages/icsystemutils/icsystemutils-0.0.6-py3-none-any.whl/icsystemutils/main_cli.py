#!/usr/bin/env python3

import argparse
import logging
import json

from iccore import runtime, logging_utils

from icsystemutils.cpu.cpu_info import CpuInfo
from icsystemutils.monitor import ResourceMonitor

logger = logging.getLogger(__name__)


def launch_common(args):
    runtime.ctx.set_is_dry_run(args.dry_run)
    logging_utils.setup_default_logger()


def read_cpu_info(args):
    launch_common(args)

    logger.info("Reading CPU info")

    info = CpuInfo()
    info.read()

    output = json.loads(str(info))
    print(json.dumps(output, indent=4))

    logger.info("Finished Reading CPU info")


def monitor(args):
    launch_common(args)

    logger.info("Starting monitor")
    resource_monitor = ResourceMonitor()
    resource_monitor.run()
    logger.info("Finished monitor")


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    read_cpu_parser = subparsers.add_parser("read_cpu")
    read_cpu_parser.set_defaults(func=read_cpu_info)

    monitor_parser = subparsers.add_parser("monitor")
    monitor_parser.set_defaults(func=monitor)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
