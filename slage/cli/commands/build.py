# coding: utf-8

import logging
import pathlib
from typing import TYPE_CHECKING

from slage import constants as consts
from slage.cli.parser import subparsers
from slage.models.site import Site

if TYPE_CHECKING:
    import argparse


log = logging.getLogger(__name__)


def command(args: 'argparse.Namespace') -> None:
    log.debug('CLI args: %s', args)
    root = pathlib.Path(args.directory).expanduser().resolve()

    out = args.out
    if out is not None:
        out = pathlib.Path(out).expanduser().resolve()

    site = Site(root)
    site.build(out)


parser = subparsers.add_parser(
    'build',
    help='Build site'
)

parser.add_argument(
    'directory',
    nargs='?',
    default=pathlib.Path.cwd(),
    help='Optional slage directory (default: current working directory)'
)

parser.add_argument(
    '-o', '--out',
    help='Destination directory (default: ./build relative to the slage directory)'
)

parser.set_defaults(func=command)
