import getopt
import json
import os
import sys
import logging
import piexif
from shutil import copyfile
import ntpath
from percentage_show import printProgress

DEFAULT_CONFIG_FILE = 'conf/config.json'
LOG_NAME = 'IMG_SORT'


class ExifClassifier:
    """
    Classifies images by their exif creation date information. You need to provide a config file to configure class.
    """

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}
        self.files_to_process = []

    def load_configuration(self, configuration_file):
        """
        Loads config file set in constructor. Raises IOError if is not a correct file or does not exists and ValueError
        if the contents are not valid json.
        :param configuration_file:
        :return: None
        """
        if not os.path.exists(self.config_file):
            raise IOError('File ' + self.config_file + ' does not exists')
        if os.path.isdir(self.config_file):
            raise IOError('A file is expected but ' + self.config_file + ' is a directory')
        try:
            with open(self.config_file) as data_file:
                self.config = json.load(data_file)
        except ValueError as err:
            raise ValueError("Cannot parse json file " + self.config_file)

    def process_list(self, file_list, config):
        # check that destination folder exists
        des_folder = self.folder_global_path(config['destination_folder'])
        i = 0
        for item in file_list:
            i += 1
            exif_dict = piexif.load(item)
            creation_date = exif_dict['Exif'][36867]
            date_folder = creation_date.split(' ')[0].replace(':', '/')
            global_folder_name = os.path.join(des_folder, date_folder)
            if not os.path.exists(global_folder_name):
                os.makedirs(global_folder_name)
            file_name = ntpath.basename(item)
            copyfile(item, os.path.join(global_folder_name, file_name))
            printProgress(iteration=i, total=len(file_list), prefix="progress: ", barLength=70,
                          suffix='(' + str(i) + '/' + str(len(file_list)) + ')')

    def start(self):
        self.load_configuration(configuration_file=self.config_file)
        file_list = self.get_file_list(self.config['source_folder'])
        self.process_list(file_list, self.config)

    def get_file_list(self, source_folder):
        """
        Returns a list of files in folder
        :param source_folder: source folder
        :return: List of files
        """
        return self.__list_subfolder(source_folder)

    def __list_subfolder(self, source_folder):
        """
        Recursively process the source folder and makes a list of files to process
        :param source_folder: Source folder
        :return: A list of the contents of folder and its subfolders
        """
        directories = os.listdir(source_folder)
        file_list = []
        for item in directories:
            item_name = os.path.join(os.path.abspath(source_folder), item)
            if not os.path.exists(item_name):
                raise IOError("path " + item_name + " does not exists!!")
            if os.path.isfile(item_name):
                filename = os.path.abspath(item_name)
                file_list.append(filename)
            if os.path.isdir(item_name):
                file_list = file_list + self.__list_subfolder(os.path.abspath(item_name))
        return file_list

    def validate_folder(self, folder):
        return self.validate_item(folder) and os.path.isdir(folder)

    def folder_global_path(self, folder):
        if self.validate_folder(folder):
            return os.path.join(os.getcwd(), folder)
        raise IOError("Directory " + folder + " does not exists")

    @staticmethod
    def validate_item(item):
        return os.path.exists(item)


def usage():
    help_string = """
    Usage: python exif_classifier.py [OPTIONS]

    OPTIONS:
        --v --verbose   Show debug messages
    """
    print(help_string)


def get_logger():
    global LOG_NAME
    return logging.getLogger(LOG_NAME)


def process_options(opts):
    logger = get_logger()
    configfile = None
    options = {}
    for opt, arg in opts:
        if opt in ("c", "--configfile"):
            logger.debug("Loading custom config file " + arg)
            configfile = arg

    if configfile is None:
        global DEFAULT_CONFIG_FILE
        logger.debug("Loading default config file " + DEFAULT_CONFIG_FILE)
        options['configfile'] = DEFAULT_CONFIG_FILE

    return options


def main():
    logger = get_logger()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cv", ['configfile=', 'verbose'])
    except getopt.GetoptError as err:
        logger.error(err)
        usage()
        sys.exit(2)
    # setting log. Search for verbose level
    logging.basicConfig(level=logging.CRITICAL)
    logger = logging.getLogger("IMG_SORT")
    for opt, arg in opts:
        if opt in ("v", "--verbose"):
            logger.setLevel(logging.DEBUG)
            logger.debug("Verbose on. Show debug messages")

    options = process_options(opts)

    try:
        exif_classifier = ExifClassifier(config_file=options['configfile'])
        exif_classifier.start()
    except Exception as e:
        logger.error(e)
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
