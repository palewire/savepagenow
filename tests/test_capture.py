import savepagenow


def test_capture():
    """Test the basic function of retriving a URL from Wayback."""
    url = "https://www.latimes.com/"
    archive_url, c = savepagenow.capture_or_cache(url)
    assert archive_url.startswith("https://web.archive.org/")
