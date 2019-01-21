A simple Python wrapper for archive.org's "Save Page Now" capturing service

.. image:: https://badge.fury.io/py/savepagenow.png
   :target: http://badge.fury.io/py/savepagenow
   :alt: PyPI version

.. image:: https://travis-ci.org/pastpages/savepagenow.svg?branch=master
   :target: https://travis-ci.org/pastpages/savepagenow
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/pastpages/savepagenow/badge.svg?branch=master
   :target: https://coveralls.io/github/pastpages/savepagenow?branch=master
   :alt: Coverage Status


Installation
^^^^^^^^^^^^

.. code-block:: bash

   $ pip install savepagenow


Python Usage
^^^^^^^^^^^^

Import it.

.. code-block:: python

   >>> import savepagenow


Capture a URL.

.. code-block:: python

   >>> archive_url = savepagenow.capture("http://www.example.com/")


See where it's stored.

.. code-block:: python

   >>> print archive_url
   https://web.archive.org/web/20161018203554/http://www.example.com/


If a URL has been recently cached, archive.org may return the URL to that page rather than conduct a new capture. When that happens, the ``capture`` method will raise a ``CachedPage`` exception.

This is likely happen if you request the same URL twice within a few seconds.

.. code-block:: python

   >>> savepagenow.capture("http://www.example.com/")
   'https://web.archive.org/web/20161019062637/http://www.example.com/'
   >>> savepagenow.capture("http://www.example.com/")
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "savepagenow/__init__.py", line 36, in capture
       archive_url
   savepagenow.exceptions.CachedPage: archive.org returned a cached version of this page: https://web.archive.org/web/20161019062637/http://www.example.com/


You can craft your code to catch that exception yourself, or use the built-in ``capture_or_cache`` method, which will return the URL provided by archive.org along with a boolean indicating if it is a fresh capture (True) or from the cache (False).

.. code-block:: python

   >>> savepagenow.capture_or_cache("http://www.example.com/")
   ('https://web.archive.org/web/20161019062832/http://www.example.com/', True)
   >>> savepagenow.capture_or_cache("http://www.example.com/")
   ('https://web.archive.org/web/20161019062832/http://www.example.com/', False)


There's no accounting for taste but you could craft a line to handle that command like so:

.. code-block:: python

   >>> url, captured = savepagenow.capture_or_cache("http://www.example.com/")


Command-line usage
^^^^^^^^^^^^^^^^^^

The Python library is also installed as a command-line interface. You can run it from your terminal like so:

.. code-block:: bash

   $ savepagenow http://www.example.com/


The command has the same options as the Python API, which you can learn about from its help output.

.. code-block:: bash

   $ savepagenow --help
   Usage: savepagenow [OPTIONS] URL

     Archives the provided URL using the archive.org Wayback Machine.

     Raises a CachedPage exception if archive.org declines to conduct a new
     capture and returns a previous snapshot instead.

   Options:
     -ua, --user-agent TEXT  User-Agent header for the web request
     -c, --accept-cache      Accept and return cached URL
     --help                  Show this message and exit.


Customizing the user agent
^^^^^^^^^^^^^^^^^^^^^^^^^^

In an effort to be transparent and polite to the Internet Archive, all requests made by savepagenow carry a custom `user agent <https://en.wikipedia.org/wiki/User_agent>`_ that identifies itself as ``"savepagenow (https://github.com/pastpages/savepagenow)"``.

You can further customize this setting by using the optional arguments to our API.

Here's how to do it in Python:

.. code-block:: python

   >>> savepagenow.capture("http://www.example.com/", user_agent="my user agent here")


And here's how to do it from the command line:

.. code-block:: bash

   $ savepagenow http://www.example.com/ --user-agent "my user agent here"
