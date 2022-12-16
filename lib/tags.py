#!/bin/python3

"""
Generate tags page
"""

from .metadata import BlogArticles, ArticleMetaData
from .blog_utils import BlogUtils

from htmlmin import minify
from itertools import chain


class TagPage:
    def __init__(self) -> None:
        self.data: dict[str, list[ArticleMetaData]] = {
            tag: [x for x in BlogArticles().getAllArticleMetadata() if tag in x.tags]
            for tag in set(
                list(
                    chain.from_iterable(
                        [i.tags for i in BlogArticles().getAllArticleMetadata()]
                    )
                )
            )
        }

    def generate_html(self) -> str:
        result: str = f"<small>Total {len(self.data.keys())} tags.</small><ul>"
        for tag, items in self.data.items():
            result += f'<details><summary class="l1">➦{tag}({len(items)})</summary><ul>'
            for article in items:
                result += str(
                    f"""
                    <li>
                        <a href="/articles/{article.title}/index.html">{article.title}</a>
                    </li>
                    """
                )
            result += "</ul></details>"
        result += "</ul>"
        return result

    def save_file(self) -> None:
        open("./output/specs/tags.html", "w").write(
            minify(
                open("./src/templates/tags.template.html")
                .read()
                .replace("<!-- CONTENT -->", self.generate_html())
            )
        )


@BlogUtils.timeit
def generate_tags_page():
    TagPage().save_file()
