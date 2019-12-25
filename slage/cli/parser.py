# coding: utf-8

import argparse

from slage import constants as consts


parser = argparse.ArgumentParser(
    prog=consts.__project__,
    description=f'{consts.__project__} - my static site generator',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '-v', '--version',
    action='version',
    version=f'%(prof)s {consts.__version__}'
)

parser.add_argument(
    '-l', '--log-level',
    choices=('DEBUG', 'INFO'),
    default='INFO',
    help='Log level'
)

parser.add_argument(
    '--log-file',
    default=False,
    help='Path to the log file'
)

subparsers = parser.add_subparsers(
    title='Commands',
    dest='command',
    required=True
)
