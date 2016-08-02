# -*- coding: utf-8 -*-
import pytest

from poetaster.lattice import BaseLattice
from poetaster.lattice import DictionaryLattice


def test_abc():
    with pytest.raises(NotImplementedError):
        BaseLattice("This can't be instantiated")


def test_lattice():

    l = DictionaryLattice("a bc", {k:True for k in ("a", " ", "d", "bc")})
    assert l
    assert  ("a", " ", "bc") in l.token_paths
    assert len(l.token_paths) == 1


def test_ambiguous():

    l = DictionaryLattice("a bc", {k:True for k in ("a", " ", "b", "c", "bc")})
    assert l
    assert  ("a", " ", "bc") in l.token_paths
    assert  ("a", " ", "b", "c") in l.token_paths
    assert len(l.token_paths) == 2

def test_longer_string():
    d = {k:True
         for k in ("new", "york", " ", ".", "i", "love", "new york", "city")}
    l = DictionaryLattice("i love new york city.", dct=d)
    assert l
    assert ("i", " ", "love", " ", "new york",
            " ", "city", ".") in l.token_paths
    assert ("i", " ", "love", " ", "new", " ", "york",
            " ", "city", ".") in l.token_paths
