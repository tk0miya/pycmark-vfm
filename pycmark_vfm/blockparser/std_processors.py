"""
    pycmark_vfm.blockparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A parser for block elements.

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from docutils import nodes
from docutils.nodes import Element
from pycmark.blockparser import PatternBlockProcessor
from pycmark.readers import LineReader


class FrontmatterProcessor(PatternBlockProcessor):
    priority = 100
    paragraph_interruptable = False
    pattern = re.compile(r'^ {0,3}\-{3,}\s*$')

    def run(self, reader: LineReader, document: Element) -> bool:
        if reader.lineno != 0:
            return False

        reader.readline()
        field_list = nodes.field_list()
        field_list.source, field_list.line = reader.get_source_and_line()
        for line in reader:
            if self.pattern.match(line):
                break
            elif ':' in line:
                key, value = line.split(':')
                field_name = nodes.field_name('', key.strip())
                field_body = nodes.field_body('', nodes.paragraph('', value.strip()))
                field_list += nodes.field('', field_name, field_body)
            else:
                # Not a frontmatter, rollback
                lines = len(field_list) + 2
                reader.step(-lines)
                return False

        document += field_list
        return True
