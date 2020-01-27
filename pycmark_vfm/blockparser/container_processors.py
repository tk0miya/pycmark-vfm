"""
    pycmark_vfm.blockparser.container_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Container processor classes for BlockParser.

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from docutils import nodes
from docutils.nodes import Element
from pycmark.blockparser import PatternBlockProcessor
from pycmark.readers import LineReader

from pycmark_vfm.readers import WalledBlockReader


class WalledBlockProcessor(PatternBlockProcessor):
    priority = 500
    paragraph_interruptable = True
    pattern = re.compile(r'^ {0,3}={3,}\s*[^=]+')

    def run(self, reader: LineReader, document: Element) -> bool:
        line = reader.readline()
        klass = line.strip().strip('=').strip()
        container = nodes.container(classes=[klass])
        container.source, container.line = reader.get_source_and_line()
        document += container

        walled_block_reader = WalledBlockReader(reader)
        self.parser.parse(walled_block_reader, container)
        walled_block_reader.consume_endmarker()
        return True
