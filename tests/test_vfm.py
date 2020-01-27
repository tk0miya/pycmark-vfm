"""
    test_vfm
    ~~~~~~~~

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils import nodes
from pycmark.addnodes import linebreak

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
