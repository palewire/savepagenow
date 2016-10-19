#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import savepagenow


class CaptureTest(unittest.TestCase):

    def test_capture(self):
        archive_url_1, c1 = savepagenow.capture_or_cache("http://www.example.com/")
        self.assertTrue(archive_url_1.startswith("http://web.archive.org/"))

        archive_url_2, c2 = savepagenow.capture_or_cache(
            "http://www.example.com/",
            user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
        )
        self.assertTrue(archive_url_2.startswith("http://web.archive.org/"))
        self.assertEquals(archive_url_1, archive_url_2)


if __name__ == '__main__':
    unittest.main()
