#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from collections.abc import Sequence
from datetime import timedelta
from os import getenv
import requests
from .exceptions import (
    CachedPage,
    WaybackRuntimeError,
    BlockedUrl,
    BlockedByRobots
)
from urllib.parse import urljoin
from requests.utils import parse_header_links
import time


USER_AGENT = "savepagenow (https://github.com/pastpages/savepagenow)"


def capture(
    target_url,
    user_agent=USER_AGENT,
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

    # If there's a content-location header in the response, we will use that.
    try:
        content_location = response.headers['Content-Location']
        archive_url = domain + content_location
    except KeyError:
        # If there's not, we  will try to parse out a Link header, which is another style they use.
        try:
            # Parse the Link tag in the header, which points to memento URLs in Wayback
            header_links = parse_header_links(response.headers['Link'])
            archive_obj = [h for h in header_links if h['rel'] == 'memento'][0]
            archive_url = archive_obj['url']
        except Exception:
            # If neither of those things works throw this error.
            raise WaybackRuntimeError(dict(status_code=response.status_code, headers=response.headers))

    # Determine if the response was cached
    cached = 'X-Page-Cache' in response.headers and response.headers['X-Page-Cache'] == 'HIT'

    # If it was cached ...
    if cached:
        # .. and we're not allowing that
        if not accept_cache:
            # ... throw an error
            msg = f'archive.org returned a cache of this page: {archive_url}'
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


def queue_capture_v2(
    target_url,
    user_agent=USER_AGENT,
    accept_cache=False,
    s3_access_key=None,
    s3_secret_key=None,
    capture_all=False,
    capture_outlinks=False,
    capture_screenshot=False,
    force_get=False,
    skip_first_archive=False,
    if_not_archived_within=None,
    outlinks_availability=False,
    email_result=False,
    js_behavior_timeout=None,
    capture_cookie=None,
    target_username=None,
    target_password=None
):
    """
    Enqueue a request to capture the provided URL using archive.org's advanced
    API. This returns information about the capture job that was queued; to get
    the results, call ``get_status_v2``.

    Returns a dict with the ID of the enqueued capture job and the requested
    URL.

    Raises a CachedPage exception if archive.org declines to conduct a new
    capture and returns a previous snapshot instead.

    To silence that exception, pass into True to the ``accept_cache`` keyword
    argument.
    """
    data = {
        'url': target_url,
        'capture_all': int(capture_all),
        'capture_outlinks': int(capture_outlinks),
        'capture_screenshot': int(capture_screenshot),
        'force_get': int(force_get),
        'skip_first_archive': int(skip_first_archive),
        'outlinks_availability': int(outlinks_availability),
        'email_result': int(email_result),
    }

    if if_not_archived_within:
        if isinstance(if_not_archived_within, Sequence):
            timeframe = if_not_archived_within
        else:
            timeframe = [if_not_archived_within]
        for index, value in enumerate(timeframe):
            if isinstance(value, timedelta):
                timeframe[index] = str(value.total_seconds())
            else:
                timeframe[index] = str(value)
        data['if_not_archived_within'] = ','.join(timeframe)

    if js_behavior_timeout is not None:
        if not isinstance(js_behavior_timeout, (float, int)):
            raise TypeError('js_behavior_timeout must be a number >= 0')
        elif js_behavior_timeout < 0:
            raise ValueError('js_behavior_timeout must be >= 0')
        data['js_behavior_timeout'] = js_behavior_timeout

    if capture_cookie:
        data['capture_cookie'] = capture_cookie

    if target_username:
        data['target_username'] = target_username
    if target_password:
        data['target_password'] = target_password

    response = requests.post('https://web.archive.org/save', data=data, headers={
        'Accept': 'application/json',
        'Authorization': get_authorization(s3_access_key, s3_secret_key),
        'User-Agent': user_agent,
    })

    result = response.json()
    if result.get('status') == 'error':
        raise parse_api_error(result)
    # If the page was recently captured and a new job was not started, the API
    # returns a normal job info object with an added "message" property.
    elif 'message' in result and not accept_cache:
        # TODO: Modify CachedPage to accept extra info
        error = CachedPage(f'{result["message"]} Capture job: {result["job_id"]}')
        error.job_id = result['job_id']
        error.url = result['url']
        raise error

    return result


def get_status_v2(
    job_id,
    user_agent=USER_AGENT,
    s3_access_key=None,
    s3_secret_key=None
):
    """
    Get the status of a capture job that was queued using ``queue_capture_v2``.
    If the job is complete, this will return details about the results.

    This returns a dict with the status and other details of the job. If a job
    is still pending, the ``status`` property will be ``"pending"``. If a job
    is complete, the ``status`` property will be ``"complete"`` and additional
    details about the result will be included in the dict.

    If a job failed, this will raise an exception representing the error as a
    subclass of ``savepagenow.WaybackRuntimeError`` or
    ``savepagenow.BlockedUrl``.
    """
    response = requests.get(
        # Unfortunately, there's a caching proxy in front of this API, even
        # though it's meant for polling. Tack the current time onto each
        # to break the cache.
        f'https://web.archive.org/save/status/{job_id}?dont-cache={time.time()}',
        headers={
            'Accept': 'application/json',
            'Authorization': get_authorization(s3_access_key, s3_secret_key),
            'User-Agent': user_agent,
        }
    )

    result = response.json()
    if 'error' in result:
        raise parse_api_error(result)

    return result


def capture_v2(
    target_url,
    user_agent=USER_AGENT,
    accept_cache=False,
    s3_access_key=None,
    s3_secret_key=None,
    capture_all=False,
    capture_outlinks=False,
    capture_screenshot=False,
    force_get=False,
    skip_first_archive=False,
    if_not_archived_within=None,
    outlinks_availability=False,
    email_result=False,
    js_behavior_timeout=None,
    capture_cookie=None,
    target_username=None,
    target_password=None,
    status_interval=1
):
    """
    Archives the provided URL using archive.org's advanced API. This method
    requires authentication, but allows for much more fine-grained control over
    the capture process.

    Authentication is performed using the "S3-like" keys that can be found for
    your account at: https://archive.org/account/s3.php. Provide them using the
    ``s3_access_key`` and ``s3_secret_key`` arguments or via the
    ``IAS3_ACCESS_KEY`` and ``IAS3_SECRET_KEY`` environment variables.

    This returns a dict with details of the job. If a job.

    Raises a CachedPage exception if archive.org declines to conduct a new
    capture and returns a previous snapshot instead. To silence that exception,
    pass into True to the ``accept_cache`` keyword argument.

    This may also raise a WaybackRuntimeError with more details if the capture
    fails for other reasons.

    For more complete details of the advanced API, check the documentation at:
    https://docs.google.com/document/d/1Nsv52MvSjbLb2PCpHlat0gkzw0EvtSgpKHu4mk0MnrA

    Parameters
    ----------
    - ``target_url`` is the URL to capture. This is the only required parameter.
    - ``user_agent`` is a custom user agent to use when communitcating with the
      Internet Archive.
    - ``accept_cache`` controls whether a ``CachedPage`` exception is raised if
      the page was already captured recently.
    - ``s3_access_key`` The S3-like access key to log into the Internet Archive
      with. This can also be set via the `IAS3_ACCESS_KEY` environment
      variable. To find your keys, check https://archive.org/account/s3.php.
    - ``s3_secret_key`` The S3-like secret key to log into the Internet Archive
      with. This can also be set via the `IAS3_ACCESS_KEY` environment
      variable. To find your keys, check https://archive.org/account/s3.php.
    - ``capture_all`` If true, capture the URL regardless of the status code.
      By default, only URLs with a 2xx status are captured.
    - ``capture_outlinks`` If true, also capture URLs linked to from
      ``target_url``. This works for HTML, PDF, and JSON/RSS feeds.
    - ``capture_screenshot`` If true, capture a full page screenshot in PNG
      format.
    - ``force_get`` If true, do not use a web browser to capture
      ``target_url``. By default, Save Page Now will determine whether to use a
      browser automatically.
    - ``skip_first_archive`` If true, do not check whether this was the first
      capture of ``target_url``. This can speed up captures.
    - ``if_not_archived_within`` Only capture ``target_url`` if it was not
      already captured within this timeframe. If you do not set this, a default
      value will be applied by archive.org's servers. This can be a timedelta
      object, a number (of seconds), or a string with a format like
      ``"3d 5h 20m"`` (3 days, 5 hours, and 20 minutes). If
      ``capture_outlinks`` is true, this may also be a sequence of 2 of any of
      the above types, where the first item represents the timeframe for
      ``target_url`` and the second item represents the timeframe for outlinks.
    - ``outlinks_availability`` If true, include the timestamp of the last
        capture for all outlinks in the result.
    - ``email_result`` If true send en e-mail report of the results to the
      user whose credentials were used for this capture.
    - ``js_behavior_timeout`` Limit JavaScript execution to this many seconds
      after page load. Setting this to ``0`` prevents JavaScript execution
      entirely.
    - ``capture_cookie`` Cookie values to set when capturing ``target_url``.
    - ``target_username`` Use this username in the page's login forms when
      capturing it.
    - ``target_password`` Use this password in the page's login forms when
      capturing it.
    - ``status_interval`` Check for results every N seconds.
    """
    if not isinstance(status_interval, (float, int)):
        raise TypeError('status_interval must be a number >= 0')
    elif status_interval < 0:
        raise ValueError('status_interval must be >= 0')

    job_info = queue_capture_v2(
        target_url,
        user_agent=user_agent,
        # Set `accept_cache` so we can continue execution and return cached
        # results with the error.
        accept_cache=True,
        s3_access_key=s3_access_key,
        s3_secret_key=s3_secret_key,
        capture_all=capture_all,
        capture_outlinks=capture_outlinks,
        capture_screenshot=capture_screenshot,
        force_get=force_get,
        skip_first_archive=skip_first_archive,
        if_not_archived_within=if_not_archived_within,
        outlinks_availability=outlinks_availability,
        email_result=email_result,
        js_behavior_timeout=js_behavior_timeout,
        capture_cookie=capture_cookie,
        target_username=target_username,
        target_password=target_password
    )
    while True:
        status = get_status_v2(
            job_info['job_id'],
            user_agent=user_agent,
            s3_access_key=s3_access_key,
            s3_secret_key=s3_secret_key
        )
        if status['status'] == 'pending':
            time.sleep(status_interval)
            continue
        elif not accept_cache and 'message' in job_info:
            archive_url = f'https://web.archive.org/web/{status["timestamp"]}/{status["original_url"]}'
            error = CachedPage(f'archive.org returned a cache of this page: {archive_url}')
            error.job_id = status['job_id']
            error.url = job_info['url']
            error.result = status
            raise error
        else:
            return status


def get_authorization(s3_access_key, s3_secret_key):
    """
    Get an authorization header string for the currently configured "S3-like"
    keys. This will read environment variables if the parameters are ``None``.
    """
    if not s3_access_key:
        s3_access_key = getenv('IAS3_ACCESS_KEY')
    if not s3_secret_key:
        s3_secret_key = getenv('IAS3_SECRET_KEY')
    if not s3_access_key or not s3_secret_key:
        raise TypeError(
            'You must set the `s3_access_key` and `s3_secret_key` parameters '
            'or the `IAS3_ACCESS_KEY` and `IAS3_SECRET_KEY` environment '
            'variables to use the v2 API'
        )

    return f'LOW {s3_access_key}:{s3_secret_key}'


def parse_api_error(data):
    """
    Parse an error response from the API and return an exception object that
    represents it.
    """
    bad_arguments = (
        'error:invalid-url-syntax',
        'error:invalid-url',
        'error:invalid-host-resolution',
    )

    # TODO: Consider whether any of these deserve special types
    # other_errors = (
    #     'error:too-many-daily-captures',
    #     'error:invalid-server-response',
    #     'error:user-session-limit',
    #     'error:soft-time-limit-exceeded',
    #     'error:proxy-error',
    #     'error:browsing-timeout',
    #     'error:no-browsers-available',
    #     'error:redis-error',
    #     'error:capture-location-error',
    #     'error:gateway-timeout',
    #     'error:no-access',
    #     'error:not-found',
    #     'error:celery',
    #     'error:filesize-limit',
    #     'error:ftp-access-denied',
    #     'error:read-timeout',
    #     'error:protocol-error',
    #     'error:too-many-redirects',
    #     'error:too-many-requests',
    #     'error:not-implemented',
    #     'error:bad-gateway',
    #     'error:service-unavailable',
    #     'error:http-version-not-supported',
    #     'error:network-authentication-required',
    # )

    error_name = data['status_ext']
    if error_name in bad_arguments:
        error = ValueError(data['message'])
    elif error_name == 'error:blocked-url':
        error = BlockedUrl(data['message'])
    else:
        error = WaybackRuntimeError(data['message'])

    # Attach additional details to the error.
    error.exception = data.get('exception')
    error.status_ext = data.get('status_ext')
    error.job_id = data.get('job_id')

    return error


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
