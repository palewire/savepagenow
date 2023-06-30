import savepagenow

def test_capture():
    """Test the basic function of retriving a URL from Wayback."""
    url = "https://www.latimes.com/"
    archive_url, c = savepagenow.capture_or_cache(url)
    assert archive_url.startswith("https://web.archive.org/")

def test_auth_capture():
    """Test the retrieval of URL from Wayback with authentication"""
    url = "https://www.latimes.com/"
    # The env variables get pulled when we call capture()
    # You have to set access_key and secret to the appropriate values for your archive.org account
    archive_url, c = savepagenow.capture(url, authenticate=True)
    assert archive_url.startswith("https://web.archive.org/")