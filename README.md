# savepagenow

A simple Python wrapper for archive.org's "Save Page Now" capturing service.

[![PyPI version](https://badge.fury.io/py/savepagenow.png)](http://badge.fury.io/py/savepagenow)
[![Build Status](https://travis-ci.org/pastpages/savepagenowsvg?branch=master)](https://travis-ci.org/pastpages/savepagenow)
[![Coverage Status](https://coveralls.io/repos/github/pastpages/savepagenow/badge.svg?branch=master)](https://coveralls.io/github/pastpages/savepagenow?branch=master)

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
