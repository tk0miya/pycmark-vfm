"""
    pycmark_vfm.inlineparser.std_processors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Standard processor classes for InlineParser.

    :copyright: Copyright 2017-2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from docutils.nodes import Element
from pycmark.addnodes import bracket
from pycmark.inlineparser import PatternInlineProcessor
from pycmark.readers import TextReader
from pycmark.utils import ESCAPED_CHARS, transplant_nodes, unescape

from pycmark_vfm import addnodes


class RubyCloserProcessor(PatternInlineProcessor):
    pattern = re.compile(r'\]{(' + ESCAPED_CHARS + '|[^}])+}')
    priority = 200

    def run(self, reader: TextReader, document: Element) -> bool:
        brackets = list(n for n in document.children if isinstance(n, bracket))
        openers = list(d for d in brackets if d['can_open'])
        if openers == []:
            return False

        matched = reader.consume(self.pattern)
        rubytext = unescape(matched.group(0)[2:-1])
        ruby = addnodes.ruby(rubytext=rubytext)
        document += ruby

        # transplant ruby base text to ruby node
        transplant_nodes(document, ruby, start=openers[-1], end=ruby)
        document.remove(openers[-1])
        return True
