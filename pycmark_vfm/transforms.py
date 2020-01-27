"""
    pycmark_vfm.transforms
    ~~~~~~~~~~~~~~~~~~~~~~

    Transform classes for BlockParser.

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import Any

from docutils import nodes
from docutils.transforms import Transform
from pycmark.addnodes import linebreak


class HardlineBreakTransform(Transform):
    default_priority = 100

    def apply(self, **kwargs: Any) -> None:
        for node in self.document.traverse(nodes.paragraph):
            for text in node.traverse(nodes.Text):
                if '\n' in text:
                    parent = text.parent
                    pos = parent.index(text)
                    for line in reversed(text.splitlines()):
                        parent.insert(pos + 1, nodes.Text(line.rstrip("\n")))
                        parent.insert(pos + 1, linebreak())
                    parent.pop(pos + 1)
                    parent.remove(text)


class CodeBlockTitleTransform(Transform):
    default_priority = 200

    def apply(self, **kwargs: Any) -> None:
        for node in self.document.traverse(nodes.literal_block):
            for klass in node['classes'][:]:
                if klass.startswith('language-') and ':' in klass:
                    language, metadata = klass.split(':', 1)
                    node['classes'].remove(klass)
                    node['classes'].append(language)
                    self.update_metadata(node, metadata)

    def update_metadata(self, node: nodes.literal_block, metadata: str) -> None:
        if '=' in metadata:
            key, value = metadata.split('=')
            node[key] = value
        else:
            node['title'] = metadata
