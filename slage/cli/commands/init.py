# coding: utf-8

import logging
import pathlib
from typing import TYPE_CHECKING

from slage.cli.parser import subparsers
from slage.models.site import Site

if TYPE_CHECKING:
    import argparse


log = logging.getLogger(__name__)


def command(args: 'argparse.Namespace') -> None:
    log.debug('CLI args: %s', args)
    directory = pathlib.Path(args.directory).expanduser().resolve()

    Site.create(directory)


parser = subparsers.add_parser(
    'init',
    help='Create new site'
)

parser.add_argument(
    'directory',
    help='Optional destination directory (default: current working directory)',
    nargs='?',
    default=pathlib.Path.cwd()
)

parser.set_defaults(func=command)
