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
        """Returns iterator over all Haiku transductions possible.  If no
        arrangement is possible, raise NotHaiku exception.
        """
        # Check that a string is given.
        if not isinstance(s, six.string_types):
            raise NotHaiku("Input object %r not a string type" % s)

        latt = IslexOrthoLattice(s)

        transductions = latt.transductions

        if not transductions:
            raise NotHaiku("Could not tile string with ortho representations.")

        num_yielded = 0
        for t in transductions:
            if t.syllable_count == 17:
                yield cls(t)
                num_yielded += 1

        if not num_yielded:
            raise NotHaiku("No syllabification has 17 syllables (found %s)"
                           % [t.syllable_count for t in transductions])

    def __init__(self, transduction):
        self.transduction = transduction
