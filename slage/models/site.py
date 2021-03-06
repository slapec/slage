# coding: utf-8

import logging
import operator
import pathlib
import shutil
from typing import List, Optional

import jinja2

from slage import constants as consts, utils
from slage.models import exceptions as exc
from slage.models.page import TemplatePage, RenderedPage


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
        self._src_root = src_root = root / consts.Directories.SRC

        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(src_root)),
            undefined=jinja2.StrictUndefined
        )

        self._index_page_path_relative = pathlib.Path(consts.Pages.INDEX)
        self._index_page: Optional[TemplatePage] = None

        self._about_page_path_relative = pathlib.Path(consts.Pages.ABOUT)
        self._about_page: Optional[TemplatePage] = None

        log.debug('All set')

    def build(self, destination: Optional[pathlib.Path] = None) -> None:
        if destination is None:
            destination = self._root

        log.info('Writing rendered files in %s', destination)

        pages: List[TemplatePage] = []
        log.info('Reading *.html files in %s', self._src_root)
        for html_path in self._src_root.rglob('*.html'):
            template_path = html_path.relative_to(self._src_root)
            root_under_src = template_path.parents[0].name

            if root_under_src not in consts.Directories.EXCLUDE_SCANNING:
                log.debug('Found %s', html_path)

                template = self._env.get_template(str(template_path))
                destination_path = destination / template_path
                page = TemplatePage(template, template_path, destination_path)

                if page.template_path == self._index_page_path_relative:
                    log.debug('Index page exists')
                    self._index_page = page
                elif page.template_path == self._about_page_path_relative:
                    log.debug('About page exists')
                    self._about_page = page
                else:
                    pages.append(page)

                log.debug('Parsed as %s', page)
            elif root_under_src == consts.Directories.SRC:
                log.warning(
                    'Skipped rendering %s. Avoid placing HTML files in src/src as those would be rendered into src/'
                    ' thus rendered files would mix with or overwrite source files.',
                    template_path
                )

        log.debug('Going to render %s pages', len(pages) + bool(self._index_page))

        pages.sort(key=operator.attrgetter('created_at'), reverse=True)
        page_chunks = list(utils.chunks(pages, 100))
        for index_counter, chunk in enumerate(page_chunks):
            rendered_pages: List[RenderedPage] = []
            for page in chunk:
                rendered_page = page.render()
                rendered_pages.append(rendered_page)

            if self._index_page:
                log.debug('Rendering index page %s', index_counter)
                self._index_page.render({
                    'pages': rendered_pages,
                    'page_count': len(page_chunks)
                })

        if self._about_page:
            log.debug('Rendering the about page')
            self._about_page.render()

    def __repr__(self):
        return f'<Site({self._root})>'
