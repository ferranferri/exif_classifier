import os
from unittest import TestCase
from exif_classifier import ExifClassifier


class TestExifClassifier(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestExifClassifier, self).__init__(*args, **kwargs)
        self.incorrect_json_file = os.path.join(os.getcwd(), "test_resources/connf.json")

    def setUp(self):
        with open(self.incorrect_json_file, 'w') as conf_json:
            conf_json.write("error_content")

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

