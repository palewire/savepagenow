#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .api import capture, capture_or_cache, CachedPage, BlockedByRobots


__version__ = "0.0.8"
__all__ = (
    'BlockedByRobots',
    'capture',
    'capture_or_cache',
    'CachedPage',
)
