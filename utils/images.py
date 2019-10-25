from root.settings import MEDIA_ROOT
import os

TEMPORARY_DIR = os.path.join(MEDIA_ROOT, 'temp')


class TempImage:
    def __init__(self, file):
        self.file = file
        self.path = f'{TEMPORARY_DIR}/{str(file)}'

    def save(self):
        with open(self.path, 'wb+') as dest:
            for chunk in self.file.chunks():
                dest.write(chunk)

    def delete(self):
        os.remove(self.path)
