# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest

from poetaster.haiku import Haiku
from poetaster.haiku import NotHaiku


def test_not_haiku():
    with pytest.raises(NotHaiku):
        Haiku.from_string("This is not a haiku.")


