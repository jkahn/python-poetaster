# -*- coding: utf-8 -*-
"""Construct lattice of tokenizations from provided dictionary of
string keys."""

from collections import defaultdict
from collections import Container
import re

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

    def all_paths(self, position=0, breadcrumbs=()):
        """Returns iterator over sequences of (begin, end) pairs that
        completely cover the target."""
        if position == self.end_sentinel:
            # Reached end.
            yield breadcrumbs
            return
        # Otherwise, recurse:
        for endpt in self._forward[position]:
            new_breadcrumbs = breadcrumbs + ((position, endpt),)
            for p in self.all_paths(position=endpt,
                                    breadcrumbs=new_breadcrumbs):
                yield p

    @property
    def token_paths(self):
        return tuple(self.path_to_tokens(p) for p in self.all_paths())


class RegexGazette(Container):
    def __init__(self, pattern):
        self._pattern = re.compile(pattern + r'$')
        # assert pattern is regex?

    def __contains__(self, thing):
        return self._pattern.match(thing)


class Lattice(BaseLattice):
    """Uses two containers to determine wat token sequences can be."""

    def __init__(self, st, keeper, discardable=tuple()):
        self._keeper = keeper  # assert compiled regex?
        self._discardable = discardable
        super(Lattice, self).__init__(st)

    def legal(self, start, end):
        s = self.substr(start, end)
        return s in self._keeper or s in self._discardable

    def contentful(self, start, end):
        s = self.substr(start, end)
        if s in self._discardable and s not in self._keeper:
            return False
        return True

    def path_to_tokens(self, path):
        return tuple(self.substr(b, e) for b, e in path
                     if self.contentful(b, e))
