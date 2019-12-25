# coding: utf-8

import logging
import pathlib
import sys
import traceback
from typing import Optional

from slage import constants as consts
from slage import exceptions as exc
from slage.cli import parser

log = logging.getLogger(consts.__project__)


def main() -> Optional[int]:
    args = parser.parse_args()

    log.setLevel(args.log_level)

    formatter = logging.Formatter(
        '%(asctime)-15s | %(levelname)-7s | %(message)s'
    )

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(formatter)
    log.addHandler(stdout_handler)

    if args.log_file:
        file_handler = logging.FileHandler(
            pathlib.Path(args.log_file).expanduser()
        )
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)

    try:
        return_code = args.func(args)

    except exc.SlageError as e:
        return_code = e.return_code

        log.debug(traceback.format_exc())
        log.error(e)

    log.debug('Main returns with %s', return_code)

    return return_code


if __name__ == '__main__':
    return_code = main()

    sys.exit(return_code)
