import os
from .file_storage import FileStorage

class MetadataStorage(FileStorage):
    def __init__(self, storage_path):
        super().__init__(os.path.join(storage_path, "metadata"))
