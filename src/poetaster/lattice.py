# -*- coding: utf-8 -*-
"""Construct lattice of tokenizations from provided dictionary of
string keys."""
from __future__ import print_function

import re
from collections import Container
from collections import defaultdict


class BaseLattice(object):
    """DAG of analyses, where every arc comes from provided dictionary.

    Initial implementation operates naively over substrings.
    """
    def __init__(self, st):
        self._st = st
        self._forward, self._backward = self._explore()

    def _explore(self, max_len=15):
        sizes = range(1, max_len+1)  # or compute from dictionary
        explored = set()
        frontier = set([0])
        viable = defaultdict(list)
        backlinks = defaultdict(list)
        while frontier:
            start = max(frontier)
            frontier.discard(start)
            explored.add(start)
            for l in sizes:
                end = start + l
                if end > self.end_sentinel:
                    break
                if self.legal(start, end):
                    viable[start].append(end)
                    backlinks[end].append(start)
                    if end < len(self._st) and end not in explored:
                        frontier.add(end)
        return (viable, backlinks)

    def legal(self, start, end):
        """Could the sequence from start to end be a legal token?"""
        raise NotImplementedError("Base class has not implemented legal()")

    @property
    def end_sentinel(self):
        return len(self._st)

    def substr(self, start, end):
        return self._st[start:end]

    @property
    def paths(self):
        return tuple(self._all_paths(position=0, past_decorations=()))

    @property
    def token_sequences(self):
        """iterable over tokenizations."""
        return tuple(tuple(self.substr(b, e) for b, e in path)
                     for path in self.paths)

    def _all_paths(self, position, past_decorations):
        """Returns iterator over sequences of (begin, end) pairs that
        completely cover the target."""
        for endpt in self._forward[position]:
            decorations = past_decorations + ((position, endpt),)
            if endpt == self.end_sentinel:
                yield decorations
            else:
                for p in self._all_paths(
                        position=endpt,
                        past_decorations=decorations):
                        yield p


class RegexGazette(Container):
    def __init__(self, pattern):
        self._pattern = re.compile(pattern + r'$')
        # assert pattern is regex?

    def __contains__(self, thing):
        return self._pattern.match(thing)


class Lattice(BaseLattice):
    """Uses two containers to determine what token sequences can be."""

    def __init__(self, st, keeper, discardable=tuple()):
        self._keeper = keeper  # assert compiled regex?
        self._discardable = discardable
        super(Lattice, self).__init__(st)

    def legal(self, start, end):
        s = self.substr(start, end)
        return s in self._keeper or s in self._discardable

    def _clean_paths(self, paths):
        """Override superclass; only return paths that delimit contentful."""
        _sent = set()
        for path in paths:
            clean = tuple((b, e) for b, e in path if self.contentful(b, e))
            if clean not in _sent:
                yield clean
                _sent.add(clean)

    @property
    def paths(self):
        return list(self._clean_paths(super(Lattice, self).paths))

    def contentful(self, start, end):
        s = self.substr(start, end)
        if s in self._discardable and s not in self._keeper:
            return False
        return True
