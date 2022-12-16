#!/bin/python3

"""
Generate Category page
"""

from .metadata import BlogArticles
from .blog_utils import BlogUtils

from itertools import groupby
from htmlmin import minify


class CategoryPage:
    def __init__(self) -> None:
        self.all_articles = sorted(
            BlogArticles().getAllArticleMetadata(), key=lambda x: x.category
        )

    def generate_html_content(self) -> str:
        categories_html = (
            f"<small>Total {len(self.all_articles)} articles.</small>\n<ul><ul>"
        )
        for key, group in groupby(self.all_articles, key=lambda x: x.category.strip()):
            categories_html += str(
                f"""
                <li class="l1">{key}</li><ul>
                """
            )
            for entry in group:
                categories_html += str(
                    f"""
                        <li target="{entry.uuid}">
                            <div>
                                <a href="/articles/{entry.title}/index.html">{entry.title}</a><br/>
                                <span style="font-size:14px">
                                    Created: {entry.createDate.strftime("%Y-%m-%d，%H:%M:%S")}
                                </span>
                            </div>
                        </li>
                    """
                )
            categories_html += "</ul>"
        categories_html += "</ul></ul>"
        return categories_html

    def save_file(self) -> None:
        open("./output//specs/categories.html", "w").write(
            minify(
                open("./src/templates/categories.template.html")
                .read()
                .replace("<!-- CONTENT -->", self.generate_html_content())
            )
        )


@BlogUtils.timeit
def generate_category_page() -> None:
    CategoryPage().save_file()
