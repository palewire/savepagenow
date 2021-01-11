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
        archive_url, c = savepagenow.capture_or_cache(url)
        self.assertTrue(archive_url.startswith("https://web.archive.org/"))

    def test_capture_v2(self):
        """
        Test the basic function of retriving a URL from Wayback using the API.
        """
        url = "https://www.latimes.com/california"
        data = savepagenow.capture_v2(url, accept_cache=True)
        self.assertTrue(data['original_url'].startswith("https://www.latimes.com/"))

    # def test_robots_error(self):
    #     with self.assertRaises(savepagenow.BlockedByRobots):
    #         savepagenow.capture("http://www.archive.is/faq.html")


if __name__ == '__main__':
    unittest.main()
