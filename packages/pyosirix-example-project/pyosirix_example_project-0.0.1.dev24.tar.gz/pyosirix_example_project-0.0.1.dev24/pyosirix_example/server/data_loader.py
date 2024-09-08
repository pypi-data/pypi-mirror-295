import os

import dvc.api

from pyosirix_example import __gh_hash__, __gh_repo__


class DataLoader:
    def __init__(self):
        self.data_directory = os.path.join(__file__, "data")
        os.makedirs(self.data_directory, exist_ok=True)

    @staticmethod
    def __dvc_data_path__() -> str:
        """ The location of the data file in the main repository (where the dvc file is located).
        """
        return "data/viewer_text.txt"

    @property
    def data_path(self) -> str:
        """ Where the data is located within the package.
        """
        return os.path.join(self.data_directory, "viewer_text.txt")

    def __download_data__(self):
        """ Load the data from the DVC repository
        """
        with dvc.api.open(self.__dvc_data_path__(), repo=__gh_repo__, rev=__gh_hash__) as f:
            with open(self.data_path, 'wb') as d:
                d.write(f.read())

    @property
    def data(self) -> str:
        """ The content of the data file.
        """
        if not os.path.exists(self.data_path):
            self.__download_data__()

        with open(self.data_path, 'r') as f:
            return f.read()
