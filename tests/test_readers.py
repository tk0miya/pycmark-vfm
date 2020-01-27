"""
    test_readers
    ~~~~~~~~~~~~

    :copyright: Copyright 2020 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from pycmark.readers import LineReader

from pycmark_vfm.readers import WalledBlockReader


def test_WalledBlockReader():
    text = ("===wall\n"
            "Lorem ipsum dolor sit amet, \n"
            "consectetur adipiscing elit, \n"
            "\n"
            "=====nested_wall\n"
            "    sed do eiusmod tempor incididunt \n"
            "    ut labore et dolore magna aliqua.\n"
            "===\n"
            "\n"
            "===\n"
            "Ut enim ad minim veniam, quis nostrud")

    reader = LineReader(text.splitlines(True), source='dummy.md')
    assert reader.readline() == "===wall\n"

    walled_block_reader = WalledBlockReader(reader)
    assert walled_block_reader.eof() is False
    assert walled_block_reader.get_source_and_line() == ('dummy.md', 1)

    # read first line
    assert walled_block_reader.readline() == "Lorem ipsum dolor sit amet, \n"
    assert walled_block_reader.current_line == "Lorem ipsum dolor sit amet, \n"
    assert walled_block_reader.fetch() == "Lorem ipsum dolor sit amet, \n"
    assert walled_block_reader.get_source_and_line() == ('dummy.md', 2)

    # read consequence lines
    assert walled_block_reader.readline() == "consectetur adipiscing elit, \n"
    assert walled_block_reader.readline() == "\n"
    assert walled_block_reader.readline() == "=====nested_wall\n"

    # nested WalledBlockReader
    nested_wbreader = WalledBlockReader(walled_block_reader)
    assert nested_wbreader.readline() == "    sed do eiusmod tempor incididunt \n"
    assert nested_wbreader.readline() == "    ut labore et dolore magna aliqua.\n"

    # reach the end of the nested block
    assert nested_wbreader.eof() is True
    try:
        nested_wbreader.readline()
        assert False
    except IOError:
        pass

    # read consequence lines by parent reader
    nested_wbreader.consume_endmarker()
    assert walled_block_reader.readline() == "\n"

    # reach the end of the parent block
    assert walled_block_reader.eof() is True
    try:
        walled_block_reader.readline()
        assert False
    except IOError:
        pass

    walled_block_reader.consume_endmarker()
    assert reader.readline() == "Ut enim ad minim veniam, quis nostrud"
