#!/bin/python3

"""
Tool to generate fonts html file for font-spider
print HTML to stdout
Arguments: length 1 or 2, first is raw file path, if have second, 
    generate only TW-Sung else generate both.
"""

from sys import argv
from functools import reduce


class CharacterFilter:
    SPEC_CHARACTERS = ["！", "？", "。", "，", "“", "”", "：", "；", "）", "（"]
    TEMPLATE_WITH_BOTH = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @font-face {
                font-family: 'twsung';
                src: url('./TW-Sung-98_1.woff2') format('woff2'), url('./TW-Sung-98_1.woff') format('woff'),
                    url('./TW-Sung-98_1.ttf') format('truetype'), url('./TW-Sung-98_1.svg') format('svg');
            }

            h1 {  font-family: 'twsung'; }

            @font-face {
                font-family: 'hwgccn';
                src: url('./CJgaodeguomh.woff2') format('woff2'), url('./CJgaodeguomh.woff') format('woff'),
                    url('./CJgaodeguomh.ttf') format('truetype'), url('./CJgaodeguomh.svg') format('svg');
            }

            h2 {  font-family: 'hwgccn'; }
        </style>
    </head>
    """

    TEMPLATE_WITH_ONLY_TWSUNG = """
    <!DOCTYPE html>
    <html>
    <style>
        @font-face {
            font-family: 'twsung';
            src: url('./TW-Sung-98_1.woff2') format('woff2'), url('./TW-Sung-98_1.woff') format('woff'),
                url('./TW-Sung-98_1.ttf') format('truetype'), url('./TW-Sung-98_1.svg') format('svg');
        }

        h1 {  font-family: 'twsung'; }
    </style>
    """

    class CharacterSet(set):
        def __str__(self) -> str:
            try:
                return reduce(lambda x, y: x + y, self)
            except TypeError:
                return ""

    def __init__(self, raw: str, needTWSung: bool, needCJao: bool) -> None:
        self.rawPath = raw
        self.characters_for_twsung = CharacterFilter.CharacterSet()
        self.characters_for_cjao = CharacterFilter.CharacterSet()
        self.needTWSung = needTWSung
        self.needCJao = needCJao

    def filter_characters(self):
        for line in open(self.rawPath, "r").readlines():
            for i in filter(
                lambda x: "\u4e00" <= x <= "\u9fff"
                or x in CharacterFilter.SPEC_CHARACTERS,
                line,
            ):
                self.characters_for_cjao.add(i) if (
                    line.startswith("#") or line.startswith("title:")
                ) and self.needCJao else self.characters_for_twsung.add(i)
        return self

    def generate_target_html(self):
        if self.needCJao:
            return (
                CharacterFilter.TEMPLATE_WITH_BOTH
                + f"<body><h1>{self.characters_for_twsung}</h1><h2>{self.characters_for_cjao}</h2></body>\n</html>"
            )
        else:
            return (
                CharacterFilter.TEMPLATE_WITH_ONLY_TWSUNG
                + f"<body><h1>{self.characters_for_twsung}</h1></body>\n</html>"
            )


if __name__ == "__main__":
    if len(argv) == 3:
        # character-filter filepath TWSungOnly
        result = CharacterFilter(argv[1], True, False)
    else:
        result = CharacterFilter(argv[1], True, True)

    print(result.filter_characters().generate_target_html())
