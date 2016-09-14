import os


class FileItem:
    def __init__(self, source_path):
        if not os.path.isabs(source_path):
            raise ValueError("Path must me absolut!!\n >>" + source_path)
        self.source_path = source_path

    def exists(self):
        return os.path.exists(self.source_path)

    def full_file_name(self):
        return self.source_path



    

