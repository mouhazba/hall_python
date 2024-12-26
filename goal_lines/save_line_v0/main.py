import sys, os
#import ast



if len(sys.argv) != 2:
    sys.exit("Argument name file expected !")

if not sys.argv[1].endswith('.py'):
    sys.exit("Not a Python file!")

def valid_lines(line):
    line = line.strip()
    if line.startswith("#") or line.startswith(("'", '"')) or not line:
        return False
    return True


def count_lines(filename):
    try:
        with open(filename, 'r') as f:
            total = 0
            for line in f:  
                if valid_lines(line):
                    total += 1
            return total
        
    except FileNotFoundError:
        sys.exit("File not found")


def is_file_exist(filepath):
    return os.path.exists(filepath)


def load_data(filepath):
    if is_file_exist(filepath):
        with open(filepath, 'r') as f:
            return f.read()
        

def save_data(file, data):
    with open(file, 'w') as f:
        f.write(str(data))


def is_data_in_file(data):
    data_eval  = eval(data)
    keys_data = [key for key in data_eval.keys()]
    new_data = sys.argv[1]
    return new_data in keys_data
    

def update_data(filepath, data):
    data_eval  = eval(data)
    keys_data = [key for key in data_eval.keys()]
    new_data = sys.argv[1]
 
    if new_data in keys_data[1:]:
        old_total_lines = data_eval[new_data]
        new_total_lines = count_lines(new_data)

        if diff:= new_total_lines - old_total_lines:
            data_eval['total_lines'] += diff
            data_eval[new_data] = new_total_lines
            save_data(filepath, data_eval)
            

namefile = "save_lines_v0.txt"
data = load_data(namefile)
if data:
    """this data exists in file"""
    if is_data_in_file(data):
        update_data(namefile, data)

    else:
        """New data"""
        data_eval  = eval(data)
        new_total_lines = count_lines(sys.argv[1])
        data_eval['total_lines'] += new_total_lines
        data_eval[sys.argv[1]] = new_total_lines
        save_data(namefile, data_eval)
else:
    """Initialization"""
    new_data = {}
    new_data['total_lines'] = count_lines(sys.argv[1])
    new_data[sys.argv[1]] = count_lines(sys.argv[1])
    save_data(namefile, new_data)

