#!/bin/python3

"""
Patch fonts of article html, this script can be executed directly
Arguments : length 1 (file basename)
"""

from datetime import datetime
from os import unlink
from sys import argv


class FontPatcher:
    FontStyleTemplate = """
    <style>
        @font-face {{
            font-family: "twsung";
            src:    url("/articles/{filename}/assets/TW-Sung-98_1.woff2")   format('woff2'),
                    url("/articles/{filename}/assets/TW-Sung-98_1.woff")    format('woff'),
                    url("/articles/{filename}/assets/TW-Sung-98_1.ttf")     format('truetype'),
                    url("/articles/{filename}/assets/TW-Sung-98_1.svg")     format('svg');
        }}

        @font-face {{
            font-family: "hwgccn";
            src:    url("/articles/{filename}/assets/CJgaodeguomh.woff2")   format('woff2'),
                    url("/articles/{filename}/assets/CJgaodeguomh.woff")    format('woff'),
                    url("/articles/{filename}/assets/CJgaodeguomh.ttf")     format('truetype'),
                    url("/articles/{filename}/assets/CJgaodeguomh.svg")     format('svg');
        }}
    </style>
    """

    def __init__(self, basename: str) -> None:
        self.basename = basename
        self.path = f"./output/articles/{basename}/_index.html"
        self.font_html = ""
        self.last_modify_html = ""

    def generate_fonts_html(self):
        self.font_html = FontPatcher.FontStyleTemplate.format(filename=self.basename)
        return self

    def save_file(self):
        open(self.path.replace("_", ""), "w+").write(
            open(self.path)
            .read()
            .replace("<!-- FONTS -->", self.font_html)
        )
        return self

    def delete_old_file(self):
        unlink(self.path)


if __name__ == "__main__":
    print(f"Patch CSS for {argv[1]}")
    FontPatcher(argv[1]).generate_fonts_html().save_file().delete_old_file()
