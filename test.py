#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import savepagenow


class CaptureTest(unittest.TestCase):
    def test_capture(self):
        archive_url_1 = savepagenow.capture("http://www.example.com/")
        self.assertTrue(archive_url_1.startswith("http://web.archive.org/"))

        archive_url_2 = savepagenow.capture(
            "http://www.example.com/",
            user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
        )
        self.assertTrue(archive_url_2.startswith("http://web.archive.org/"))
        self.assertEquals(archive_url_1, archive_url_2)

    def test_capture_additional_archives(self):
        # webcitation and archive.is generate unique identifiers
        # e.g 6lNs1rSP8 != 6lNs26aSl per archive request
        # testing two requests for the same resource to produce
        # the same url would always fail
        archive_url_1 = savepagenow.capture("http://www.example.com/",
                                            archive='webcitation.org')
        archive_url_2 = savepagenow.capture(
            "http://www.example.com/",
            archive='webcitation.org',
            user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
        )

        self.assertTrue(archive_url_1.startswith("http://www.webcitation.org"))
        self.assertTrue(archive_url_2.startswith("http://www.webcitation.org"))

        archive_url_1 = savepagenow.capture("http://www.example.com/",
                                            archive='archive.is')
        archive_url_2 = savepagenow.capture(
            "http://www.example.com/",
            archive='archive.is',
            user_agent="savepagenow (https://github.com/pastpages/savepagenow)"
        )

        self.assertTrue(archive_url_1.startswith("http://archive.is"))
        self.assertTrue(archive_url_2.startswith("http://archive.is"))


if __name__ == '__main__':
    unittest.main()
