# savepagenow

A simple Python wrapper for archive.org's "Save Page Now" capturing service.

### Installation

```bash
$ pip install savepagenow
```

### Usage

Import it.

```python
>>> import savepagenow
```

Capture a URL.

```python
>>> archive_url = savepagenow.capture("http://www.example.com/")
```

See where it's stored.

```python
>>> print archive_url
http://web.archive.org/web/20161018203554/http://www.example.com/
```
