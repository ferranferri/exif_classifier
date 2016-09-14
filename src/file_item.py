import os
import hashlib
import piexif
import shutil


class FileItem:
    def __init__(self, source_path):
        if not os.path.isabs(source_path):
            raise ValueError("Path must me absolut!!\n >>" + source_path)
        self.source_path = source_path
        self.exif_dic = {}

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

    def copy_to(self, path):
        final_path = path
        if os.path.exists(final_path):
            if os.path.isdir(final_path):
                final_path = os.path.join(final_path, self.name())
                shutil.copyfile(self.source_path, final_path)
                return final_path
            elif os.path.isfile(final_path):
                shutil.copyfile(self.source_path, final_path)
                return final_path



    

