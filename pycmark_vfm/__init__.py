"""
    pycmark_vfm
    ~~~~~~~~~~~

    Vivliostyle Flavored Markdown parser for docutils.

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import List, Type

from docutils import nodes
from docutils.transforms import Transform
from pycmark import CommonMarkParser
from pycmark.blockparser import BlockProcessor
from pycmark.inlineparser import InlineProcessor
from pycmark.readers import LineReader


class VFMParser(CommonMarkParser):
    """Vivliostyle Flavored Markdown parser for docutils."""

    supported = ('markdown', 'md')

    def get_block_processors(self) -> List[Type[BlockProcessor]]:
        """Returns block processors. Overrided by subclasses."""
        processors = super().get_block_processors()
        return processors

    def get_inline_processors(self) -> List[Type[InlineProcessor]]:
        """Returns inline processors. Overrided by subclasses."""
        processors = super().get_inline_processors()
        return processors

    def get_transforms(self) -> List[Type[Transform]]:
        transforms = super().get_transforms()
        return transforms

    def parse(self, inputtext: str, document: nodes.document) -> None:
        """Parses a text and build document."""
        document.settings.inline_processors = self.get_inline_processors()
        reader = LineReader(inputtext.splitlines(True), source=document['source'])
        block_parser = self.create_block_parser()
        block_parser.parse(reader, document)
