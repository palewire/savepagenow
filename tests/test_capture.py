import random

import pytest

import savepagenow
from savepagenow.exceptions import WaybackRuntimeError

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
    archive_url = savepagenow.capture(url, authenticate=True, accept_cache=True)
    assert archive_url.startswith("https://web.archive.org/")


def test_link_header_fallback_timegate(monkeypatch):
    """When memento is missing, fall back to timegate in Link header."""

    class DummyResponse:
        def __init__(self):
            self.status_code = 200
            self.headers = {
                "Link": '<https://example.com>; rel="original", '
                '<https://web.archive.org/web/timemap/link/https://example.com>; rel="timemap"; type="application/link-format", '
                '<https://web.archive.org/web/https://example.com>; rel="timegate"'
            }
            self.content = b""

    def fake_get(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr(savepagenow.api.requests, "get", fake_get)

    archive_url = savepagenow.capture("https://example.com")
    assert archive_url == "https://web.archive.org/web/https://example.com"


def test_link_header_fallback_missing(monkeypatch):
    """Raise clear runtime error when no usable Link targets exist."""

    class DummyResponse:
        def __init__(self):
            self.status_code = 200
            self.headers = {"Link": '<https://example.com>; rel="original"'}
            self.content = b""

    def fake_get(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr(savepagenow.api.requests, "get", fake_get)

    with pytest.raises(WaybackRuntimeError):
        savepagenow.capture("https://example.com")
