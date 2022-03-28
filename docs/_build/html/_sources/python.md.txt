```{include} _templates/nav.html
```

# Python Usage

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
