"""
    pycmark_vfm.addnodes
    ~~~~~~~~~~~~~~~~~~~~

    Additional docutils nodes for pycmark-vfm.

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from docutils.nodes import Inline, TextElement


class ruby(Inline, TextElement):
    pass
