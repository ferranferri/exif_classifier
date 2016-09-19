import getopt
import json
import os
import sys
import logging

from file_item import FileItem
from log_config import get_logger
from percentage_show import printProgress

DEFAULT_CONFIG_FILE = 'conf/config.json'


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
        num_items = len(file_list)
        current_item = 0
        num_files_copied = 0
        printProgress(current_item, num_items, prefix='Progress:', suffix='Complete', barLength=50)
        for file_item in file_list:
            created_dir = self.create_path_from_name(file_item)
            created_dir = os.path.join(os.getcwd(), self.config['destination_folder'], created_dir)
            path, file_exists = file_item.copy_to(os.path.join(created_dir, file_item.name()))
            current_item += 1
            if not file_exists:
                num_files_copied += 1
            printProgress(current_item, num_items, prefix='Progress:', suffix='Complete', barLength=50)

        print ("Finished. " + str(num_items) + ' processed. ' + str(num_files_copied) + ' new files added')

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
        files_to_process = []
        list_items = os.listdir(source_folder)
        for item in list_items:
            item = os.path.join(os.getcwd(), self.config['source_folder'], item)
            if os.path.isdir(item):
                self.files_to_process += self.__list_subfolder(item)
            elif os.path.exists(item) and os.path.isfile(item):
                files_to_process.append(FileItem(os.path.abspath(item)))
        return files_to_process

    def create_path_from_name(self, file_item):
        date_exif = file_item.creation_date()
        date, hour = date_exif.split(' ')
        date = date.replace(':', '/')
        return date


def usage():
    help_string = """
    Usage: python exif_classifier.py [OPTIONS]

    OPTIONS:
        --v --verbose   Show debug messages
    """
    print(help_string)


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
