import os
from unittest import TestCase
from exif_classifier import ExifClassifier


class TestExifClassifier(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestExifClassifier, self).__init__(*args, **kwargs)
        self.incorrect_json_file = os.path.join(os.getcwd(), "test_resources/connf.json")
        self.correct_json_file = os.path.join(os.getcwd(), "test_resources/config0.json")
        self.correct_json_file_with_content = os.path.join(os.getcwd(), "test_resources/config10.json")
        self.base_folder = os.path.join(os.getcwd(), "test_resources")

    def setUp(self):
        with open(self.incorrect_json_file, 'w') as conf_json:
            conf_json.write("error_content")

        #os.makedirs(os.path.join(self.base_folder, "camera0"))
        #os.makedirs(os.path.join(self.base_folder, "camera10"))

    def tearDown(self):
        if os.path.exists(self.incorrect_json_file):
            os.remove(self.incorrect_json_file)


    #######################################################################################
    #  Test cases                                                                       ###
    #######################################################################################

    def test___load_configuration_when_config_doesnotexists_then_execption_is_raised(self):
        ec = ExifClassifier(config_file="fff")
        with self.assertRaises(IOError) as context:
            ec.load_configuration(configuration_file="fff")
        self.assertTrue("File fff does not exists" in context.exception)

    def  test__load_configuration_when_config_is_a_directory_then_exception_is_raised(self):
        ec = ExifClassifier(config_file="conf")
        with self.assertRaises(IOError) as context:
            ec.load_configuration(configuration_file="conf")
        self.assertTrue("A file is expected but conf is a directory" in context.exception)

    def test__load_configuration_when_config_isnt_json_anexception_is_raised(self):
        ec = ExifClassifier(config_file=self.incorrect_json_file)
        with self.assertRaises(ValueError) as context:
            ec.load_configuration(configuration_file=self.incorrect_json_file)
        self.assertTrue("Cannot parse json file " + self.incorrect_json_file in context.exception)

    def test_get_file_list_when_folder_have_no_files_return_empty_list(self):
        ec = ExifClassifier(config_file=self.correct_json_file)
        ec.load_configuration(ec.config_file)
        source_folder = os.path.join(self.base_folder, ec.config['source_folder'])
        list_of_files = ec.get_file_list(source_folder)
        self.assertEqual(len(list_of_files), 0)

    def test_get_file_list_when_only_exists_files_count_files_are_correct(self):
        ec = ExifClassifier(config_file=self.correct_json_file_with_content)
        ec.load_configuration(ec.config_file)
        source_folder = os.path.join(self.base_folder, ec.config['source_folder'])
        list_of_files = ec.get_file_list(source_folder)
        self.assertEqual(len(list_of_files), 4)

    def test_get_file_list_each_element_of_list_is_full_path(self):
        ec = ExifClassifier(config_file=self.correct_json_file_with_content)
        ec.load_configuration(ec.config_file)
        source_folder = os.path.join(self.base_folder, ec.config['source_folder'])
        list_of_files = ec.get_file_list(source_folder)
        for f in list_of_files:
            self.assertTrue(os.path.exists(f) and os.path.isfile(f))

    def test_get_file_list_function_crawls_in_deep_folders(self):
        ec = ExifClassifier(config_file=self.correct_json_file_with_content)
        ec.load_configuration(ec.config_file)
        ec.config['source_folder'] = 'camera10'
        source_folder = os.path.join(self.base_folder, ec.config['source_folder'])
        list_of_files = ec.get_file_list(source_folder)
        for f in list_of_files:
            self.assertTrue(os.path.exists(f) and os.path.isfile(f))
        self.assertEqual(len(list_of_files), 15)