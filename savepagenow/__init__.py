import requests
from six.moves.urllib.parse import urljoin


def capture(target_url):
    """
    Archives the provided URL using archive.org's Wayback Machine.

    Returns the archive.org URL where the capture is stored.
    """
    # Put together the URL that will save our request
    domain = "http://web.archive.org"
    save_url = urljoin(domain, "/save/")
    request_url = save_url + target_url

    # Send the capture request to achive.org
    response = requests.get(request_url)

    # Put together the URL where this page is archived
    archive_id = response.headers['Content-Location']
    archive_url = urljoin(domain, archive_id)

    # Determine if the response was cached
    cached = response.headers['X-Page-Cache'] == 'HIT'
    if cached:
        print("Cached URL returned")

    # Return that
    return archive_url
