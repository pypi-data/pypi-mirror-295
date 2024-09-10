import os
from pathlib import Path
from typing import Any, Dict, Union

import numpy as np
from loguru import logger

from ..enums import Enums
from ..exceptions import NumpyLoadError, WrongDatsetFile
from ..utils import extract_archive


class NumpyDataLoader:
    def __init__(self, dataset_file_path:str, inputs:Dict[Union[str, int], Any]):
        self.npy = self.load_datasets(dataset_file_path, inputs)

    def load_datasets(self, dataset_file_path:str, inputs:Dict[Union[str, int], Any])->Dict[Union[str, int], np.ndarray]:
        outputs = {}
        # for single numpy file case
        if Path(dataset_file_path).is_file() and Path(dataset_file_path).suffix == ".npy":
            for key in inputs:
                try:
                    outputs[key]=np.load(dataset_file_path)
                except ValueError:
                    raise NumpyLoadError(detail=f"Failed to load the .npy file: {dataset_file_path}.")
            return outputs
        # for multiple numpy file case
        elif Path(dataset_file_path).suffix not in Enums.NUMPY_FILE_SUFFIXES.value:
            # Unzip dataset_file_path
            extract_archive(dataset_file_path, os.path.dirname(dataset_file_path))
            parent_directory = os.path.dirname(dataset_file_path)
            for key in inputs:
                file_name = f"{key}.npy"
                file_path = os.path.join(parent_directory, file_name)
                if os.path.exists(file_path):
                    try:
                        outputs[key] = np.load(file_path)
                    except ValueError:
                        raise NumpyLoadError(detail=f"Failed to load the .npy file: {file_path}.")
                else:
                    logger.warning(f"Warning: File {file_path} does not exist.")
            return outputs
        else:
            raise WrongDatsetFile()
