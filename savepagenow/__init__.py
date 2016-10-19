#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from .exceptions import CachedPage
from six.moves.urllib.parse import urljoin
__version__ = "0.0.5"


def capture(
    target_url,
    archive="web.archive.org",
    user_agent="savepagenow (https://github.com/pastpages/savepagenow)",
    accept_cache=False
):
    if archive == "webcitation.org":
        return capture_webcitation(target_url, user_agent=user_agent)
    elif archive == "archive.is":
        return capture_archive_is(target_url, user_agent=user_agent)
    else:
        return capture_web_archive_org(target_url, user_agent=user_agent,
                                       accept_cache=accept_cache)


def capture_web_archive_org(target_url, user_agent, accept_cache):
    """
    Archives the provided URL using archive.org's Wayback Machine.

    Returns the archive.org URL where the capture is stored.
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


def capture_webcitation(target_url, user_agent):
    """
    Archives the provided URL using webcitation.org's submission form

    Returns the archive.is URL where the capture is stored.
    """

    def random_email():
        """
        Helper function for capture_webcitation

        Webcitation requires you to include an email address when submitting

        They do not check if it is valid
        """
        import random
        from six.moves import range
        alpha = "abcdefghijklmnopqrstuvwxyz"
        choices = alpha + "0123456789"
        domains = [".com", ".org", ".edu", ".co.uk", ".net"]
        text = []

        # build the user portion of the email
        for i in range(0, random.randint(2, 4)):
            # need 2-4 individual chunks with length between 1-3 characters
            for j in range(0, random.randint(1, 3)):
                text.append(choices[random.randint(0, len(choices) - 1)])

        text.append('@')

        # build the email host
        for i in range(0, random.randint(2, 3)):
            for j in range(0, random.randint(1, 3)):
                text.append(alpha[random.randint(0, len(alpha) - 1)])

        text.append(domains[random.randint(0, 4)])

        return ''.join(text)

    # Put together the URL that will save our request
    domain = "http://www.webcitation.org"
    save_url = urljoin(domain, "/archive.php")

    # generate the random email
    email = random_email()

    # Send the capture request to webcitation.org
    headers = {
        'User-Agent': user_agent,
    }
    data = {"email": email, "url": target_url}
    response = requests.post(save_url, headers=headers, data=data)

    # build the regular expression to find
    # the location of the archived resource
    import re
    archived_location_regex = re.compile(r"""(          # begin capture group
                                       [A-Za-z]{4,5}:// # matches http(s)://
                                       [a-z]{3}\.       # matches www.
                                       [a-z]{11}        # matches webcitation
                                       \.[a-z]{3}/      # matches .org/
                                       [a-zA-z0-9]{9}   # matches 9 character
                                                        # archived resource
                                                        # unique identifier
                                       )                # end capture group
                                       """, re.X)

    # search through the returned html page for the location
    # to the archived resource
    # when found, the url-m is contained in group 0 of the returned MatchObject
    # see https://docs.python.org/3/library/re.html#re.regex.search
    archive_url = archived_location_regex.search(response.text).group(0)

    return archive_url


def capture_archive_is(target_url, user_agent):
    """
    Archives the provided URL using archive.is's submission form

    Returns the archive.is URL where the capture is stored.
    """
    # Put together the URL that will save our request
    domain = "http://archive.is"
    save_url = urljoin(domain, "/submit/")

    # Send the capture request to archive.is
    headers = {
        'User-Agent': user_agent,
    }
    data = {"coo": '', "url": target_url}
    response = requests.post(save_url, headers=headers, data=data)

    # archive.is returns a link format timemap in the header field link
    # but if it was the first time archive.is has archived the uri-r
    # or for some other reason unknown at this time
    # this information will not be present so resort to searching the
    # returned html page
    import re
    memento_re = re.compile('"(http(?:s)?://archive\.is/(?:[0-9]{14}/(?:\b)?)?'
                            '[-a-zA-Z0-9@:%_+.~#?&/=]+)"',
                            re.IGNORECASE | re.MULTILINE)
    mementos = memento_re.findall(response.text)

    # the url to the memento is the first element in the list
    return mementos[0]


def capture_or_cache(
    target_url,
    user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
):
    try:
        return capture(target_url, user_agent=user_agent, accept_cache=False), True
    except CachedPage:
        return capture(target_url, user_agent=user_agent, accept_cache=True), False
