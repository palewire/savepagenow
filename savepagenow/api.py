#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import requests
from .exceptions import (
    CachedPage,
    WaybackRuntimeError,
    BlockedByRobots
)
from urllib.parse import urljoin


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

    To silence that exception, pass into True to the ``accept_cache`` keyword
    argument.
    """
    # Put together the URL that will save our request
    domain = "https://web.archive.org"
    save_url = urljoin(domain, "/save/")
    request_url = save_url + target_url

    # Send the capture request to archive.org
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(request_url, headers=headers)

    # If it has an error header, raise that.
    has_error_header = 'X-Archive-Wayback-Runtime-Error' in response.headers
    if has_error_header:
        error_header = response.headers['X-Archive-Wayback-Runtime-Error']
        if error_header == 'RobotAccessControlException: Blocked By Robots':
            raise BlockedByRobots("archive.org returned blocked by robots.txt error")
        else:
            raise WaybackRuntimeError(error_header)

    # If it has an error code, raise that
    if response.status_code in [403, 502, 520]:
        raise WaybackRuntimeError(response.headers)

    # The link object marked as the `memento` is the one we want to return
    try:
        content_location = response.headers['Content-Location']
        archive_url = domain + content_location
    except KeyError:
        raise WaybackRuntimeError(dict(status_code=response.status_code, headers=response.headers))

    # Determine if the response was cached
    cached = 'X-Page-Cache' in response.headers and response.headers['X-Page-Cache'] == 'HIT'

    # If it was cached ...
    if cached:
        # .. and we're not allowing that
        if not accept_cache:
            # ... throw an error
            msg = "archive.org returned a cache of this page: {}".format(archive_url)
            raise CachedPage(msg)

    # Finally, return the archived URL
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


@click.command()
@click.argument("url")
@click.option("-ua", "--user-agent", help="User-Agent header for the web request")
@click.option("-c", "--accept-cache", help="Accept and return cached URL", is_flag=True)
def cli(url, user_agent, accept_cache):
    """
    Archives the provided URL using archive.org's Wayback Machine.

    Raises a CachedPage exception if archive.org declines to conduct a new
    capture and returns a previous snapshot instead.
    """
    kwargs = {}
    if user_agent:
        kwargs['user_agent'] = user_agent
    if accept_cache:
        kwargs['accept_cache'] = accept_cache
    archive_url = capture(url, **kwargs)
    click.echo(archive_url)


if __name__ == "__main__":
    cli()
