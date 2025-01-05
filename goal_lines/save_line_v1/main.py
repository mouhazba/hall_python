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
    if os.path.isfile(path):
        with open(path, 'r') as f:
            while line:= f.readline():
                if is_valid_line(line):
                    total_lines += 1

    elif os.path.isdir(path):
        """Parcourt un dossier et compte les lignes dans tous les fichiers Python."""
        ignored_dirs = {'.git', '__pycache__'}  # Liste des répertoires à ignorer
        for root, dirs, files in os.walk(path):
            for pathfile in files:
                # Supprimer les répertoires à ignorer de la liste des sous-dossiers
                dirs[:] = [d for d in dirs if d not in ignored_dirs]
                filepath = os.path.join(root, pathfile)
                if is_python_file([filepath]):
                    if is_valid_line(filepath):
                        total_lines += count_lines_in_file(filepath) # appel recursif pour ne pas repeter le 1er bloc if
    return total_lines


def inizialize_data(filepath):
    data = {}
    data['total_lines'] = 0
    data['files'] = {}
    data['directory'] = {}

    
    if os.path.isfile(filepath):
        new_lines = count_lines_in_file(filepath)
        data['total_lines'] += new_lines
        data['files'][filepath] = new_lines
        
    elif os.path.isdir(filepath):
        #new_lines = count_lines_in_directory(filepath)
        new_lines = count_lines_in_file(filepath)
        data['total_lines'] += new_lines
        data['directory'][filepath] = new_lines

    return data


def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Les données ont été sauvegardées dans '{filename}'.")
    except FileNotFoundError:
        print('File {filename} not found')


def load_data(filepath):
    # Vérifier si le fichier existe
    if not os.path.exists(filepath):
        return None

    try:
        # Charger le contenu du fichier JSON
        with open(filepath, 'r') as file:
            # Vérifier si le fichier est vide
            if os.path.getsize(filepath) == 0:
                print(f"Le fichier '{filepath}' est vide.")
                return None
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        print(f"Le fichier '{filepath}' contient des données JSON invalides.")
        return None


def is_new_data_exist(data, new_file):
    if new_file in data.get('files', {}) or new_file in data.get('directory', {}):
        return True
    else:
        False

def is_data_change(data, new_path):
    if os.path.isfile(new_path):
        new_data_lines = count_lines_in_file(new_path)
        old_data_lines = data['files'][new_path]

    elif os.path.isdir(new_path):
        new_data_lines = count_lines_in_file(new_path)
        old_data_lines = data['directory'][new_path]
    return old_data_lines != new_data_lines


def update_data(filename, new_path):
    if os.path.isfile(new_path):
        new_data_lines = count_lines_in_file(new_path)
        data = load_data(filename)
        old_data_lines = data['files'][new_path]
        data['total_lines'] += new_data_lines - old_data_lines
        data['files'][new_path] = new_data_lines

    elif os.path.isdir(new_path):
        new_data_lines = count_lines_in_file(new_path)
        data = load_data(filename)
        old_data_lines = data['directory'][new_path]
        data['total_lines'] += new_data_lines - old_data_lines
        data['directory'][new_path] = new_data_lines
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Les données ont été bien mises a jour dans '{filename}'.")
    except FileNotFoundError:
        print(f'File {filename} not found')


def add_new_data_in_file(filename, new_path):
    if os.path.isfile(new_path):
        new_data_lines = count_lines_in_file(new_path)
        data = load_data(filename)
        data['total_lines'] += new_data_lines
        data['files'][new_path] = new_data_lines
    
    elif os.path.isdir(new_path):
        new_data_lines = count_lines_in_file(new_path)
        data = load_data(filename)
        data['total_lines'] += new_data_lines
        data['directory'][new_path] = new_data_lines

    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{new_path} a bien été ajoute dans '{filename}'.")
    except FileNotFoundError:
        print('File {filepath} not found')

def global_check_and_save_data(filename,paths):
    data_in_file = load_data(filename)
    if len(paths) == 1:  # Si un seul élément est fourni

        path = paths[0]
        if is_python_file([path]):
    
            if data_in_file != None:
                if is_new_data_exist(data_in_file, path):
                    if is_data_change(data_in_file, path):
                        update_data(filename, path)
                    else:
                        print('Aucun change note')
                else:
                    add_new_data_in_file(filename, path)
            else:
                data_iniatial = inizialize_data(path)
                save_data(filename, data_iniatial)
                print('Data initialized')
                

        elif os.path.isdir(path):
            if data_in_file != None:
                if is_new_data_exist(data_in_file, path):
                    if is_data_change(data_in_file, path):
                        update_data(filename, path)

                    else:
                        print('Aucun changement')
                else:
                    add_new_data_in_file(filename, path)
                    
                    
            else:
                data_iniatial = inizialize_data(path)
                save_data(filename, data_iniatial)
                print('Data initialized')

        else:
            print(f"'{path}' is not a Python file or a directory.")


    else:
        # Si plusieurs chemins sont fournis, vérifier qu'ils sont tous des fichiers Python
        if is_python_file(paths):
            if data_in_file != None:
                is_something_change = False
                is_something_added = False
                for f in paths:
                    if is_new_data_exist(data_in_file, f):
                        if is_data_change(data_in_file, f):
                            update_data(filename, f)
                            is_something_change = True
                    
                    else:
                        add_new_data_in_file(filename, f)
                        is_something_added = True
                if not is_something_change and not is_something_added:
                    print('Aucun changement note')

            else:
                data_iniatial = inizialize_data(paths[0])
                save_data(filename, data_iniatial)
                for f in paths[1:]:
                    add_new_data_in_file(filename, f)
        else:
            print("Not all provided files are Python files!")

def main():
    if len(sys.argv) < 2:
        sys.exit('Too few arguments!')

    filename = 'save_lines.json'

    paths = sys.argv[1:]
    global_check_and_save_data(filename, paths)    
  

if __name__ == "__main__":
    main()

