#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CachedPage(Exception):
    """
    This error is raised when archive.org declines to make a new capture
    and instead returns the cached version of most recent archive.
    """
    pass
