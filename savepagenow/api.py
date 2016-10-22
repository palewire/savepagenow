#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from .exceptions import CachedPage
from six.moves.urllib.parse import urljoin


def capture(
    target_url,
    user_agent="savepagenow (https://github.com/pastpages/savepagenow)",
    accept_cache=False
):
    """
    Archives the provided URL using archive.org's Wayback Machine.

    Returns the archive.org URL where the capture is stored.

    Raises a CachedPage exception if archive.org declines to conduct a new
    capture and returns a previous snapshot instead.
    """
    # Put together the URL that will save our request
    domain = "http://web.archive.org"
    save_url = urljoin(domain, "/save/")
    request_url = save_url + target_url

    # Send the capture request to achive.org
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(request_url, headers=headers)

    # Put together the URL where this page is archived
    archive_id = response.headers['Content-Location']
    archive_url = urljoin(domain, archive_id)

    # Determine if the response was cached
    cached = response.headers['X-Page-Cache'] == 'HIT'
    if cached:
        if not accept_cache:
            raise CachedPage("archive.org returned a cached version of this page: {}".format(
                archive_url
            ))

    # Return that
    return archive_url


def capture_or_cache(
    target_url,
    user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
):
    """
    Archives the provided URL using archive.org's Wayback Machine, unless
    the page has been recently captured.

    Returns a tuple with the archive.org URL where the capture is stored,
    along with a boolean indicating if a new capture was conducted.

    If the boolean is True, archive.org conducted a new capture. If it is False,
    archive.org has returned a recently cached capture instead, likely taken
    in the previous minutes.
    """
    try:
        return capture(target_url, user_agent=user_agent, accept_cache=False), True
    except CachedPage:
        return capture(target_url, user_agent=user_agent, accept_cache=True), False
