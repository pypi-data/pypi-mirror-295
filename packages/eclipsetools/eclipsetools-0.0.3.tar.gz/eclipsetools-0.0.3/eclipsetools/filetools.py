import json
import subprocess
import re
import os
import shutil

log_functions: bool = True


def print_et(value):
    if log_functions:
        print(value)


def copy_directory(src_directory: str, dst_directory: str, renaming: list[tuple[str, str]] = [], ignore: list[str] = [],
                   overwrite_files: bool = False, ignore_files: bool = False):
    """
    Copies a directory tree from the source to the destination with optional renaming, ignoring specific paths,
    and optionally overwriting existing files.

    :param src_directory: The source directory to copy from.
    :param dst_directory: The destination directory to copy to.
    :param renaming: A list of tuples with old and new path segments to rename during copying.
    :param ignore: A list of paths to ignore during the copy process.
    :param overwrite_files: Boolean indicating whether to overwrite existing files at the destination.
    :param ignore_files: Boolean indicating whether to ignore copying files, copying only directories.
    :return: None
    """
    src_directory = os.path.abspath(src_directory)
    dst_directory = os.path.abspath(dst_directory)
    paths = []

    # Collect all paths (directories and files) from the source directory
    for root, dirs, files in os.walk(src_directory):
        # Process directories
        for dir_name in dirs:
            abs_dir_path = os.path.abspath(os.path.join(root, dir_name))
            rel_dir_path = os.path.relpath(abs_dir_path, src_directory)
            if abs_dir_path not in ignore and rel_dir_path not in ignore:
                paths.append([rel_dir_path, abs_dir_path])

        # Process files
        for file_name in files:
            abs_file_path = os.path.abspath(os.path.join(root, file_name))
            rel_file_path = os.path.relpath(abs_file_path, src_directory)
            if abs_file_path not in ignore and rel_file_path not in ignore:
                paths.append([rel_file_path, abs_file_path])

    # Sort paths by depth (lowest to highest)
    paths.sort(key=lambda p: p[0].count(os.sep))

    # Apply renaming to paths
    for path in paths:
        for old, new in renaming:
            path[0] = path[0].replace(old, new)

    # Construct the full paths for the destination directory
    full_renamed_paths = [
        [os.path.join(dst_directory, path[0]), path[1]] for path in paths]

    # Create directories in the destination path
    for dest_path, src_path in full_renamed_paths:
        if not os.path.isfile(src_path):
            if log_functions:
                print_et(
                    f"Created folder:\n|- From: [{src_path}]\n|- To:   [{dest_path}]")
            os.makedirs(dest_path, exist_ok=True)

    # Copy files to the destination path
    if not ignore_files:
        for dest_path, src_path in full_renamed_paths:
            if os.path.isfile(src_path):
                if overwrite_files or not os.path.exists(dest_path):
                    try:
                        if log_functions:
                            print_et(
                                f"Copied file:\n|- From: [{src_path}]\n|- To:   [{dest_path}]")
                        shutil.copyfile(src_path, dest_path)
                    except Exception as e:
                        print_et(f"Error copying {src_path} to {dest_path}: {e}")


def read_file(path: str) -> str:
    """
    Reads the content of a file and returns it as a string.

    :param path: The path to the file to be read.
    :return: A string containing the file's content.
    """
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        print_et(f"Error reading file {path}: {e}")
        return ""


def write_file(path: str, content: str):
    """
    Writes a string content to a file.

    :param path: The path to the file where content will be written.
    :param content: The string content to write to the file.
    :return: None
    """
    try:
        with open(path, "w") as file:
            file.write(content)
    except Exception as e:
        print_et(f"Error writing to file {path}: {e}")


def read_json_file(path: str) -> dict:
    """
    Reads a JSON file and returns the content as a dictionary.

    :param path: The path to the JSON file to be read.
    :return: A dictionary representing the JSON content.
    """
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        print_et(f"Error reading JSON file {path}: {e}")
        return {}


def write_json_file(path: str, content: dict):
    """
    Writes a dictionary to a JSON file.

    :param path: The path to the file where the JSON content will be written.
    :param content: A dictionary containing the data to write to the JSON file.
    :return: None
    """
    try:
        with open(path, "w") as file:
            json.dump(content, file, indent=4)
    except Exception as e:
        print_et(f"Error writing JSON file {path}: {e}")


def sanitize_file_folder_name(name: str) -> str:
    """
    Sanitizes a file or folder's name by removing invalid characters and trimming spaces.

    :param name: The original name to sanitize.
    :return: A sanitized version of the name.
    """
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', name).strip()
    return sanitized_name


def open_explorer_to_path(path: str):
    """
    Opens the specified path in the system's file explorer.

    :param path: The path to open in the file explorer.
    :return: None
    """
    try:
        subprocess.Popen(['explorer', path])
    except Exception as e:
        print_et(f"Error opening path {path}: {e}")


def get_toplevel_paths(dir_list: list[str]) -> list[str]:
    """
    Returns the top-level directories from a list, excluding subdirectories.

    :param dir_list: A list of directory paths to evaluate.
    :return: A list of top-level directory paths.
    """
    dir_list = sorted([os.path.normpath(dir) for dir in dir_list], key=len)
    result = []

    for i, current_dir in enumerate(dir_list):
        if not any(current_dir.startswith(other + os.sep) for j, other in enumerate(dir_list) if i != j):
            result.append(current_dir)

    return result
