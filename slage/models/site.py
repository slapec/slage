# coding: utf-8

import logging
import pathlib
import shutil
from typing import List, Optional

import jinja2

from slage import constants as consts
from slage.models import exceptions as exc
from slage.models.page import TemplatePage, RenderedPage
from slage import filters


log = logging.getLogger(__name__)


class Site:
    @classmethod
    def create(cls, root: pathlib.Path) -> 'Site':
        log.info('Creating new site in %s', root)

        slage_root = root / consts.Directories.SLAGE
        log.debug('Creating slage root in %s', slage_root)

        try:
            slage_root.mkdir()
            log.debug('Created successfully')

        except FileNotFoundError:
            raise exc.RootNotFound(root)

        except FileExistsError:
            raise exc.SiteExits(root)

        log.debug('Copying assets into %s', root)
        shutil.copytree(consts.Paths.ASSETS, root, dirs_exist_ok=True)

        log.info('Your site is ready')

        return Site(root)

    def __init__(self, root: pathlib.Path) -> None:
        log.debug('Slage site root is %s', root)

        self._root = root
        self._slage_root = root / consts.Directories.SLAGE
        self._templates_root = root / consts.Directories.TEMPLATES

        self._env = env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(root)),
            undefined=jinja2.StrictUndefined
        )
        env.filters['subrender'] = filters.subrender

        self._index_page_path_relative = pathlib.Path(consts.Pages.INDEX)
        self._index_page: Optional[TemplatePage] = None

        log.debug('All set')

    def build(self, destination: Optional[pathlib.Path] = None) -> None:
        if destination is None:
            destination = self._root / consts.Directories.BUILD

        log.info('Building slage site in %s', destination)

        pages: List[TemplatePage] = []
        log.info('Reading *.html files in %s', self._root)
        for html_path in self._root.rglob('*.html'):
            template_path = html_path.relative_to(self._root)
            destination_path = destination / template_path

            if template_path.parents[0].name not in consts.Directories.EXCLUDE_SCANNING:
                log.debug('Found %s', html_path)

                template = self._env.get_template(str(template_path))
                page = TemplatePage(template, template_path, destination_path)

                if page.template_path == self._index_page_path_relative:
                    log.debug('Index page exists')
                    self._index_page = page
                else:
                    pages.append(page)

                log.debug('Parsed as %s', page)

        log.debug('Going to render %s pages', len(pages) + bool(self._index_page))

        rendered_pages: List[RenderedPage] = []
        for page in pages:
            rendered_page = page.render()
            rendered_pages.append(rendered_page)

        if self._index_page:
            log.debug('Rendering the index page')
            self._index_page.render({
                'pages': rendered_pages
            })

    def __repr__(self):
        return f'<Site({self._root})>'
