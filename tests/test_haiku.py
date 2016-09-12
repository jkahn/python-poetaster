# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest

from poetaster.haiku import Haiku
from poetaster.haiku import NotHaiku

def assert_non_haiku(inp, message):
    """Utility function for non-haikus."""
    with pytest.raises(NotHaiku) as excinfo:
        Haiku.from_string(inp)
    assert message in excinfo.exconly()


def test_not_haiku():
    assert_non_haiku(77, "not a string type")
    assert_non_haiku("BBEFECEE CEFWEC EWRE CE RWEER",
                     "Could not tile string")
    assert_non_haiku("This is not a haiku.",
                     "No syllabification has 17 syllables")

    assert_non_haiku("This is not a haiku either", # eight
                     "No syllabification has 17 syllables")
