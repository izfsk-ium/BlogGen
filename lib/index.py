#!/bin/python3

"""
Generate index html
"""

from .metadata import BlogArticles
from .blog_utils import BlogUtils

from datetime import datetime
from htmlmin import minify


class IndexPageContent:
    def __init__(self) -> None:
        self.recent_posts = sorted(
            [
                i
                for i in BlogArticles().getAllArticleMetadata()
                if not i.isDraft and not i.isOutdated
            ],
            key=lambda x: x.createDate.timestamp(),
            reverse=True,
        )[:5]
        self.meta_info_html = ""
        self.recent_posts_html = ""

    def generate_meta_info(self):
        self.meta_info_html = (
            f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        )
        return self

    def generate_recent_posts(self):
        recent_posts_html = ""
        for i in self.recent_posts:
            recent_posts_html += f"""
                <li>
                    <span>{i.createDate.strftime("%Y-%m-%d")}</span>
                    <a href="/articles/{i.title}/index.html">{i.title}</a>
                </li>
            """
        self.recent_posts_html = recent_posts_html
        return self

    def save_file(self):
        open("./output/index.html", "w").write(
            minify(
                open("./src/templates/index.template.html")
                .read()
                .replace("<!-- RECENT_POSTS -->", self.recent_posts_html)
                .replace("<!-- GENERATE INFO -->", self.meta_info_html),
            )
        )


@BlogUtils.timeit
def generate_index_page() -> None:
    IndexPageContent().generate_meta_info().generate_recent_posts().save_file()
