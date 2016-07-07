#! /usr/bin/python3
import os
import cli
import unittest

# Testing for download one

class tests_for_cli(unittest.TestCase):
    def test_download_one(self):
        cli.download_one(cli.read_dict(), 1000)
        desc_path = os.path.abspath('.') + '/xkcd_archive/1000/description.txt'
        png_path = os.path.abspath('.') + '/xkcd_archive/1000/1000Comics.png'
        self.assertTrue(os.path.isfile(desc_path))
        self.assertTrue(os.path.isfile(png_path))

    def test_download_exclude_list(self):
        cli.download_one(cli.read_dict(), 1608)
        # Special comics may or may not have an image, but definitely have a
        # description
        desc_path = os.path.abspath('.') + '/xkcd_archive/1608/description.txt'
        png_path = os.path.abspath('.') + '/xkcd_archive/1608/1000Comics.png'
        self.assertTrue(os.path.isfile(desc_path))
        self.assertFalse(os.path.isfile(png_path))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
