# -*- coding: utf-8 -*-
"""Construct lattice of tokenizations from provided dictionary of
string keys."""
from __future__ import print_function

import itertools
import re

from collections import Container
from collections import Mapping
from collections import Sequence
from collections import defaultdict


import islex.data.core
import islex.load


def _traverse_reachable(paths, start):
    """Returns set of all paths reachable from point."""
    s = set([start])
    for target in paths[start]:
        s.update(_traverse_reachable(paths, target))
    return s


class BaseLattice(object):
    def __init__(self, string, multiple_transductions=False,
                 max_len=15):
        self.sizes = range(1, max_len + 1)
        self.string = string
        self.explored = set()
        self.frontier = set([0])
        self.forward = defaultdict(list)
        self.backward = defaultdict(list)
        self.multiple_transductions = multiple_transductions

        while self.frontier:
            start = min(self.frontier)
            self.frontier.discard(start)
            self.explore_at(start)
        self.prune()

    def admit(self, start, end):
        """Subclasses make different choices about whether to admit.
        Returning True means "this range is possible".  Base class
        keeps track of paths that can be admitted.
        """
        raise NotImplementedError

    def transduce(self, start, end):
        """Subclasses make different decisions about what to return in
        transduction.  Implementations should return a list of
        possible transductions for this range.
        """
        raise NotImplementedError

    def consider(self, start, end):
        if self.admit(start, end):
            self.forward[start].append(end)
            self.backward[end].append(start)
            return True
        return False

    def explore_at(self, start):
        for l in self.sizes:
            end = start + l
            if end > len(self.string):
                break
            if self.consider(start, end):
                if end < len(self.string) and end not in self.explored:
                    self.frontier.add(end)
        self.explored.add(start)

    def prune(self):
        """Removes links for those links that do not participate in full
        coverage.
        """
        back_reachable = _traverse_reachable(self.backward, len(self.string))
        for removable_forward in set(self.forward.keys()) - back_reachable:
            del self.forward[removable_forward]

        for removable_backward in set(self.backward.keys()) - back_reachable:
            del self.backward[removable_backward]

    @property
    def end_sentinel(self):
        return len(self.string)

    def _all_paths(self, position, past_decorations):
        """Returns iterator over sequences of (begin, end) pairs that
        completely cover the target."""
        for endpt in self.forward[position]:
            decorations = past_decorations + ((position, endpt),)
            if endpt == self.end_sentinel:
                yield decorations
            else:
                for p in self._all_paths(
                        position=endpt,
                        past_decorations=decorations):
                        yield p

    @property
    def paths(self):
        return tuple(self._all_paths(position=0, past_decorations=()))

    def substr(self, start, end):
        # raise ValueError if end > len(self.string)
        return self.string[start:end]

    @property
    def token_sequences(self):
        """iterable over tokenizations."""
        return tuple(tuple(self.substr(b, e) for b, e in path)
                     for path in self.paths)

    @property
    def transductions(self):
        def _itr():
            for p in self.paths:
                for t in self._transductions(p, [()]):
                    yield t
        return list(_itr())

    def _transductions(self, path, so_far):
        if not path:
            return so_far
        span = path[0]

        new_so_far = []
        for t in self.transduce(*span):
            for old_path in so_far:
                new_so_far.append(old_path + tuple([t]))
        return self._transductions(path[1:], new_so_far)


class Lattice(BaseLattice):
    """Simple tiling with one admitter. Works for non-whitespace languages?"""
    def __init__(self, string, admitter, **kwargs):
        # Value error if admitter not a container
        self.admitter = admitter
        super(Lattice, self).__init__(string, **kwargs)

    def admit(self, start, end):
        return self.substr(start, end) in self.admitter

    def transduce(self, b, e):
        assert isinstance(self.admitter, Mapping)
        if self.multiple_transductions:
            return self.admitter[self.substr(b, e)]
        else:
            return [self.admitter[self.substr(b, e)]]


class AlternatingLattice(BaseLattice):
    """Explores assuming alternation between two types of legal.

    Works well for spacer/content tokenization.
    """
    def __init__(self, string, content_admitter, spacing_admitter,
                 discard_spacers=True,
                 **kwargs):
        # Value errors if admitters not containers
        self.content_admitter = content_admitter
        self.spacing_admitter = spacing_admitter
        self.discard_spacers = discard_spacers
        self.content_ends = set([0])
        self.spacing_ends = set([0])
        super(AlternatingLattice, self).__init__(string, **kwargs)

    def admit(self, start, end):
        s = self.substr(start, end)
        # print("testing substring '" + s + "' from", start, "to", end)
        matched = False
        if start in self.spacing_ends and s in self.content_admitter:
                self.content_ends.add(end)
                # print ("matched '" + s + "'")
                matched = True
        if start in self.content_ends and s in self.spacing_admitter:
                self.spacing_ends.add(end)
                # print ("spacing matched '" + s + "'")
                matched = True
        return matched

    def transduce(self, b, e):
        """Same as for simple Lattice, except two transducers."""
        assert isinstance(self.content_admitter, Mapping)
        assert self.discard_spacers or isinstance(self.spacing_admitter,
                                                  Mapping)
        s = self.substr(b, e)
        if self.discard_spacers or s in self.content_admitter:
            if self.multiple_transductions:
                return self.content_admitter[s]
            else:
                return [self.content_admitter[s]]
        else:
            if self.multiple_transductions:
                return self.spacing_admitter[s]
            else:
                return [self.spacing_admitter[s]]

    @property
    def paths(self):
        raw = super(AlternatingLattice, self).paths
        if self.discard_spacers:
            return list(self._clean_paths(raw))
        else:
            return raw

    def _clean_paths(self, paths):
        """Only return paths that delimit contentful."""
        _sent = set()
        for path in paths:
            clean = tuple((b, e) for b, e in path
                          if self.substr(b, e) in self.content_admitter)
            if clean not in _sent:
                yield clean
                _sent.add(clean)


class RegexGazette(Container):
    def __init__(self, pattern):
        self._pattern = re.compile(pattern + r'$')
        # assert pattern is regex?

    def __contains__(self, thing):
        return self._pattern.match(thing)


class SegmentationError(ValueError):
    """Raise this when there's a headache segmenting a lattice."""
    pass


class Transduction(Sequence):
    """Consider moving Transduction and IslexOrthoLattice to a separate
    module."""
    def __init__(self, wordseq):
        self._words = wordseq

    def __len__(self):
        return len(self._words)

    def __getitem__(self, key):
        return self._words[key]

    def syllable_range(self, begin, end):
        """Returns new Transduction for each range."""
        sylls = self.syllabification
        if begin not in range(0, len(sylls)):
            raise ValueError("begin value %s out of range" % begin)
        if end not in range(0, len(sylls) + 1):
            raise ValueError("end value %s out of range" % end)

        cursor = 0
        words_in_range = []
        for w in self._words:
            w_syll_count = sum(len(pron.sylls) for pron in w.prons)
            next_cursor = cursor + w_syll_count
            # print("begin", begin, "cursor", cursor, "end", end,
            #       "word", w.ortho)
            if begin <= cursor < end:
                if next_cursor <= end:
                    words_in_range.append(w)
                else:
                    # next_cursor > end
                    raise SegmentationError(
                        "word '%s' broken across end of range"
                        % w.ortho)
            elif end <= cursor:
                break
            else:
                # cursor < begin
                if begin < next_cursor < end:
                    raise SegmentationError(
                        "word '%s' broken across beginning of range"
                        % w.ortho)

            cursor = next_cursor
        return Transduction(words_in_range)

    @property
    def retokenization(self):
        return tuple(w.ortho for w in self._words)

    @property
    def pronunciation(self):
        return tuple(itertools.chain.from_iterable(
            w.prons for w in self._words))

    @property
    def syllabification(self):
        return tuple(itertools.chain.from_iterable(
            pron.sylls for pron in self.pronunciation))

    @property
    def syllable_count(self):
        return len(self.syllabification)

    @property
    def ipa_syllabification(self):
        return tuple(''.join(syll.ipa) for syll in self.syllabification)


class IslexOrthoLattice(AlternatingLattice):
    def __init__(self, st):
        # Build or retrieve an ortho-based multidictionary.
        discard = RegexGazette(r'[0-9<>\'",.?!:;\s]+')
        super(IslexOrthoLattice, self).__init__(
            string=st,
            content_admitter=islex.load.ortho_mapping(islex.data.core),
            spacing_admitter=discard, discard_spacers=True,
            multiple_transductions=True)

    @property
    def transductions(self):
        return [Transduction(t)
                for t in super(IslexOrthoLattice, self).transductions]

    @property
    def retokenizations(self):
        return [t.retokenization for t in self.transductions]

    @property
    def pronunciations(self):
        return [t.pronunciation for t in self.transductions]

    @property
    def ipa_syllabifications(self):
        return [t.ipa_syllabification
                for t in self.transductions]
