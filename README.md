# savepagenow

A simple Python wrapper for archive.org\'s "Save Page Now" capturing service.

### Installation

```bash
$ pip install savepagenow
```

### Usage

```python
>>> import savepagenow
>>> archive_url = savepagenow.capture("http://www.example.com/")
>>> print archive_url
http://web.archive.org/web/20161018203554/http://www.example.com/
```
