#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import savepagenow


class CaptureTest(unittest.TestCase):

    def test_capture(self):
        archive_url_1, c1 = savepagenow.capture_or_cache("http://www.example.com/")
        self.assertTrue(archive_url_1.startswith("http://web.archive.org/"))

        # Test CacheError
        archive_url_2, c2 = savepagenow.capture_or_cache(
            "http://www.example.com/",
            user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
        )
        self.assertTrue(archive_url_2.startswith("http://web.archive.org/"))
        self.assertEqual(archive_url_1, archive_url_2)

    def test_robots_error(self):
        with self.assertRaises(savepagenow.BlockedByRobots):
            savepagenow.capture("http://www.columbiamissourian.com/")


if __name__ == '__main__':
    unittest.main()
