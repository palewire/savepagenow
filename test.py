#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import savepagenow


class CaptureTest(unittest.TestCase):
    def test_attr(self):
        archive_url = savepagenow.capture("http://www.example.com/")
        self.assertTrue(archive_url.startswith("http://web.archive.org/"))
        archive_url = savepagenow.capture("http://www.example.com/",
                                          archive='webcitation.org')
        self.assertTrue(archive_url.startswith("http://www.webcitation.org"))
        archive_url = savepagenow.capture("http://www.example.com/",
                                          archive='archive.is')
        self.assertTrue(archive_url.startswith("http://archive.is"))


if __name__ == '__main__':
    unittest.main()
