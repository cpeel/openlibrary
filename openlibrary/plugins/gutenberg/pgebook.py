"""Handlers for PG eBooks"""

import os
import logging

import gutenberg.acquire.metadata
from gutenberg.acquire.metadata import InvalidCacheException
from gutenberg.query import get_metadata

logger = logging.getLogger("openlibrary.gutenberg")

CACHE_PATH = '/var/lib/openlibrary/gutenberg/metadata/metadata.db'

class InvalidEbook(Exception):
    pass

class PgEbook:
    format_extensions = {
        'text' : [
            '.txt',
        ],
        'epub' : [
            '.epub.images',
            '.epub.noimages',
            '.epub',
        ],
        'html' : [
            '.html',
            '.htm',
        ],
        'kindle' : [
            '.kindle.images',
            '.kindle.noimages',
            '.kindle',
        ],
    }

    cache_manager = gutenberg.acquire.metadata.MetadataCacheManager(
            'Sleepycat', CACHE_PATH)

    def __init__(self, ebook_num=None):
        self.ebook_num = ebook_num
        gutenberg.acquire.metadata.set_metadata_cache_manager(self.cache_manager)

    def get_link_to_book_record(self):
        """
        Returns a URL to a PG eBook record or None if it doesn't exist.
        """

        if not self.ebook_num:
            return

        # TODO: validate ebook_num is a valid record and throw InvalidEbook if not

        return "http://www.gutenberg.org/ebook/%s" % self.ebook_num

    def get_link_to_book_text(self, desired_format):
        """
        Returns a URL to a PG eBook text given a file format.
        Valid formats:
            * text
            * epub
            * html
            * kindle
        If there are multiple URLs that satisfies the request (eg: one with
        images and one without) the 'best' one is returned, for some definition
        of best.

        Returns None if unknown ebook or there is no link for the desired
        extension.
        """
        if not self.ebook_num:
            return

        if desired_format not in self.format_extensions:
            raise ValueError("desired_format is of unknown type")

        try:
            uris = get_metadata('formaturi', self.ebook_num)
        except InvalidCacheException:
            return

        for extension in self.format_extensions[desired_format]:
            for uri in uris:
                if uri.endswith(extension):
                    return uri
