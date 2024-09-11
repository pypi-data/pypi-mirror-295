#!/usr/bin/env python

"""
    `jict` provides dictionaries with multiple
    levels of nested-ness.
"""

__version__ = '3.0.2'

from .jict import jict
from .helpers import walk, cycle
from .yaml_to_note import yaml_to_note
from .soup import Soup

__all__ = ( 'jict', 'deque' ,'walk', 'Soup','yaml_to_note')
