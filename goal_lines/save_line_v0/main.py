import sys
import os

# import ast


def validation_arguements():
    """Validate command-line arguements."""
    if len(sys.argv) != 2:
        sys.exit("Usage: python file <file.py>")
    file_path = sys.argv[1]
    """ 
    if not file_path.endswith(".py"):
        sys.exit("Expected a python file")
    """
    _, extension = os.path.splitext(file_path)
    if extension != ".py":
        sys.exit("Expected a python file")


def is_valid_line(line):
    """Return False for empty lines, comments, or lines starting with quotes.
    args:
        line(str): a line of code
    return:
        True if the line is valid, False otherwise
    """
    stripped_line = line.strip()
    return not (
        stripped_line.startswith("#")
        or stripped_line.startswith(("'", '"'))
        or not stripped_line
    )


def count_valid_lines(filename):
    """Count valid lines in a Python file.
    args:
        filename(str): the name of the file to count lines
    return:
        the number of valid lines in the file or -1 if the file does not exist"""

    with open(filename, "r", encoding="utf-8") as f:
        return sum(1 for line in f if is_valid_line(line))



    """
        total_valid_lines = 0
        for line in f:
            if is_valid_line(line):
                total_valid_lines += 1

    return total_valid_lines"""



# os.path.exists(filepath) check if the file exists and is a file, not a directory
# os.path.isfile(filepath) check if the file exists and is a file, not a directory, and is accessible (i.e., the user has permission to read the file)


def read_file_content(filepath):
    """Return file content."""
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def save_data(file, data):
    """this function save data to a file
    args:
        file(str): the name of the file to save
        data(str): the data to save
        data should be a dictionary that contains the number of valid lines for each file and the total number of valid lines
    return:
        None
    """

    with open(file, "w") as f:
            f.write(str(data))


def is_file_in_data(data, file_target):
    data_eval = eval(data)  # eval data to a dictionary
    keys_data = [key for key in data_eval.keys()]
    
    return file_target in keys_data[1:]


def update_data(filepath, file_data, file_target):
    file_data_eval = eval(file_data)
    keys_data = [key for key in file_data_eval.keys()]
 

    if file_target in keys_data[1:]:  # redondance use the func is_file_in_data
        old_total_file_lines = file_data_eval[file_target]  # get old total lines for this file
        new_total_lines = count_valid_lines(file_target)
        if new_total_lines != None:
            if diff := new_total_lines - old_total_file_lines: # if there is a difference between the old total lines and the new total lines, update the total valid lines and the total lines for this file
                file_data_eval["total_valid_lines"] += diff
                file_data_eval[file_target] = new_total_lines
                save_data(filepath, file_data_eval)
                print(f"File {file_target} is successfully updated with {diff} new lines")
            else:
                print(f"No changes detected for file {file_target}")


def main(file_target):
    name_file_store = "save_lines_v0.txt"
    try:
        data = read_file_content(name_file_store) # data is a dictionary that contains the number of valid lines for each file and the total number of valid lines
    except FileNotFoundError:
        data = None


    if  data == None:
        """Initialization"""
        new_data = {}
        try:
            total_valid_lines = count_valid_lines(file_target)
        except FileNotFoundError:
            sys.exit(f"File {file_target} not found or cannot be read")
 
        new_data["total_valid_lines"] = total_valid_lines
        new_data[file_target] = total_valid_lines
        try:
            save_data(name_file_store, new_data)
            print(f"File {file_target} is successfully saved")
        except IOError as e:
            sys.exit(f"Error occurred while saving data for file {file_target}: {e}")

    else:
        """this data exists in file"""
        if is_file_in_data(data, file_target):
            try:
                update_data(name_file_store, data, file_target)
            except FileNotFoundError as e:
                sys.exit(f"Error occurred while updating data for file {file_target}: {e}")

        else:
            """New data to add in file"""
            data_eval = eval(data) # eval data to a dictionary
            try:
                new_total_lines = count_valid_lines(file_target)
            except FileNotFoundError:
                sys.exit(f"File {file_target} not found or cannot be read")
            data_eval["total_valid_lines"] += new_total_lines
            data_eval[file_target] = new_total_lines
            try:
                save_data(name_file_store, data_eval)
                print(f"File {file_target} is successfully saved")
            except IOError as e:
                sys.exit(f"Error occurred while saving data for file {file_target}: {e}")


if __name__ == "__main__":
    validation_arguements()
    main(sys.argv[1])

