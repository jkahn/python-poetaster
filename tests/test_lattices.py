# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest

from poetaster.lattice import BaseLattice
from poetaster.lattice import IslexOrthoLattice
from poetaster.lattice import Lattice
from poetaster.lattice import MultiLattice
from poetaster.lattice import RegexGazette


def test_abc():
    with pytest.raises(NotImplementedError):
        BaseLattice("This can't be instantiated")


def test_lattice():

    l = Lattice("a bc", keeper=frozenset(("a", " ", "d", "bc")))
    assert l
    assert  ("a", " ", "bc") in l.token_sequences
    assert len(l.paths) == 1


def test_ambiguous():

    l = Lattice("a bc", keeper=frozenset(("a", " ", "b", "c", "bc")))
    assert l
    assert  ("a", " ", "bc") in l.token_sequences
    assert  ("a", " ", "b", "c") in l.token_sequences
    assert len(l.paths) == 2

def test_longer_string():
    d = frozenset(("new", "york", " ", ".", "i", "love", "new york", "city"))
    l = Lattice("i love new york city.", keeper=d)
    assert l
    assert ("i", " ", "love", " ", "new york",
            " ", "city", ".") in l.token_sequences
    assert ("i", " ", "love", " ", "new", " ", "york",
            " ", "city", ".") in l.token_sequences


def test_discarding_gunge():
    keeper = frozenset(("city", "new york", "new", "i", "<3"))
    discardable = RegexGazette(r'[0-9<>\'",.?!:;\s]+')
    s = "i <3 new york!"
    assert len(s) == 14
    assert "<3" in discardable
    assert "i" in keeper
    assert " " in discardable
    assert "<3" in keeper
    assert "new york" in keeper
    assert "!" in discardable
    l = Lattice(s, keeper=keeper, discardable=discardable)
    assert l.end_sentinel == len(s)
    # print (l.paths)
    assert ("i", "<3", "new york") in l.token_sequences


def test_transducer():
    keeper = {'a': "A", 'b': "b", 'c': "C"}
    discardable = RegexGazette(r'[0-9<>\'",.?!:;\s]+')
    s = "a b c"
    l = Lattice(s, keeper=keeper, discardable=discardable)
    assert ("a", "b", "c") in l.token_sequences
    assert ("a", "b", "c") not in l.transductions
    assert ("A", "b", "C") in l.transductions
    assert len(l.transductions) == 1


def test_multi_transducer():
    keeper = {'a': ["A", "a"], 'b': ["b"], 'c': ['c', 'C']}
    discardable = RegexGazette(r'[0-9<>\'",.?!:;\s]+')
    s = "a b c"
    l = MultiLattice(s, keeper=keeper, discardable=discardable)
    assert ("a", "b", "c") in l.token_sequences
    assert ("a", "b", "c") in l.transductions
    assert ("A", "b", "C") in l.transductions
    assert ("A", "b", "c") in l.transductions
    assert ("a", "b", "C") in l.transductions


def test_islex_transducer():
    ilat = IslexOrthoLattice("help me now!")
    assert ilat.transductions
    assert len(ilat.transductions) == 2
    assert ('help', 'me', 'now') in ilat.retokenizations
    assert ('he', 'l', 'p', 'me', 'now') in ilat.retokenizations
    assert len(ilat.retokenizations) == 2
    # FIXME: "he l p me now" not acceptable...

    assert len(ilat.pronunciations) == len(ilat.transductions)

    assert (tuple(len(p) for p in ilat.pronunciations)
            == tuple(len(t) for t in ilat.transductions))

    assert (u"hˈɛlp", u"mˈi", u"nˈaʊ") in ilat.ipa_syllabifications

@pytest.mark.xfail
def test_islex_explosion():
    lat = IslexOrthoLattice("This is not a haiku either")
    assert len(lat.transductions) < 40
    print([t.retokenization for t in lat.transductions])
