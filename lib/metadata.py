#!/bin/python3

"""
The article metadata 
"""

import uuid

from enum import Enum
from datetime import datetime
import os
import toml

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


class BlogArticles(object):
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

    def getAllArticleMetadata(self) -> list[ArticleMetaData]:
        return self.all_articles
