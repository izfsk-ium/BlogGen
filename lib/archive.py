#!/bin/python3


"""
Generate archive page.
"""

import itertools

from enum import Enum
from htmlmin import minify

from .blog_utils import BlogUtils
from .metadata import ArticleMetaData, BlogArticles


class ArchivePageContent:
    MONTH_TABLE: list[str] = [
        "",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    class NodeType(Enum):
        YearStart = "YearStart"
        MonthStart = "MonthStart"
        Article = "Article"
        MonthStop = "MonthStop"
        YearStop = "YearStop"

    class Node:
        def __init__(self, raw: ArticleMetaData) -> None:
            self.type = None
            self.data = None
            self.raw = raw

        def __repr__(self) -> str:
            return str(self.type)

        def buildYearStart(self):
            self.type = ArchivePageContent.NodeType.YearStart
            self.data = self.raw.createDate.year
            return self

        def buildMonthStart(self):
            self.type = ArchivePageContent.NodeType.MonthStart
            self.data = ArchivePageContent.MONTH_TABLE[self.raw.createDate.month]
            return self

        def buildArticle(self):
            self.type = ArchivePageContent.NodeType.Article
            self.data = self.raw
            return self

        def buildMonthStop(self):
            self.type = ArchivePageContent.NodeType.MonthStop
            return self

        def buildYearStop(self):
            self.type = ArchivePageContent.NodeType.YearStop
            return self

    def __init__(self) -> None:
        self.all_articles: list[
            ArticleMetaData
        ] = BlogArticles().getAllArticleMetadata()
        self.nodeElements: list[ArchivePageContent.Node] = list()
        self.htmlContent: str = str(self)

        self.month_article_counter = {
            x: len(list(y))
            for x, y in itertools.groupby(
                self.all_articles, lambda x: f"{x.createDate.year}.{x.createDate.month}"
            )
        }
        self.generate_node_tree()

    def __str__(self) -> str:
        html_content = "<div>"
        for item in self.nodeElements:
            match item.type:
                case ArchivePageContent.NodeType.YearStart:
                    html_content += f"<li class=l1> {item.data} </li>"
                case ArchivePageContent.NodeType.MonthStart:
                    html_content += f"""
                        <div class="archive-month">
                            <h3 class="archive-month-header">
                                {item.data}&nbsp;
                                <sub>{self.month_article_counter[f'{item.raw.createDate.year}.{item.raw.createDate.month}']}</sub>
                            </h3>
                        <div class="archive-posts">
                    """
                case ArchivePageContent.NodeType.Article:
                    html_content += ArchivePageContent.metaDataToArchiveString(item.raw)
                case ArchivePageContent.NodeType.MonthStop:
                    html_content += "</div></div>"
                case ArchivePageContent.NodeType.YearStop:
                    html_content += "<br/>"
                case _:
                    pass
        return str(html_content)

    def __repr__(self) -> str:
        # for debug. report node tree
        return "\n".join(
            [
                f"{i.type}{f'({i.data})' if i.type!=ArchivePageContent.NodeType.Article else ''}"
                for i in self.nodeElements
            ]
        )

    @staticmethod
    def metaDataToArchiveString(metadata: ArticleMetaData) -> str:
        IS_DRAFT: str = "<span class='draft'>草稿</span>"
        IS_OUTDATED: str = "<span class='outdated'>过期</span>"
        IS_ARTICLE: str = "文章"

        return f"""
        <div class="archive-entry">
            <h3 class="archive-entry-title">
                <a href="/articles/{metadata.title}/index.html">{metadata.title}</a>
            </h3>
            <div class="archive-meta" id="{metadata.uuid}">
                <span title="{metadata.title}">
                    {metadata.createDate.strftime("%Y-%m-%d，%H:%M:%S")}
                </span>
                ・{metadata.category}・{metadata.author}・{IS_DRAFT 
                    if metadata.isDraft else IS_OUTDATED 
                        if metadata.isOutdated else IS_ARTICLE}
            </div>
        </div>
        """

    def generate_html(self) -> str:
        return str(self)

    def iter_all_articles(self):
        return iter(
            sorted(
                self.all_articles, key=lambda x: x.createDate.timestamp(), reverse=True
            )
        )

    def generate_node_tree(self) -> None:
        ptr_first, ptr_second = itertools.tee(self.iter_all_articles(), 2)

        # push first year and month to store
        first_element = next(ptr_second)
        string_of_month = ArchivePageContent.MONTH_TABLE[first_element.createDate.month]
        self.nodeElements.append(
            ArchivePageContent.Node(first_element).buildYearStart()
        )
        self.nodeElements.append(
            ArchivePageContent.Node(first_element).buildMonthStart()
        )

        # compare two iterator, if have difference, store diff data, catch exceptions
        while True:
            try:
                left = next(ptr_first)
                self.nodeElements.append(ArchivePageContent.Node(left).buildArticle())
                right = next(ptr_second)
                if left.createDate.year != right.createDate.year:
                    self.nodeElements.append(
                        ArchivePageContent.Node(left).buildMonthStop()
                    )
                    self.nodeElements.append(
                        ArchivePageContent.Node(left).buildYearStop()
                    )
                    self.nodeElements.append(
                        ArchivePageContent.Node(right).buildYearStart()
                    )
                    self.nodeElements.append(
                        ArchivePageContent.Node(right).buildMonthStart()
                    )
                    continue
                if left.createDate.month != right.createDate.month:
                    self.nodeElements.append(
                        ArchivePageContent.Node(left).buildMonthStop()
                    )
                    self.nodeElements.append(
                        ArchivePageContent.Node(right).buildMonthStart()
                    )

            except StopIteration:
                # the left pointers to the last one
                self.nodeElements.append(
                    ArchivePageContent.Node(first_element).buildMonthStop()
                )
                self.nodeElements.append(
                    ArchivePageContent.Node(first_element).buildYearStop()
                )
                break


@BlogUtils.timeit
def generate_archive_page():
    with open("./src/templates/archives.template.html", "r") as fp_in:
        open("./output/specs/archives.html", "w").write(
            fp_in.read().replace("<!-- CONTENTS -->", minify(str(ArchivePageContent())))
        )
        fp_in.close()
