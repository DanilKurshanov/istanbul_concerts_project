import os
import random


class Layers():

    def __init__(self, path: str):
        self.path = path

    def get_image_path(self):
        image_file_name = os.listdir(self.path)
        return os.path.normpath(os.path.join(self.path, random.choice(image_file_name)))
        # return (self.path, random.choice(image_file_names))
