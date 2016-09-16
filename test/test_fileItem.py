import os
import shutil
from unittest import TestCase

from file_item import FileItem


class TestFileItem(TestCase):
    def setUp(self):
        self.FILE_EXIST_PATH = os.path.join(os.getcwd(), 'test_resources/camera10/folder1/2016-05-11-20h32m20.jpg')
        self.FILE_EXIST_PATH2 = os.path.join(os.getcwd(), 'test_resources/camera10/folder1/deep1/2016-05-21-17h41m59.jpg')
        self.FILE_NOT_EXIST_PATH = os.path.join(os.getcwd(), '/test_resources/camera10/folder1/2020-05-11-20h32m20.jpg')

    def tearDown(self):
        folder = os.path.join(os.getcwd(), 'test_resources/temp')
        for item in os.listdir(folder):
            file_path = os.path.join(folder, item)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)

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
        self.assertEqual(fi.name(), '2016-05-11-20h32m20.jpg')

    def test_container_folder_returns_the_folder_name(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        self.assertEqual(os.path.join(os.getcwd(), 'test_resources/camera10/folder1'), fi.directory())

    def test_creation_date_returns_exif_creation_date(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        self.assertEqual(fi.creation_date(), '2016:05:11 20:32:20')

    def test_copy_to_a_folder_returns_the_new_path(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        path = os.path.join(os.getcwd(), 'test_resources/temp', fi.name())
        self.assertEqual(path, fi.copy_to(path))

    def test_copy_to_a_folder_returns_path_when_destination_is_a_non_existent_folder(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        path = os.path.join(os.getcwd(), 'test_resources/temp/deep1/deep2/')
        self.assertEqual(os.path.join(path, fi.name()), fi.copy_to(path))


    def test_copy_to_file_returns_path_when_destination_is_a_non_existent_path(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        file_name = 'file1.jpg'
        path = os.path.join(os.getcwd(), 'test_resources/temp/deep1/', file_name)
        self.assertEqual(path, fi.copy_to(path))

    def test_copy_to_the_file_in_destinations_does_exists(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        fi2 = FileItem(self.FILE_EXIST_PATH2)
        fi2.copy_to(os.path.join(os.getcwd(), 'test_resources/temp/deep1/deep2/'))
        path = os.path.join(os.getcwd(), 'test_resources/temp/deep1', fi.name())
        final_path = fi.copy_to(path)
        self.assertTrue(os.path.exists(final_path) and os.path.isfile(path))
    """
    def test_copy_if_folder_does_not_exists_it_is_created(self):
        fi = FileItem(self.FILE_EXIST_PATH)
        path = os.path.join(os.getcwd(), 'test_resources/temp/deep1/deep2', fi.name())
        self.assertFalse(os.path.exists(path))
        final_path = fi.copy_to(path)
        self.assertTrue(os.path.exists(final_path))
    """
    def test_equals_defines_files_equals_other_if_has_the_same_md5_sum(self):
        fi1 = FileItem(self.FILE_EXIST_PATH)
        fi2 = FileItem(self.FILE_EXIST_PATH)
        self.assertTrue(fi1.equals(fi2))

    """
    def test_equals_is_true_even_if_files_are_in_different_places(self):
    def test_equals_defines_files_equals_other_if_has_the_same_md5_sum(self):
        fi1 = FileItem(self.FILE_EXIST_PATH)
        file_name2 = os.path.join(os.getcwd(), 'test_resources/camera10/folder1/deep1/deep2/2016-08-14-14h49m55.jpg')
        fi2 = FileItem(file_name2)
        self.assertTrue(fi1.equals(fi2))
    """
