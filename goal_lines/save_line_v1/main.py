import json
import os
import sys

def is_python_file(file):
    """
    Check if a given file is a Python file.

    Args:
        file (str): Path to the file.

    Returns:
        bool: True if the file ends with .py, otherwise False.
    """
    if os.path.isfile(file):
        return file.endswith('.py')
    return False


def is_valid_line(line):
    """
    Determine if a line of code is valid (not a comment, string, or empty).

    Args:
        line (str): Code line to check.

    Returns:
        bool: True if the line is valid, otherwise False.
    """
    line = line.strip()
    if line.startswith("#") or line.startswith(("'", '"')) or not line:
        return False
    return True


def count_lines_in_file(path):
    """
    Count valid lines in a file or directory. Supports recursive traversal for directories.

    Args:
        path (str): Path to the file or directory.

    Returns:
        int: Total number of valid lines.
    """
    total_lines = 0

    if os.path.isfile(path):
        with open(path, 'r') as f:
            while line := f.readline():
                if is_valid_line(line):
                    total_lines += 1

    elif os.path.isdir(path):
        ignored_dirs = {'.git', '__pycache__'}
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            for file in files:
                filepath = os.path.join(root, file)
                if is_python_file(filepath):
                    total_lines += count_lines_in_file(filepath)

    return total_lines


def inizialize_data(filepath):
    """
    Initialize data for a given file or directory.

    Args:
        filepath (str): Path to the file or directory.

    Returns:
        dict: Dictionary containing initialized data.
    """
    data = {
        'total_lines': 0,
        'files': {},
        'directory': {}
    }

    if os.path.isfile(filepath):
        new_lines = count_lines_in_file(filepath)
        data['total_lines'] += new_lines
        data['files'][filepath] = new_lines

    elif os.path.isdir(filepath):
        new_lines = count_lines_in_file(filepath)
        data['total_lines'] += new_lines
        data['directory'][filepath] = new_lines

    return data


def save_data(filename, data):
    """
    Save data to a JSON file.

    Args:
        filename (str): Name of the file to save data to.
        data (dict): Data to be saved.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except FileNotFoundError:
        print(f'File {filename} not found')

def load_data(filepath):
    """
    Load data from a JSON file.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict or None: Loaded data or None if the file is invalid.
    """
    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, 'r') as file:
            if os.path.getsize(filepath) == 0:
                print(f"{filepath} is empty.")
                return None
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        print(f"The file {filepath} contains invalid JSON data.")
        return None
    

def is_new_data_exist(data, new_file):
    """
    Check if a file or directory is already recorded in the data.

    Args:
        data (dict): Current data.
        new_file (str): Path to the file or directory to check.

    Returns:
        bool: True if the file/directory is already recorded, otherwise False.
    """
    return new_file in data.get('files', {}) or new_file in data.get('directory', {})


def is_data_change(data, new_path):
    """
    Check if the data for a file or directory has changed.

    Args:
        data (dict): Current data.
        new_path (str): Path to the file or directory.

    Returns:
        bool: True if the data has changed, otherwise False.
    """
    new_data_lines = count_lines_in_file(new_path)

    if os.path.isfile(new_path):
        old_data_lines = data['files'][new_path]
    elif os.path.isdir(new_path):
        old_data_lines = data['directory'][new_path]

    return old_data_lines != new_data_lines


def add_new_data_in_file(filename, new_path):
    """
    Add or update data for a new file or directory.

    Args:
        filename (str): Name of the JSON file to save data to.
        new_path (str): Path to the file or directory.

    Returns:
        str: Message indicating the result of the operation.
    """
    data_in_file = load_data(filename)
    new_data_lines = count_lines_in_file(new_path)
    msg = ''

    if data_in_file is not None:
        if is_new_data_exist(data_in_file, new_path):
            if is_data_change(data_in_file, new_path):
                if os.path.isfile(new_path):
                    old_data_lines = data_in_file['files'][new_path]
                    data_in_file['total_lines'] += new_data_lines - old_data_lines
                    data_in_file['files'][new_path] = new_data_lines

                elif os.path.isdir(new_path):
                    old_data_lines = data_in_file['directory'][new_path]
                    data_in_file['total_lines'] += new_data_lines - old_data_lines
                    data_in_file['directory'][new_path] = new_data_lines
                save_data(filename, data_in_file)
                msg = f"Data updated in {filename}"
            else:
                msg = f"No changes detected"

        else:
            if os.path.isfile(new_path):
                data_in_file['total_lines'] += new_data_lines
                data_in_file['files'][new_path] = new_data_lines

            elif os.path.isdir(new_path):
                data_in_file['total_lines'] += new_data_lines
                data_in_file['directory'][new_path] = new_data_lines
            save_data(filename, data_in_file)
            msg = f"Data saved in file {filename}"

    else:
        data_initialized = inizialize_data(new_path)
        save_data(filename, data_initialized)
        msg = f"Data initialized and saved in {filename}"

    return msg


def check_valid_args(paths):
    """
    Check if the provided arguments are valid (Python files or directories).

    Args:
        paths (list): List of paths to check.

    Returns:
        bool: True if all paths are valid, otherwise False.
    """
    return all((is_python_file(path) or os.path.isdir(path) for path in paths))


def main(args):
    """
    Main function to handle command-line arguments.

    Args:
        args (list): List of arguments passed via command line.
    """
    if len(args) < 1:
        sys.exit('Too few arguments!')

    elif not check_valid_args(args):
            print("Not all provided paths are valid Python files or directories!")
            sys.exit(1)

            
    filename = 'save_lines.json'
    data_in_file = load_data(filename)

    if data_in_file is not None:
        for f in args:
            msg = add_new_data_in_file(filename, f)
        print(msg)

    else:
        for f in args:
            msg = add_new_data_in_file(filename, f)
        print(f"Initialization: {msg}")

if __name__ == "__main__":
    main(sys.argv[1:])
