#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import random
import savepagenow


class CaptureTest(unittest.TestCase):

    def test_capture(self):
        random_number = random.choice(range(0, 1000))
        url = "http://www.example.com/my-random-page-{}".format(random_number)
        archive_url_1, c1 = savepagenow.capture_or_cache(url)
        self.assertTrue(archive_url_1.startswith("https://web.archive.org/"))

        # Test CacheError
        archive_url_2, c2 = savepagenow.capture_or_cache(
            url,
            user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
        )
        self.assertTrue(archive_url_2.startswith("https://web.archive.org/"))
        self.assertEqual(archive_url_1, archive_url_2)

    # def test_robots_error(self):
    #     with self.assertRaises(savepagenow.BlockedByRobots):
    #         savepagenow.capture("http://www.archive.is/faq.html")


if __name__ == '__main__':
    unittest.main()
