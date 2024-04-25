# savepagenow

A simple Python wrapper and command-line interface for archive.org’s [“Save Page Now”](https://archive.org/web) capturing service

## Installation

The package can be installed from the [Python Package Index](https://pypi.org/project/savepagenow/) with one of Python’s installation tools. Here's an example with `pipenv`.

```bash
pipenv install savepagenow
```

## Python Usage

First import the library into your Python code.

```python
import savepagenow
```

Capture a URL.

```python
archive_url = savepagenow.capture("http://www.example.com/")
```

See where it's stored.

```python
print(archive_url)
```

### Authentication

By default, savepagenow sends anonymous requests, which are limited to three captures per minute.

Authenticated requests are allowed 6 captures per minute. To take advantage of this, you must register an account with [archive.org](https://archive.org/account/login.createaccount.php) and
set your [API credentials](https://archive.org/account/s3.php) to the local environment variables ``SAVEPAGENOW_ACCESS_KEY`` and ``SAVEPAGENOW_SECRET_KEY``.

Then you can run `capture()` with the authenticate flag set to true like so:

```python
savepagenow.capture(url, authenticate=True)
```

### Cached pages

If a URL has been recently cached, archive.org may return the URL to that page rather than conduct a new capture. When that happens, the ``capture`` method will raise a ``CachedPage`` exception.

This is likely happen if you request the same URL twice within a few seconds.

```
savepagenow.capture("http://www.example.com/")
'https://web.archive.org/web/20161019062637/http://www.example.com/'
savepagenow.capture("http://www.example.com/")
Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   File "savepagenow/__init__.py", line 36, in capture
      archive_url
savepagenow.exceptions.CachedPage: archive.org returned a cached version of this page: https://web.archive.org/web/20161019062637/http://www.example.com/
```

You can craft your code to catch that exception yourself, or use the built-in ``capture_or_cache`` method, which will return the URL provided by archive.org along with a boolean indicating if it is a fresh capture (True) or from the cache (False).

```python
savepagenow.capture_or_cache("http://www.example.com/")
("https://web.archive.org/web/20161019062832/http://www.example.com/", True)
savepagenow.capture_or_cache("http://www.example.com/")
("https://web.archive.org/web/20161019062832/http://www.example.com/", False)
```

There's no accounting for taste but you could craft a line to handle that command like so:

```python
url, captured = savepagenow.capture_or_cache("http://www.example.com/")
```

## Command-line usage

The Python library is also installed as a command-line interface. You can run it from your terminal like so:

```bash
savepagenow https://example.com/
```

The command has the same options as the Python API.

```bash
Usage: savepagenow [OPTIONS] URL

  Archive the provided URL using archive.org's Wayback Machine.

  Raises a CachedPage exception if archive.org declines to conduct a new
  capture and returns a previous snapshot instead.

Options:
  -ua, --user-agent TEXT  User-Agent header for the web request
  -c, --accept-cache      Accept and return cached URL
  -a, --authenticate      Allows you to run saves with authentication
  --help                  Show this message and exit.
```

### Developing the CLI

The command-line interface is implemented using Click and setuptools. To install it locally for development inside your virtual environment, run the following installation command, as [prescribed by the Click documentation](https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration).

```bash
pip install --editable .
```

## Customizing the user agent

In an effort to be transparent and polite to the Internet Archive, all requests made by savepagenow carry a custom [user agent](https://en.wikipedia.org/wiki/User_agent) that identifies itself as ``"savepagenow (https://github.com/pastpages/savepagenow)"``.

You can further customize this setting by using the optional arguments to our API.

Here's how to do it in Python:

```python
savepagenow.capture("http://www.example.com/", user_agent="my user agent here")
```

And here's how to do it from the command line:

```bash
savepagenow http://www.example.com/ --user-agent "my user agent here"
```

## Links

- Documentation: [palewi.re/docs/savepagenow/](https://palewi.re/docs/savepagenow/)
- Code: [github.com/palewire/savepagenow](https://github.com/palewire/savepagenow)
- Issues: [github.com/palewire/savepagenow/issues](https://github.com/palewire/savepagenow/issues)
- Packaging: [pypi.org/project/savepagenow](https://pypi.org/project/savepagenow)
