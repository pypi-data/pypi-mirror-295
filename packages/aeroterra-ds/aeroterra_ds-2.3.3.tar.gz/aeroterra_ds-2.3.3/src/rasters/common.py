from typing import Union

import os

from exceptions.type_checker import type_checker

@type_checker
def is_tiff(file: str):
    """
    Returns a boolean indicating if a file is a tiff image
    
    Parameters:
        file: (Relative) Path to file wanting to check if a tiff
    """
    filename, file_extension = os.path.splitext(file)
    
    file_extension = file_extension.lower()
    
    return file_extension.find(".tif") == 0

@type_checker
def get_tiffs_from_folder(tiff_folder: str):
    """
    Return all the tiffs files from the tiff_folder
    
    Parameters:
        file: (Relative) Path to folder wanting to check
    """
    if not os.path.isdir(tiff_folder):
        raise Exception(f"Folder {tiff_folder} Doesn't Exist")

    files = os.listdir(tiff_folder)

    tiff_files = []

    for file in files:
        if is_tiff(file):
            file = f"{tiff_folder}{file}"
            tiff_files.append(file)

    return tiff_files


NUMBER_LIKE = Union[int, float, complex]