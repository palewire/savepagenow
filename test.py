#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import savepagenow


class CaptureTest(unittest.TestCase):

    def test_attr(self):
        archive_url = savepagenow.capture("http://www.example.com/")
        self.assertTrue(archive_url.startswith("http://web.archive.org/"))


if __name__ == '__main__':
    unittest.main()
