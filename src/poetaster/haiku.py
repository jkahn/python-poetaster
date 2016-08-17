# -*- coding: utf-8 -*-
"""Detects (and formats?) haiku in input strings."""


class NotHaiku(ValueError):
    """Error class indicating that input string was not a haiku (and why)."""
    pass


class Haiku(object):
    """Core components of a haiku."""
    @classmethod
    def from_string(cls, s):
        raise NotHaiku("So far, all input text strings are not haikus.")
