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
from requests.utils import parse_header_links


def capture(
    target_url,
    user_agent="savepagenow (https://github.com/pastpages/savepagenow)",
    accept_cache=False
):
    """
    Archives the provided URL using archive.org's Wayback Machine.

    Returns a tuple with the archive.org URL where the capture is stored,
    along with a boolean indicating if a new capture was conducted.

    Raises a CachedPage exception if accept_cache=False and archive.org
    declines to conduct a new capture and returns a previous snapshot instead.
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

    # Parse the Link tag in the header, which points to memento URLs in Wayback
    header_links = parse_header_links(response.headers['Link'])

    # The link object marked as the `memento` is the one we want to return
    try:
        archive_obj = [h for h in header_links if h['rel'] == 'memento'][0]
        archive_url = archive_obj['url']
    except (IndexError, KeyError):
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
    return (archive_url, not cached)


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
    (archive_url, captured) = capture(url, **kwargs)
    click.echo(archive_url)
    click.echo(captured)


if __name__ == "__main__":
    cli()
