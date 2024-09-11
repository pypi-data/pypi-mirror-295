import os
import re
from os.path import join
import shutil

def get_names(FOLDER):
    """
    Retrieves and sorts the names of all items in the specified folder.

    Parameters:
    FOLDER (str): The path to the folder from which to retrieve item names.

    Returns:
    list of str: A sorted list of names of the items in the specified folder.

    Example:
    folder_names = get_names("/path/to/folder")
    print(folder_names)
    """
    names = os.listdir(FOLDER)
    names.sort()
    return names

def remove_files_from_case(pattern: str, path_to_case: str):
    """
    Removes files that match the specified pattern from the given directory.

    Parameters:
    pattern (str): The regular expression pattern to match filenames against.
    path_to_case (str): The path to the directory from which files should be removed.

    Example:
    remove_files_from_case(r'^temp.*/.txt$', "/path/to/case")
    """
    files_to_remove = [file for file in os.listdir(path_to_case)
                       if re.match(pattern, file)]
    for file in files_to_remove:
        os.remove(join(path_to_case, file))

def remove_files_based_on_pattern(pattern: str | re.Pattern[str], FOLDER):
    """
    Removes files that match the specified pattern from subdirectories within the given folder.
    It looks for files in "initial" and "final" subdirectories of each folder found in FOLDER.

    Parameters:
    pattern (str | re.Pattern[str]): The regular expression pattern to match filenames against.
    FOLDER (str): The path to the root folder containing subdirectories to search in.

    Example:
    remove_files_based_on_pattern(r'^temp.*/.txt$', "/path/to/root/folder")
    """
    names = get_names(FOLDER)
    for name in names:
        for period in ["initial", "final"]:
            remove_files_from_case(pattern, join(FOLDER, name, period))


def copy_structure(initial_folder, final_folder):
    """
    Creates a new directory structure in 'final_folder' that mirrors the structure of 'initial_folder'.
    
    Parameters:
    - initial_folder (str): The path to the initial directory whose structure will be copied.
    - final_folder (str): The path to the final directory where the new structure will be created.
    
    Raises:
    - FileExistsError: If 'final_folder' already exists.
    """
    os.mkdir(final_folder)
    names = os.listdir(initial_folder)
    for name in names:
        subfolders = os.listdir(join(initial_folder, name))
        os.mkdir(join(final_folder, name))
        for period in subfolders:
            os.mkdir(join(final_folder, name, period))

def areFilesinStructure(initial_folder, files):
    """
    Checks if the specified files exist in the structure of 'initial_folder'.
    
    Parameters:
    - initial_folder (str): The path to the initial directory.
    - files (list of str): A list of file names to check.
    
    Returns:
    - bool: True if all files exist in the structure, False otherwise.
    """
    names = os.listdir(initial_folder)
    for name in names:
        subfolders = os.listdir(join(initial_folder, name))
        for period in subfolders:
            for file in files:
                if not os.path.exists(join(initial_folder, name, period, file)):
                    return False
    return True

def isStructureCorrect(initial_folder, final_folder):
    """
    Checks if the structure of 'final_folder' matches the structure of 'initial_folder'.
    
    Parameters:
    - initial_folder (str): The path to the initial directory.
    - final_folder (str): The path to the final directory.
    
    Returns:
    - bool: True if the structures match, False otherwise.
    """
    names = os.listdir(initial_folder)
    for name in names:
        subfolders = os.listdir(join(initial_folder, name))
        for period in subfolders:
            if not os.path.exists(join(final_folder, name, period)):
                return False
    return True

def symlink_files(initial_folder, final_folder, files_to_symlink):
    """
    Creates symbolic links for specified files from 'initial_folder' to 'final_folder'.
    
    Parameters:
    - initial_folder (str): The path to the initial directory.
    - final_folder (str): The path to the final directory.
    - files_to_symlink (list of str): A list of file names to symlink.
    
    Raises:
    - OSError: If an error occurs during the creation of symbolic links.
    """
    names = os.listdir(initial_folder)
    for name in names:
        subfolders = os.listdir(join(initial_folder, name))
        for period in subfolders:
            for file in files_to_symlink:
                os.symlink(
                    os.path.abspath(join(initial_folder, name, period, file)),
                    os.path.abspath(join(final_folder, name, period, file))
                )

def copy_files(initial_folder, final_folder, files_to_symlink):
    """
    Copies specified files from 'initial_folder' to 'final_folder'.
    
    Parameters:
    - initial_folder (str): The path to the initial directory.
    - final_folder (str): The path to the final directory.
    - files_to_symlink (list of str): A list of file names to copy.
    
    Raises:
    - shutil.Error: If an error occurs during the copying of files.
    """
    names = os.listdir(initial_folder)
    for name in names:
        subfolders = os.listdir(join(initial_folder, name))
        for period in subfolders:
            for file in files_to_symlink:
                shutil.copy(
                    os.path.abspath(join(initial_folder, name, period, file)),
                    os.path.abspath(join(final_folder, name, period, file))
                )

def create_workfolder(initial_folder, final_folder, paths_to_symlink=[], paths_to_copy=[]):
    """
    Creates a new working directory structure in 'final_folder', copying and symlinking specified files from 'initial_folder'.
    
    Parameters:
    - initial_folder (str): The path to the initial directory.
    - final_folder (str): The path to the final directory.
    - paths_to_symlink (list of str, optional): A list of file paths to symlink.
    - paths_to_copy (list of str, optional): A list of file paths to copy.
    
    Returns:
    - bool: True if the operation is successful, False otherwise.
    
    Raises:
    - FileExistsError: If the files to copy or to symlink are not in the initial folder, or they are corrupted.
    - Exception: If an error occurs during the copying or symlinking process.
    """
    b1 = areFilesinStructure(initial_folder, paths_to_symlink)
    b2 = areFilesinStructure(initial_folder, paths_to_copy)
    if b1 and b2:
        try:
            copy_structure(initial_folder, final_folder)
        except Exception as e:
            raise e
    else:
        raise FileExistsError("The files to copy or to symlink are not in the initial folder, or they are corrupted!")

    if paths_to_copy:
        print("I am copying")
        try:
            copy_files(initial_folder, final_folder, paths_to_copy)
        except Exception as e:
            raise e

    if paths_to_symlink:
        print("I am symlinking")
        try:
            symlink_files(initial_folder, final_folder, paths_to_symlink)
        except Exception as e:
            raise e
        
    return True