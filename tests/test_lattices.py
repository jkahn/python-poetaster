# -*- coding: utf-8 -*-

from __future__ import print_function

from poetaster.lattice import AlternatingLattice
from poetaster.lattice import IslexOrthoLattice
from poetaster.lattice import Lattice
from poetaster.lattice import RegexGazette




def test_explorer():
    e = Lattice("a bc", admitter=frozenset(["a", " ", "d", "bc"]))
    assert e.admit(0, 1)
    assert e.string == "a bc"
    assert len(e.paths) == 1
    assert ("a", " ", "bc") in e.token_sequences


def test_ambiguous():

    l = Lattice("a bc", admitter=frozenset(("a", " ", "b", "c", "bc")))
    assert l
    assert  ("a", " ", "bc") in l.token_sequences
    assert  ("a", " ", "b", "c") in l.token_sequences
    assert len(l.paths) == 2


def test_longer_string():
    d = frozenset(("new", "york", " ", ".", "i", "love", "new york", "city"))
    l = Lattice("i love new york city.", admitter=d)
    assert l
    assert ("i", " ", "love", " ", "new york",
            " ", "city", ".") in l.token_sequences
    assert ("i", " ", "love", " ", "new", " ", "york",
            " ", "city", ".") in l.token_sequences


def test_discarding_gunge():
    keeper = frozenset(("city", "new york", "new", "i", "<3"))
    discardable = RegexGazette(r'[0-9<>\'",.?!:;\s ]+')
    s = "i <3 new york!"
    assert len(s) == 14
    assert "<3" in discardable
    assert "i" in keeper
    assert " " in discardable
    assert "<3" in keeper
    assert "new york" in keeper
    assert "!" in discardable
    l = AlternatingLattice(s, content_admitter=keeper,
                            spacing_admitter=discardable)
    # print (l.paths)
    assert ("i", "<3", "new york") in l.token_sequences


def test_transducer():
    keeper = {'a': "A", 'b': "b", 'c': "C"}
    s = "abc"
    l = Lattice(s, admitter=keeper)
    assert ("a", "b", "c") in l.token_sequences
    assert ("a", "b", "c") not in l.transductions
    assert ("A", "b", "C") in l.transductions
    assert len(l.transductions) == 1

def test_spacing_transducer():
    keeper = {'a': "A", 'b': "b", 'c': "C"}
    discardable = RegexGazette(r'[0-9<>\'",.?!:;\s]+')
    s = "a b c"
    l = AlternatingLattice(s, content_admitter=keeper,
                            spacing_admitter=discardable,
                            discard_spacers=True)
    assert ("a", "b", "c") in l.token_sequences
    assert ("a", "b", "c") not in l.transductions
    assert ("A", "b", "C") in l.transductions
    assert len(l.transductions) == 1


def test_multi_transducer():
    keeper = {'a': ["A", "a"], 'b': ["b"], 'c': ['c', 'C']}
    s = "abc"
    l = Lattice(s, admitter=keeper, multiple_transductions=True)
    assert ("a", "b", "c") in l.token_sequences
    assert ("a", "b", "c") in l.transductions
    assert ("A", "b", "C") in l.transductions
    assert ("A", "b", "c") in l.transductions
    assert ("a", "b", "C") in l.transductions


def test_islex_transducer():
    ilat = IslexOrthoLattice("help me now!")
    assert ilat.transductions
    assert len(ilat.transductions) == 1
    assert ('help', 'me', 'now') in ilat.retokenizations
    # Make sure alternating lattice is working right.
    assert ('he', 'l', 'p', 'me', 'now') not in ilat.retokenizations
    assert len(ilat.retokenizations) == 1

    assert len(ilat.pronunciations) == len(ilat.transductions)

    assert (tuple(len(p) for p in ilat.pronunciations)
            == tuple(len(t) for t in ilat.transductions))

    assert (u"hˈɛlp", u"mˈi", u"nˈaʊ") in ilat.ipa_syllabifications

def test_islex_explosion():
    lat = IslexOrthoLattice("This is not a haiku either.")
    assert len(lat.transductions) == 1
