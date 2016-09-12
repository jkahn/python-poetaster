# -*- coding: utf-8 -*-
"""Detects (and formats?) haiku in input strings."""
import six
from poetaster.lattice import IslexOrthoLattice


class NotHaiku(ValueError):
    """Error class indicating that input string was not a haiku (and why)."""
    # Hmmmm.  should this be a subclass of StopIteration?
    pass


class Haiku(object):
    """Core components of a haiku."""
    @classmethod
    def from_string(cls, s):
        """Returns list of all Haiku transductions possible.  If no
        arrangement is possible, raise NotHaiku exception.
        """
        # Check that a string is given.
        if not isinstance(s, six.string_types):
            raise NotHaiku("Input object %r not a string type" % s)

        latt = IslexOrthoLattice(s)

        transductions = latt.transductions

        if not len(transductions):
            raise NotHaiku("Could not tile string with ortho representations.")

        haikus = [cls(s, t) for t in transductions if t.syllable_count == 17]

        if not haikus:
            raise NotHaiku("No syllabification has 17 syllables (found %s)"
                           % [t.syllable_count for t in transductions])
        return haikus

    def __init__(self, raw, transduction):
        self.raw = raw
        self.transduction = transduction
