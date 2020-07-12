#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom exceptions
"""


class CachedPage(Exception):
    """
    This error is raised when archive.org declines to make a new capture
    and instead returns the cached version of most recent archive.
    """
    pass


class WaybackRuntimeError(Exception):
    """
    An error returned by the Wayback Machine.
    """
    pass


class BlockedByRobots(WaybackRuntimeError):
    """
    This error is raised when archive.org has been blocked by the site's robots.txt access control instructions.
    """
    pass
