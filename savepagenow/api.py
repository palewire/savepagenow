#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import requests
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

    To silence that exception, pass into True to the ``accept_cache`` keyword
    argument.
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

    # If it has an error header, raise that.
    has_error_header = 'X-Archive-Wayback-Runtime-Error' in response.headers
    if has_error_header:
        error_header = response.headers['X-Archive-Wayback-Runtime-Error']
        if error_header == 'RobotAccessControlException: Blocked By Robots':
            raise BlockedByRobots("archive.org returned blocked by robots.txt error")
        else:
            raise WaybackRuntimeError(error_header)

    # If it has an error code, raise that
    if response.status_code in [403, 502]:
        raise WaybackRuntimeError(response.headers)

    # Put together the URL where this page is archived
    try:
        archive_id = response.headers['Content-Location']
    except KeyError:
        # If it can't find that key raise the error
        raise WaybackRuntimeError(dict(status_code=response.status_code, headers=response.headers))
    archive_url = urljoin(domain, archive_id)

    # Determine if the response was cached
    cached = 'X-Page-Cache' in response.headers and response.headers['X-Page-Cache'] == 'HIT'
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


def get_versions(
    url,
    limit=0,
    chunk_limit=1000,
    user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
):
    """
    versions returns archived versions of a given URL as an iterator. It will
    page through results from the Internet Archive's CDX Server API until 
    there aren't any more.  If you would like to limit the total number of URLs
    returned use the limit parameter. If you want to change the number of URLs 
    that are requested at a time from the API use the chunk_limit parameter, 
    which defaults to 1000 and can have a maximum valuee of 150000.
    """

    cdx_url = "https://web.archive.org/cdx/search/cdx"
    params = {
        "url": url,
        "limit": chunk_limit,
        "collapse": "timestamp",
        "showResumeKey": "true",
        "output": "json"
    }

    count = 0
    more_to_do = True
    while more_to_do:
        results = requests.get(cdx_url, params=params).json()

        # remove headers
        if len(results) > 1:
            results.pop(0)

        resume_key = None
        for r in results:
            if len(r) == 1:
                resume_key = r[0]
            elif len(r) > 0:
                count += 1
                if limit and count > limit:
                    more_to_do = False
                else:
                    yield 'https://web.archive.org/web/{}/{}'.format(r[1], url)
       
        if resume_key:
            params['resumeKey'] = resume_key
        else:
            more_to_do = False


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


@click.command()
@click.argument("url")
@click.option("-ua", "--user-agent", help="User-Agent header for the web request")
@click.option("-c", "--accept-cache", help="Accept and return cached URL", is_flag=True)
@click.option("-v", "--versions", help="Print archived versions of URL", is_flag=True)
@click.option("-l", "--limit", help="Limit number of archive URLs to return. The default of 0 is unlimited.", default=0)
def cli(url, user_agent, accept_cache, versions, limit):
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
    if versions:
        for archive_url in get_versions(url, limit=limit):
            click.echo(archive_url)
    else:
        archive_url = capture(url, **kwargs)
        click.echo(archive_url)


if __name__ == "__main__":
    cli()
