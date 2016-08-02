# -*- coding: utf-8 -*-
import re

import pytest

from poetaster.lattice import BaseLattice
from poetaster.lattice import Lattice
from poetaster.lattice import RegexGazette


def test_abc():
    with pytest.raises(NotImplementedError):
        BaseLattice("This can't be instantiated")


def test_lattice():

    l = Lattice("a bc", keeper=frozenset(("a", " ", "d", "bc")))
    assert l
    assert  ("a", " ", "bc") in l.token_paths
    assert len(l.token_paths) == 1


def test_ambiguous():

    l = Lattice("a bc", keeper=frozenset(("a", " ", "b", "c", "bc")))
    assert l
    assert  ("a", " ", "bc") in l.token_paths
    assert  ("a", " ", "b", "c") in l.token_paths
    assert len(l.token_paths) == 2

def test_longer_string():
    d = frozenset(("new", "york", " ", ".", "i", "love", "new york", "city"))
    l = Lattice("i love new york city.", keeper=d)
    assert l
    assert ("i", " ", "love", " ", "new york",
            " ", "city", ".") in l.token_paths
    assert ("i", " ", "love", " ", "new", " ", "york",
            " ", "city", ".") in l.token_paths


def test_discarding_gunge():
    d = frozenset(("city", "new york", "new", "i", "<3"))
    discardable = RegexGazette(r'[0-9<>\'",.?!:;\s]+')
    s = "i <3 new york!"
    l = Lattice(s, keeper=d, discardable=discardable)
    assert ("i", "<3", "new york") in l.token_paths
