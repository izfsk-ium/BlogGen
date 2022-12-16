#!/bin/python3

"""
Generate file system page
"""

#!/bin/python3

# generate fs page

from datetime import datetime
from htmlmin import minify
from magic import from_file
from hashlib import sha224
from os.path import getsize, getmtime
from os import listdir

from .blog_utils import BlogUtils

FILE_ITEM_TEMPLATE = """
<tr>
    <td class="filename"><a href="{LINK}" download="{NAME}">⬇</a>
        {NAME}
    </td>
    <td>
        {SIZE}
    </td>
    <td>
        {TIME}
    </td>
    <td>
        {TYPE}
    </td>
    <td class="sha">
        {SHA224}
    </td>
</tr>
"""


def get_size_in_good_formate(file_path, isFile=True):
    if isFile:
        value = getsize(file_path)
    else:
        value = file_path
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size


@BlogUtils.timeit
def generate_file_page():
    buff_files_html = ""
    total_file_size, total_file_count = 0, 0
    for file in listdir("./src/fs"):
        file_path = "./src/fs/" + file
        total_file_count += 1
        total_file_size += getsize(file_path)
        hash = sha224()
        with open(file_path, "rb") as fp:
            for buff in iter(lambda: fp.read(8192), b""):
                hash.update(buff)

        buff_files_html += FILE_ITEM_TEMPLATE.format(
            LINK="/fs/{name}".format(name=file),
            NAME=file,
            SIZE=get_size_in_good_formate(file_path),
            TIME=datetime.fromtimestamp(getmtime(file_path)).__str__()[:19],
            TYPE=from_file(file_path, mime=True),
            SHA224=hash.hexdigest(),
        )

    open("./output/specs/fs.html", "w").write(
        minify(
            open("./src/templates/fs.template.html")
            .read()
            .replace("<!--FILES-->", buff_files_html)
            .replace(
                "<!--SUMMARY-->",
                "<br/>\nTotal {size}, {count} files.".format(
                    size=get_size_in_good_formate(total_file_size, isFile=False),
                    count=total_file_count,
                ),
            )
        )
    )
