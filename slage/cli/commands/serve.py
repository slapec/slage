# coding: utf-8

import logging
import pathlib
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import TYPE_CHECKING, Optional

from slage.cli.parser import subparsers

if TYPE_CHECKING:
    import argparse


log = logging.getLogger(__name__)


def command(args: 'argparse.Namespace') -> Optional[int]:
    log.debug('CLI args: %s', args)
    directory = pathlib.Path(args.directory).expanduser().resolve()

    server = partial(SimpleHTTPRequestHandler,  directory=str(directory))

    httpd = ThreadingHTTPServer(
        server_address=('127.0.0.1', 0),
        RequestHandlerClass=server
    )

    with httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        print(
            f"Serving HTTP on {host} port {port} "
            f"(http://{url_host}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            return 0


parser = subparsers.add_parser(
    'serve',
    help='Serves an already rendered site. Live rendering and reloading is not supported!'
)

parser.add_argument(
    '-d', '--directory',
    help='Optional Slage site (default: current working directory)',
    default=pathlib.Path.cwd()
)

parser.set_defaults(func=command)
