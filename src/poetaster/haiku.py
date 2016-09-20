# -*- coding: utf-8 -*-
"""Detects (and formats?) haiku in input strings."""
import six
from poetaster.lattice import IslexOrthoLattice
from poetaster.lattice import SegmentationError


class NotHaiku(ValueError):
    """Error class indicating that input string was not a haiku (and why)."""
    # Hmmmm.  should this be a subclass of StopIteration?
    pass


class Haiku(object):
    """Core components of a haiku."""
    @classmethod
    def from_transduction(cls, t, s):
        """Returns haiku (or None) given transduction and string."""
        lines = []
        for b, e in ((0, 5), (5, 12), (12, 17)):
            try:
                lines.append(t.syllable_range(b, e))
            except SegmentationError:
                return None  # No word break at appropriate syll boundary
        if t.syllable_count != 17:
            return None
        return cls(s, t, _lines=lines)

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

        haikus = []
        for t in transductions:
            h = cls.from_transduction(t, s)
            if h:
                haikus.append(h)

        if not haikus:
            raise NotHaiku("No syllabification has 17 syllables (found %s)"
                           % [t.syllable_count for t in transductions])

        return haikus

    def __init__(self, raw, transduction, _lines=None):
        self.raw = raw
        self.transduction = transduction
        self._lines = _lines

    @property
    def lines(self):
        if not self._lines:
            # extract lines
            self._lines = [self.transduction.syllable_range(b, e)
                           for b, e in ((0, 5), (5, 12), (12, 17))]
        return self._lines

    @property
    def formatted(self):
        line_tokens = (l.retokenization for l in self.lines)
        lines = (' '.join(ws) for ws in line_tokens)
        return "\n".join(s.capitalize() for s in lines)
