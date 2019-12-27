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
    SRC = 'src'

    EXCLUDE_SCANNING = frozenset((TEMPLATES, STATIC, SRC))


class Pages:
    INDEX = 'index.html'
    ABOUT = 'about.html'
