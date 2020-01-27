"""
    pycmark_vfm.readers
    ~~~~~~~~~~~~~~~~~~~

    Vivliostyle Flavored Markdown readers for docutils.

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

import re

from pycmark.readers import LineReaderDecorator


class WalledBlockReader(LineReaderDecorator):
    """A reader for walled blocks."""
    pattern = re.compile(r'^ {0,3}={3,}\s*$')

    def fetch(self, relative: int = 0, **kwargs) -> str:
        """Returns a line until the end of walled block."""
        line = self.reader.fetch(relative, **kwargs)
        if kwargs.get('allow_endmarker') is True:
            return line
        elif self.pattern.match(line):
            raise IOError
        else:
            return line

    def consume_endmarker(self) -> None:
        """Consumes the end marker of wall block."""
        line = self.fetch(1, allow_endmarker=True)
        if self.pattern.match(line):
            self.step(1)
