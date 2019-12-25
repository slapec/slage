# coding: utf-8

import pathlib

__project__ = 'slage'
__version__ = '1.0.0'


class Paths:
    MODULE_ROOT = pathlib.Path(__file__).parent
    ASSETS = MODULE_ROOT / 'assets'


class Directories:
    SLAGE = '.slage'
    TEMPLATES = 'templates'
    STATIC = 'static'
    BUILD = 'build'

    EXCLUDE_SCANNING = frozenset((SLAGE, TEMPLATES, STATIC, BUILD))


class Pages:
    INDEX = 'index.html'
