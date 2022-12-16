#!/bin/python3

"""
The tool to patch final HTML file, add custom css, credit information and so
should be invoked after pandoc
Arguments : length 1, the filename (basename)
"""
import os

from .metadata import BlogArticles, ArticleMetaData

from datetime import datetime
from toml import load
from sys import argv


class ArticlePatcher:
    def __init__(self, title: str) -> None:
        # TODO: use UUID to determine target
        # find TOML file and load it here to prevent load all the configs
        self.configure_path: str = os.path.join("./src/articles/", title, "config.toml")
        self.patchTarget: str = os.path.join("./output/articles/", title, "_index.html")
        self.rawFilePath: str = os.path.join("./src/articles/", title, f"{title}.md")

        if (
            not os.path.exists(self.patchTarget)
            or not os.path.exists(self.configure_path)
            or not os.path.exists(self.rawFilePath)
        ):
            print(f"Failed to find target {self.patchTarget}.")
            exit(2)
        self.targetArticleMetadata = ArticleMetaData(
            self.rawFilePath, load(open(self.configure_path, "r"))
        )

        self.rawFileContent: str = open(self.patchTarget, "r").read()

    def patchExternCSS(self):
        # process extern CSS links, insert them into head
        # by replace <!-- EXTERNS -->
        # allowCSS is checked by metadata loader, skip check here.
        result = ""
        for link in self.targetArticleMetadata.externCSSLinks:
            result += f"<link rel='stylesheet' href='{link}' />\n"
        self.rawFileContent = self.rawFileContent.replace("<!-- EXTERNS -->", result)
        return self

    def patchLastModifyDate(self):
        # patch last modify data.
        # replace <!-- LASTMODIFY -->
        if self.targetArticleMetadata.shouldLastModifyUpdated:
            self.rawFileContent = self.rawFileContent.replace(
                "<!-- LASTMODIFY -->",
                f"<span class='date before-toc'>Modified:<time>{datetime.now().strftime('%Y-%m-%d %H:%M')}</time></span>",
            )
        return self

    def patchCreditInfo(self):
        # patch credit info
        # replace <!-- LICENSE -->
        if self.targetArticleMetadata.credit == "default":
            self.rawFileContent = self.rawFileContent.replace(
                "<!-- LICENSE -->",
                "<a href='https://creativecommons.org/licenses/by-nc-sa/2.5/cn/'>CC BY-NC-SA 2.5 CN</a>",
            )
            print(self.rawFileContent)
        else:
            self.rawFileContent = self.rawFileContent.replace(
                "<!-- LICENSE -->", f"<a>{self.targetArticleMetadata.credit}</a>"
            )
        return self

    def patchCommentArea(self):
        # TODO
        print(f"{__file__} {__name__} TODO!")
        return self

    def save_file(self):
        with open(self.patchTarget, "w") as fp:
            fp.write(self.rawFileContent)
            fp.flush()
            fp.close()


def _patch_output(arg):
    ArticlePatcher(
        arg
    ).patchExternCSS().patchCreditInfo().patchLastModifyDate().patchCommentArea().save_file()
