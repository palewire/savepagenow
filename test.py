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
        self.assertTrue(archive_url_1.startswith("http://web.archive.org/"))

        # Test CacheError
        archive_url_2, c2 = savepagenow.capture_or_cache(
            url,
            user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
        )
        self.assertTrue(archive_url_2.startswith("http://web.archive.org/"))
        self.assertEqual(archive_url_1, archive_url_2)

    # def test_robots_error(self):
    #     with self.assertRaises(savepagenow.BlockedByRobots):
    #         savepagenow.capture("http://www.archive.is/faq.html")


class VersionsTest(unittest.TestCase):

    def test_versions(self):
        versions = savepagenow.get_versions('https://nytimes.com')
        version = next(versions)
        self.assertTrue(version.startswith('https://web.archive.org/'))

    def test_versions_limit(self):
        count = 0
        versions = savepagenow.get_versions('http://nytimes.com', limit=1111)
        self.assertEqual(len(list(versions)), 1111)

    def test_versions_paging(self):
        count = 0
        for url in savepagenow.get_versions('https://nytimes.com', chunk_limit=10):
            count += 1
            if count > 10:
                break
        self.assertTrue(count > 10)


if __name__ == '__main__':
    unittest.main()
