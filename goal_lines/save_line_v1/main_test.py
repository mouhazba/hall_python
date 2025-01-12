import json
import os
import sys


def is_python_file(files):
    return all(f.endswith('.py') and os.path.isfile(f) for f in files)


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
                if is_python_file([filepath]):
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
        print(f"{data} saved in file {filename}'.")
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


def update_data(filename, new_path):
    #with file
    if os.path.isfile(new_path):
        new_data_lines = count_lines_in_file(new_path)
        data = load_data(filename)
        old_data_lines = data['files'][new_path]
        data['total_lines'] += new_data_lines - old_data_lines
        data['files'][new_path] = new_data_lines

    #with directory
    elif os.path.isdir(new_path):
        new_data_lines = count_lines_in_file(new_path)
        data = load_data(filename)
        old_data_lines = data['directory'][new_path]
        data['total_lines'] += new_data_lines - old_data_lines
        data['directory'][new_path] = new_data_lines

    save_data(filename, data)


def add_new_data_in_file(filename, new_path):
    data = load_data(filename)

    #with file
    if os.path.isfile(new_path):
        new_data_lines = count_lines_in_file(new_path)
        if is_new_data_exist(data, new_path):
            data['total_lines'] += new_data_lines
            
        else:
            old_data_lines = data['files'][new_path]
            data['total_lines'] += new_data_lines - old_data_lines
        data['files'][new_path] = new_data_lines

    #with directory
    elif os.path.isdir(new_path):
        new_data_lines = count_lines_in_file(new_path)
        data['total_lines'] += new_data_lines
        data['directory'][new_path] = new_data_lines
    save_data(filename, data)


def global_check_and_save_data(filename,paths):
    data_in_file = load_data(filename)
    msg = ''
    for path in paths:
        if is_python_file([path]):
            
            if data_in_file != None:
                if is_new_data_exist(data_in_file, path):
                    if is_data_change(data_in_file, path):
                        update_data(filename, path)
                    else:
                        msg = 'Aucun change note'
                        #print('Aucun change note')
                else:
                    add_new_data_in_file(filename, path)
            else:
                data_iniatial = inizialize_data(path)
                save_data(filename, data_iniatial)
                msg = 'Data initialized'
                #print('Data initialized')


        elif os.path.isdir(path):
            if data_in_file != None:
                if is_new_data_exist(data_in_file, path):
                    if is_data_change(data_in_file, path):
                        update_data(filename, path)

                    else:
                        msg = 'Aucun change note'
                        #print('Aucun changement')
                else:
                    add_new_data_in_file(filename, path)
                      
            else:
                data_iniatial = inizialize_data(path)
                save_data(filename, data_iniatial)
                #print('Data initialized')


        else:
            msg = f'{path} is not a Python file or a directory.'
            #print(f"'{path}' is not a Python file or a directory.")
    print(msg)

def main(args):
    if len(args) < 1:
        sys.exit('Too few arguments!')

    filename = 'save_lines.json'
    global_check_and_save_data(filename, args)    
  

if __name__ == "__main__":
    main(sys.argv[1:])



# revoir le code des chose euvent encore factoriser