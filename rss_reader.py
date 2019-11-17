#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from sys import exit
from termcolor import colored

from core.__version__ import __version__

from core.document import Document
from core.logger import create_logger
from core.requester import request_xml

parser = ArgumentParser(prog="RSS reader", description="Pure Python command-line RSS reader.")

parser.add_argument("source", type=str, help="RSS URL")
parser.add_argument("--version", action="version", help="Print version info", version=__version__)
parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
parser.add_argument("--limit", type=int, default=0, help="Limit news topics if this parameter provided")

args = parser.parse_args()
logger = create_logger(args.verbose)

try:
    response = request_xml(args.source, logger)
    document = Document.from_xml(response, args.limit, logger)
    data = document.to_json() if args.json else str(document)
    print(data)
except Exception as e:
    logger.error(e)
    print(colored(str(e), "red"))
    exit(1)