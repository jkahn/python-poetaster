# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest

from six import string_types

from poetaster.haiku import Haiku
from poetaster.haiku import NotHaiku
from poetaster.lattice import Transduction

def assert_non_haiku(inp, message):
    """Utility function for non-haikus."""
    with pytest.raises(NotHaiku) as excinfo:
        Haiku.from_string(inp)
    assert message in excinfo.exconly()


def assert_haiku(inp):
    haikus = Haiku.from_string(inp)
    for h in haikus:
        assert isinstance(h, Haiku)
    assert len(haikus)
    return haikus

def test_not_haiku():
    assert_non_haiku(77, "not a string type")
    assert_non_haiku("BBEFECEE CEFWEC EWRE CE RWEER",
                     "Could not tile string")
    assert_non_haiku("This is not a haiku.",
                     "No syllabification has 17 syllables")

    assert_non_haiku("This is not a haiku either", # eight
                     "No syllabification has 17 syllables")

    assert_non_haiku("This long utterance is much, "  # seven
                     "much too long for a haiku "  # seven
                     "but that will not stop me from trying",  # nine
                     "No syllabification has 17 syllables")

TEST_HAIKU = (
    "The autumn leaves fall "  # five
    "gently into my basket "  # seven
    "how I knew them green."  # five
)

TARGET = """\
The autumn leaves fall
Gently into my basket
How i knew them green"""

def test_haikus():
    haikus = assert_haiku(TEST_HAIKU)
    assert len(haikus) == 1


def test_format_haiku():
    haiku = assert_haiku(TEST_HAIKU)[0]
    assert len(haiku.lines) == 3
    for l in haiku.lines:
        assert isinstance(l, Transduction)

    assert tuple(l.syllable_count for l in haiku.lines) == (5, 7, 5)

    assert tuple(l.retokenization for l in haiku.lines) == (
        ("the", "autumn", "leaves", "fall"),
        ("gently", "into", "my", "basket"),
        ("how", "i", "knew", "them", "green")
    )

    assert isinstance(haiku.formatted, string_types)
    assert haiku.formatted == TARGET
