# coding: utf-8

import os
import logging
import datetime

from typing import TYPE_CHECKING, Tuple

from slage import constants as consts

import lxml.etree
import lxml.html

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    import pathlib

    import jinja2


class TemplatePage:
    generator = f'{consts.__project__} {consts.__version__}'

    def __init__(self, template: 'jinja2.Template', template_path: 'pathlib.Path', destination_path: 'pathlib.Path') -> None:
        self._template = template
        self._template_path = template_path
        self._destination_path = destination_path
        self._created_at = datetime.datetime.fromtimestamp(os.stat(template.filename).st_ctime)

    @property
    def template_path(self) -> 'pathlib.Path':
        return self._template_path

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def url(self) -> str:
        return f'/{self._template_path}'

    def render(self, *args, **kwargs) -> 'RenderedPage':
        destination_path = self._destination_path

        log.info('Rendering: %s -> %s', self._template_path, destination_path)

        render = self._template.render(*args, **{
            **kwargs,
            'this': self
        })
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        destination_path.write_text(render)

        return RenderedPage(self, render)


class RenderedPage:
    def __init__(self, template_page: TemplatePage, rendered_content: str):
        self._template_page = template_page
        self._content = rendered_content

        self._parse()

    def _parse(self):
        self._root = root = lxml.html.fromstring(self._content)  # type: lxml.html.HtmlElement

        self._language = root.attrib.get('lang').strip().lower()

        head, = root.xpath('./head')  # type: lxml.html.HtmlElement
        author, = head.xpath('./meta[@name="author"]/@content')
        self._author = author.strip()

        keywords, = head.xpath('./meta[@name="keywords"]/@content')
        self._keywords = tuple(sorted(map(str.strip, keywords.split(','))))

        title, = head.xpath('./title/text()')
        self._title = title.strip()

        body, = root.xpath('./body')  # type: lxml.html.HtmlElement

        self._article = None
        try:
            article, = body.xpath('./main/article')  # type: lxml.html.HtmlElement
            self._article = lxml.html.tostring(article).decode()
        except ValueError:
            pass

    @property
    def template_page(self) -> TemplatePage:
        return self._template_page

    @property
    def url(self) -> str:
        return self._template_page.url

    @property
    def created_at(self) -> datetime.datetime:
        return self._template_page.created_at

    @property
    def content(self) -> str:
        return self._content

    @property
    def language(self) -> str:
        return self._language

    @property
    def author(self) -> str:
        return self._author

    @property
    def keywords(self) -> Tuple[str, ...]:
        return self._keywords

    @property
    def title(self) -> str:
        return self._title

    @property
    def article(self) -> str:
        return self._article
