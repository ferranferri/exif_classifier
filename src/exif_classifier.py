import getopt
import json
import os
import sys


class ExifClassifier:
    """
    Classifies images by their exif creation date information. You need to provide a config file to configure class.
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}
        self.files_to_process = []

    def __load_configuration(self, configuration_file):
        # check that exists
        if not os.path.exists(self.config_file):
            raise IOError('File ' + self.config_file + ' does not exists')
        with open(self.config_file) as data_file:
            self.config = json.load(data_file)

    def start(self):
        self.__load_configuration(configuration_file=self.config_file)
        file_list = self.get_file_list(self.config['source_folder'])
        pass

    def get_file_list(self, source_folder):
        flist = []
        self.__list_subfolder(source_folder)
        pass

    def __list_subfolder(self, source_folder):
        dirs = os.listdir(source_folder)
        for d in dirs:
            fname = os.path.join(os.path.abspath(source_folder), d)
            if not os.path.exists(fname):
                raise IOError("path " + fname + " does not exists!!")
            if os.path.isfile(fname):
                filename = os.path.abspath(fname)
                self.files_to_process.append(filename)
            if os.path.isdir(fname):
                self.__list_subfolder(os.path.abspath(fname))

"""
exif_dict = piexif.load(
    '/Users/ferranferri/directo/development/experimental/exif_classifier/Camera/2016-04-21-18h06m30.jpg')

exif_d = exif_dict['Exif']
creation_date = exif_d[36867]
print(creation_date)
"""


def usage():
    print("Read the fucking manual!!!!")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c", ['configfile='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    configfile = None
    for opt, arg in opts:
        if opt in ("c", "--configfile"):
            configfile = arg

    try:
        exif_classifier = ExifClassifier(config_file=configfile)
        exif_classifier.start()
    except Exception as e:
        print e
        usage()
        sys.exit(2)


if __name__ == '__main__':
    main()
