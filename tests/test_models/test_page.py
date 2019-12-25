# coding: utf-8

from unittest import TestCase

from slage.models.page import RenderedPage


class RenderedPageTests(TestCase):
    def test_parse(self):
        # language=HTML
        html = '''
            <html lang="en">
                <head>
                    <meta name="author" content="slapec">
                    <meta name="keywords" content="c, a, b">
                    <title>Test post</title>
                </head>
                <body>
                    <h1>Test content</h1>
                </body>
            </html>
        '''

        page = RenderedPage(None, html)
        self.assertEqual(page.language, 'en')
        self.assertEqual(page.author, 'slapec')
        self.assertEqual(page.keywords, ('a', 'b', 'c'))
        self.assertEqual(page.title, 'Test post')
