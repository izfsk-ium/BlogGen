#!/bin/python3

"""
The article metadata 
"""

import uuid
import re
from enum import Enum
from datetime import datetime
import os
import toml
from msgpack import packb

from .blog_utils import BlogUtils


class ArticleMetaData:
    def __init__(self, rawPath, tomlDict) -> None:
        self.filePath: str = rawPath
        self.title: str = tomlDict["title"]
        self.description: str = tomlDict["description"].replace("\n", " ")
        if self.description == "":
            self.description = self.generateDescription()
        self.uuid: uuid.UUID = uuid.UUID(tomlDict["uuid"])
        self.createDate: datetime = tomlDict["metadata"]["created"]
        self.author: str = tomlDict["metadata"]["author"]
        self.credit: str = tomlDict["metadata"]["credit"]

        self.tags: list[str] = tomlDict["category"]["tags"]
        self.category: str = tomlDict["category"]["category"]

        self.isDraft: bool = tomlDict["metadata"]["isDraft"]
        self.isOutdated: bool = tomlDict["metadata"]["isOutdated"]
        self.shouldLastModifyUpdated: bool = tomlDict["options"]["updateLastModifyDate"]
        self.shouldCommentAllowed: bool = tomlDict["options"]["allowComment"]
        self.externCSSLinks: list[str] = list()
        if tomlDict["options"]["allowUserCSS"]:
            self.externCSSLinks = tomlDict["options"]["externCSSLinks"]

    def __repr__(self) -> str:
        return (
            "\n".join([f"{name}:{value}" for name, value in vars(self).items()]) + "\n"
        )

    def generateDescription(self) -> str:
        return ";".join(
            [
                x.strip().replace("#", "").replace("<", "")
                for x in open(self.filePath, "r").readlines()
                if x.startswith("#")
            ]
        )


def remove_markdown(text):
    text = re.sub(r"^#*", "", text, flags=re.MULTILINE)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"!\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"```(.+?)```", "", text, flags=re.DOTALL)
    return text


class BlogArticles(object):
    isGenerated: bool = False

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(BlogArticles, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.all_articles: list[ArticleMetaData] = []
        for (markdown_file_path, base_dir) in BlogUtils.find_file("./src", ".md"):
            configure_file_path: str = os.path.join(base_dir, "config.toml")
            if not os.path.exists(configure_file_path):
                continue
            self.all_articles.append(
                ArticleMetaData(
                    markdown_file_path, toml.load(open(configure_file_path, "r"))
                )
            )
        self.generateAllArticleSearchData()

    def generateAllArticleSearchData(self):
        if not BlogArticles.isGenerated:
            searchData = []
            for i in [i for i in self.all_articles]:
                _, content = open(i.filePath).read().split("---", 2)[1:]
                searchData.append(
                    {
                        "title": i.title,
                        "path": f"/articles/{i.title}/index.html",
                        "date": i.createDate.timestamp(),
                        "data": remove_markdown(
                            "".join([i.strip() for i in content.split()])
                        ),
                    }
                )
            BlogArticles.isGenerated = True
            with open("output/overview.msgpack", "wb") as fp:
                fp.write(packb(searchData, use_bin_type=True))
                fp.flush()
                fp.close()

    def getAllArticleMetadata(self) -> list[ArticleMetaData]:
        return self.all_articles
