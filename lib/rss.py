#!/bin/python3

"""
The RSS generator
"""

from .metadata import BlogArticles
from .blog_utils import BlogUtils

from datetime import datetime

ARTICLE_TEMPLATE = """
<item>
    <title>{TITLE}</title>
    <link>{LINK}</link>
    <pubDate>{PUBDATE}</pubDate>
    <guid>{LINK}</guid>
    <description>{DESCRIPTION}</description>
</item>
""".strip()

RSS_TEMPLATE = """
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>izfsk的博客</title>
        <link>https://izfsk-ium.github.io/</link>
        <description>Recent content on izfsk's blog</description>
        <generator>bash scripts, python scripts and love</generator>
        <copyright>Licensed under CC BY-NC-SA 2.5 CN</copyright>
        <lastBuildDate>{LASTCHILD}</lastBuildDate>
        <atom:link href="https://izfsk-ium.github.io/rss.xml" rel="self" type="application/rss+xml" />
        {ITEMS}
    </channel>
</rss>
""".strip()


@BlogUtils.timeit
def generate_rss_page():
    result = ""
    for article in BlogArticles().getAllArticleMetadata():
        result += ARTICLE_TEMPLATE.format(
            TITLE=article.title,
            LINK=f"https://izfsk-ium.github.io/articles/{article.title}/index.html",
            PUBDATE=article.createDate.__str__(),
            DESCRIPTION=str(article.description.replace("<", "\\<")),
        )
    with open("./output/rss.xml", "w") as fp_in:
        fp_in.write(
            RSS_TEMPLATE.format(ITEMS=result, LASTCHILD=datetime.now().__str__())
        )
        fp_in.flush()
        fp_in.close()
