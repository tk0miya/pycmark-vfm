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

from pycmark_vfm.blockparser.container_processors import WalledBlockProcessor
from pycmark_vfm.blockparser.std_processors import FrontmatterProcessor
from pycmark_vfm.transforms import (
    CodeBlockTitleTransform,
    HardlineBreakTransform,
)


class VFMParser(CommonMarkParser):
    """Vivliostyle Flavored Markdown parser for docutils."""

    supported = ('markdown', 'md')

    def get_block_processors(self) -> List[Type[BlockProcessor]]:
        """Returns block processors. Overrided by subclasses."""
        processors = super().get_block_processors()
        processors.append(FrontmatterProcessor)
        processors.append(WalledBlockProcessor)
        return processors

    def get_inline_processors(self) -> List[Type[InlineProcessor]]:
        """Returns inline processors. Overrided by subclasses."""
        processors = super().get_inline_processors()
        return processors

    def get_transforms(self) -> List[Type[Transform]]:
        transforms = super().get_transforms()
        transforms.append(CodeBlockTitleTransform)
        transforms.append(HardlineBreakTransform)
        return transforms

    def parse(self, inputtext: str, document: nodes.document) -> None:
        """Parses a text and build document."""
        document.settings.inline_processors = self.get_inline_processors()
        reader = LineReader(inputtext.splitlines(True), source=document['source'])
        block_parser = self.create_block_parser()
        block_parser.parse(reader, document)
