import os
import hashlib
import piexif
import shutil
import logging


class FileItem:
    def __init__(self, source_path):
        if not os.path.isabs(source_path):
            raise ValueError("Path must me absolut!!\n >>" + source_path)
        self.source_path = source_path
        self.dest_path = ''
        self.exif_dic = {}
        logging.basicConfig(level=logging.CRITICAL)
        self.logger = logging.getLogger("FILE_ITEM")

    @staticmethod
    def __file_md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def exists(self):
        return os.path.exists(self.source_path)

    def full_file_name(self):
        return self.source_path

    def name(self):
        return self.source_path.split(os.sep)[-1]

    def directory(self):
        return os.path.abspath(os.path.join(self.source_path, os.pardir))

    def creation_date(self):
        self.exif_dic = piexif.load(self.source_path)
        return self.exif_dic['Exif'][36867]

    def equals(self, fi2):
        a = self.__file_md5(self.source_path)
        assert fi2.exists()
        b = self.__file_md5(fi2.full_file_name())
        return a == b

    def __create_dir_recursive(self, path):
        if not os.path.exists(path):
            self.__create_dir_recursive(os.path.join(path, os.pardir))
        os.makedirs(path)

    def get_destination_path(self):
        return self.dest_path

    def copy_to(self, path):
        final_path = path
        file_exists = False
        if not os.path.exists(final_path):
            file_exists = False
            if final_path.endswith('/') or final_path.endswith('\\'):
                # assume is a directory
                os.makedirs(final_path)
                shutil.copy(self.source_path, os.path.join(final_path, self.name()))
                self.dest_path = os.path.join(final_path, self.name())
            else:
                final_folder = os.path.abspath(os.path.join(final_path, os.pardir))
                # get the file name
                name = final_path.split('/')[-1]
                if not os.path.exists(final_folder):
                    os.makedirs(final_folder)
                shutil.copy(self.source_path, os.path.join(final_folder, name))
                self.dest_path = os.path.join(final_folder, name)
        else:
            file_exists = True
            self.logger.warning("A file with the same name already exists")
            fi = FileItem(final_path)
            if self.equals(fi):
                self.dest_path = fi.full_file_name()
                self.logger.info("The file is the same. No copies are made")
            else:
                name, extension = fi.name().split(".")
                directory = fi.directory()
                self.dest_path = os.path.join(directory, name + '_1.' + extension)
                self.copy_to(self.dest_path)
                self.logger.warning("Two different files with the same name exists. Changing destination name")
        return self.dest_path, file_exists
