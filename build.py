#!/bin/python3

from lib.archive import generate_archive_page
from lib.rss import generate_rss_page
from lib.fs import generate_file_page
from lib.bookmarks import generate_bookmark_page
from lib.tags import generate_tags_page
from lib.category import generate_category_page
from lib.index import generate_index_page

from lib.patch_output import _patch_output

from lib.blog_utils import BlogUtils

from sys import argv


@BlogUtils.timeit
def BlogGen():
    generate_archive_page()
    generate_rss_page()
    generate_file_page()
    generate_bookmark_page()
    generate_tags_page()
    generate_category_page()
    generate_index_page()


if __name__ == "__main__":
    if len(argv) == 3:
        # Python's import system is so genius that i cannot fix ImportError at all
        # use this ugly way to fix now
        _patch_output(argv[2])
    else:
        BlogGen()
