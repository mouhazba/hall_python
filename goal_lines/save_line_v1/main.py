import json
import os
import sys


def is_python_file(file):
    if os.path.isfile(file):
        return file.endswith('.py')
    return False



def is_valid_line(line):
    line = line.strip()
    if line.startswith("#") or line.startswith(("'", '"')) or not line:
        return False
    return True


def count_lines_in_file(path):
    total_lines = 0
    #with files
    if os.path.isfile(path):
        with open(path, 'r') as f:
            while line:= f.readline():
                if is_valid_line(line):
                    total_lines += 1

    #with directories
    elif os.path.isdir(path):
        """count lines of Python files  recursively in a folder."""
        ignored_dirs = {'.git', '__pycache__'}
        for root, dirs, files in os.walk(path):
            for pathfile in files:
                # list of files to ignore
                dirs[:] = [d for d in dirs if d not in ignored_dirs]
                filepath = os.path.join(root, pathfile)
                if is_python_file(filepath):
                    if is_valid_line(filepath):
                        total_lines += count_lines_in_file(filepath) #count_lines_in_file() called
    return total_lines


def inizialize_data(filepath):
    data = {}
    data['total_lines'] = 0
    data['files'] = {}
    data['directory'] = {}
    
    #with files
    if os.path.isfile(filepath):
        new_lines = count_lines_in_file(filepath)
        data['total_lines'] += new_lines
        data['files'][filepath] = new_lines
        
    #with directories
    elif os.path.isdir(filepath):
        new_lines = count_lines_in_file(filepath)
        data['total_lines'] += new_lines
        data['directory'][filepath] = new_lines

    return data


def save_data(filename, data):
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except FileNotFoundError:
        print('File {filename} not found')


def load_data(filepath):
    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, 'r') as file:
            # check if file is empty
            if os.path.getsize(filepath) == 0:
                print(f"{filepath} is empty.")
                return None
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        print(f"The file {filepath} contains invalid format JSON's data.")
        return None


def is_new_data_exist(data, new_file):
    #use any() instead
    if new_file in data.get('files', {}) or new_file in data.get('directory', {}):
        return True
    else:
        False

def is_data_change(data, new_path):
    # check in files
    if os.path.isfile(new_path):
        new_data_lines = count_lines_in_file(new_path)
        old_data_lines = data['files'][new_path]

    # check in directories
    elif os.path.isdir(new_path):
        new_data_lines = count_lines_in_file(new_path)
        old_data_lines = data['directory'][new_path]
        
    return old_data_lines != new_data_lines



def add_new_data_in_file(filename, new_path):
    data_in_file = load_data(filename)
    new_data_lines = count_lines_in_file(new_path)
    msg = ''
    if data_in_file != None:
        #update file
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
                msg = f"data updated in  {filename}"
            else:
                msg = f"No change"

        else:
            #add new file
            if os.path.isfile(new_path):
                data_in_file['total_lines'] += new_data_lines
                data_in_file['files'][new_path] = new_data_lines

            elif os.path.isdir(new_path):
                data_in_file['total_lines'] += new_data_lines
                data_in_file['directory'][new_path] = new_data_lines
            save_data(filename, data_in_file)
            msg = f"data saved in file {filename}"

        return msg

    else:
        data_inialized = inizialize_data(new_path)
        save_data(filename, data_inialized)
        return f"data saved in  {filename}"     

def check_valid_args(paths):
    return all((is_python_file(path) or os.path.isdir(path) for path in paths))


def main(args):
    if len(args) < 1:
        sys.exit('Too few arguments!')

    filename = 'save_lines.json'
    data_in_file = load_data(filename)
    if data_in_file != None:
        for f in args:
            msg = add_new_data_in_file(filename, f)
        print(msg)
    
    else:
        if not check_valid_args(args):
            print("Not all provided files are Python files!")
            sys.exit(1)
        for f in args:
            msg = add_new_data_in_file(filename, f)
        print(f"Inialization: {msg}")

if __name__ == "__main__":
    main(sys.argv[1:])



