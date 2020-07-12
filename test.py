#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests.
"""
import unittest
import savepagenow


class CaptureTest(unittest.TestCase):

    def test_capture(self):
        """
        Test the basic function of retriving a URL from Wayback.
        """
        url = "https://www.latimes.com/"
        archive_url, c1 = savepagenow.capture_or_cache(url)
        self.assertTrue(archive_url.startswith("https://web.archive.org/"))

    # def test_robots_error(self):
    #     with self.assertRaises(savepagenow.BlockedByRobots):
    #         savepagenow.capture("http://www.archive.is/faq.html")


if __name__ == '__main__':
    unittest.main()
