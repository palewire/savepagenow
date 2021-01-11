#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .api import (
    capture,
    capture_or_cache,
    capture_v2,
    queue_capture_v2,
    get_status_v2,
    CachedPage,
    BlockedByRobots
)


__version__ = "1.0.1"

__all__ = (
    'BlockedByRobots',
    'capture',
    'capture_or_cache',
    'capture_v2',
    'queue_capture_v2',
    'get_status_v2',
    'CachedPage'
)
