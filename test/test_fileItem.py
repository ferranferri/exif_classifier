import os
from unittest import TestCase

from file_item import FileItem



class TestFileItem(TestCase):

    def setUp(self):
        self.FILE_EXIST_PATH = '/Users/ferranferri/directo/development/experimental/exif_classifier/test_resources/camera10/folder1/2016-05-11-20h32m20.jpg'
        self.FILE_NOT_EXIST_PATH = '/Users/ferranferri/directo/development/experimental/exif_classifier/test_resources/camera10/folder1/2020-05-11-20h32m20.jpg'

    def test_constructor_if_path_is_not_absolut_raise_valueerror(self):
        with self.assertRaises(ValueError) as context:
            fi = FileItem('test_resources/camera10/folder1/2016-05-11-20h32m20.jpg')
        print(context.exception)

    def test_exists_returns_false_if_file_not_exists(self):
        fi = FileItem(self.FILE_NOT_EXIST_PATH)
        self.assertFalse(fi.exists())

    def test_exists_returns_true_if_file_exists(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        self.assertTrue(fi.exists())

    def test_full_file_name_returns_original_file_name_with_path(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        self.assertEqual(fi.full_file_name(), self.FILE_EXIST_PATH)

    def test_full_file_name_is_always_absolut_path(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        self.assertTrue(os.path.isabs(fi.full_file_name()))

    def test_file_name_returns_the_name_of_file(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        self.assertEqual(fi.name, '2016-05-11-20h32m20.jpg')

