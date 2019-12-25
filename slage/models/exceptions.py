# coding: utf-8

from typing import TYPE_CHECKING

from slage import exceptions as exc

if TYPE_CHECKING:
    import pathlib


class SiteError(exc.SlageError):
    def __init__(self, root: 'pathlib.Path'):
        self.root = root


class RootNotFound(SiteError):
    def __str__(self):
        return f'Slage site cannot be created in {self.root}.' \
               f' (A parent directory might not exists.)'


class SiteExits(SiteError):
    def __str__(self):
        return f'A slage site already exists in this directory: {self.root}.' \
               f' (The .slage directory already exists in that directory.)'


class DestinationError(SiteExits):
    def __str__(self):
        return 'Your destination directory must not be the same as your project directory'
