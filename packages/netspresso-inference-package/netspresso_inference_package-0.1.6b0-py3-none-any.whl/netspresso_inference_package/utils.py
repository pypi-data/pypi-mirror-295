import os
import shutil
import tarfile
import tempfile
import zipfile
from pathlib import Path

import py7zr
import rarfile
from loguru import logger

from .exceptions import UnsupportedArchiveFormat


def make_temp_dir()->str:
    temp_file_path = tempfile.mkdtemp()
    Path(temp_file_path).mkdir(exist_ok=True, parents=True)
    return temp_file_path


def compress_files(file_paths:str, zip_path:str):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_paths:
            zipf.write(file, arcname=file.split('/')[-1])
    logger.info(f"Compress files: {file_paths}")


def extract_archive(archive_path:str, extract_path:str):
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    elif archive_path.endswith(('.tar', '.tar.gz', '.tgz')):
        with tarfile.open(archive_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_path)
    elif archive_path.endswith('.7z'):
        with py7zr.SevenZipFile(archive_path, mode='r') as z:
            z.extractall(extract_path)
    elif archive_path.endswith('.rar'):
        with rarfile.RarFile(archive_path, 'r') as rar_ref:
            rar_ref.extractall(extract_path)
    else:
        raise UnsupportedArchiveFormat()


def delete_parent_directory(file_path:str):
    try:
        parent_directory = os.path.dirname(file_path)
        shutil.rmtree(parent_directory)
        logger.info(f"Directory {file_path} is deleted.")
    except FileNotFoundError:
        logger.info(f"Directory {file_path} does not exist.")
    except PermissionError:
        logger.info(f"Permission denied to delete {file_path}.")
