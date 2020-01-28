"""
    test_vfm
    ~~~~~~~~

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from pycmark.addnodes import linebreak

from pycmark_vfm.addnodes import ruby
from utils import assert_node, publish


def test_VFM():
    text = ("はじめまして。\n"
            "\n"
            "Vivliostyle Flavored Markdown（略して VFM）の世界へようこそ。\n"
            "VFM は出版物の執筆に適した Markdown 方言であり、Vivliostyle プロジェクトのために策定・実装されました。\n")
    result = publish(text)
    assert_node(result,
                ([nodes.paragraph, "はじめまして。"],
                 [nodes.paragraph, ("Vivliostyle Flavored Markdown（略して VFM）の世界へようこそ。",
                                    linebreak,
                                    "VFM は出版物の執筆に適した Markdown 方言であり、Vivliostyle プロジェクトのために策定・実装されました。")]))


def test_Heading():
    text = ("# Heading 1\n"
            "\n"
            "## Heading 2\n"
            "\n"
            "### Heading 3\n"
            "\n"
            "#### Heading 4\n"
            "\n"
            "##### Heading 5\n"
            "\n"
            "###### Heading 6\n")
    result = publish(text)
    assert_node(result,
                ([nodes.section, ([nodes.title, "Heading 1"],
                                  [nodes.section, ([nodes.title, "Heading 2"],
                                                   [nodes.section, ([nodes.title, "Heading 3"],
                                                                    nodes.section)])])],))
    assert_node(result[0][1][1][1],
                [nodes.section, ([nodes.title, "Heading 4"],
                                 [nodes.section, ([nodes.title, "Heading 5"],
                                                  [nodes.section, nodes.title, "Heading 6"])])])


def test_Code():
    text = ("```javascript:app.js\n"
            "function main() {}\n"
            "```\n")
    result = publish(text)
    assert_node(result, ([nodes.literal_block, "function main() {}\n"],))
    assert_node(result[0], nodes.literal_block, classes=["code", "language-javascript"], title="app.js")


def test_Code_Dictionary_style_metadata():
    text = ("```javascript:title=app.js\n"
            "function main() {}\n"
            "```\n")
    result = publish(text)
    assert_node(result, ([nodes.literal_block, "function main() {}\n"],))
    assert_node(result[0], nodes.literal_block, classes=["code", "language-javascript"], title="app.js")


def test_Ruby():
    text = ("This is [Ruby]{ルビ}")
    result = publish(text)
    assert_node(result, ([nodes.paragraph, ("This is ",
                                            [ruby, "Ruby"])],))
    assert_node(result[0][1], ruby, rubytext="ルビ")


def test_Image():
    text = ("![Figure 1](./fig1.png)")
    result = publish(text)
    assert_node(result, ([nodes.paragraph, nodes.image],))
    assert_node(result[0][0], nodes.image, uri="./fig1.png", alt="Figure 1")


def test_Walled_block():
    text = ("===section-author\n"
            "uetchy\n"
            "===\n")
    result = publish(text)
    assert_node(result, ([nodes.container, nodes.paragraph, "uetchy"],))
    assert_node(result[0], nodes.container, classes=["section-author"])


def test_nested_Walled_block():
    text = ("===section-author\n"
            "uetchy\n"
            "====author-homepage\n"
            "<https://uechi.io>\n"
            "====\n"
            "===\n")
    result = publish(text)
    assert_node(result,
                ([nodes.container, ([nodes.paragraph, "uetchy"],
                                    [nodes.container, nodes.paragraph, nodes.reference, "https://uechi.io"])],))
    assert_node(result[0], nodes.container, classes=['section-author'])
    assert_node(result[0][1], nodes.container, classes=['author-homepage'])


def test_CustomHTML():
    text = ('<div class="custom">\n'
            '  <p>Hey</p>\n'
            '</div>\n')
    result = publish(text)
    assert_node(result, ([nodes.raw, text],))
    assert_node(result[0], nodes.raw, format='html')


def test_Frontmatter():
    text = ("---\n"
            "title: Introduction to VFM\n"
            "---\n")
    result = publish(text)
    assert_node(result,
                ([nodes.field_list, nodes.field, ([nodes.field_name, "title"],
                                                  [nodes.field_body, nodes.paragraph, "Introduction to VFM"])],))
