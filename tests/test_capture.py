import random

import savepagenow

SITE_LIST = [
    "https://palewi.re/docs/first-django-admin/",
    "https://palewi.re/docs/first-github-scraper/",
    "https://palewi.re/docs/first-pull-request/",
    "https://palewi.re/docs/first-python-notebook/",
    "https://palewi.re/docs/first-visual-story/",
    "https://palewi.re/docs/air-quality-index/",
    "https://bln-python-client.readthedocs.io/",
]


def test_capture():
    """Test the basic function of retriving a URL from Wayback."""
    url = random.choice(SITE_LIST)
    archive_url, c = savepagenow.capture_or_cache(url)
    assert archive_url.startswith("https://web.archive.org/")


def test_auth_capture():
    """Test the retrieval of URL from Wayback with authentication."""
    url = random.choice(SITE_LIST)
    archive_url = savepagenow.capture(url, authenticate=True)
    assert archive_url.startswith("https://web.archive.org/")
