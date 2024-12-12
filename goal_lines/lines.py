import sys

if len(sys.argv) < 2:
    sys.exit("Too few command-line arguments !")

if len(sys.argv) > 2:
    sys.exit("Too many command-line arguement !")

if not sys.argv[1].endswith('.py'):
    sys.exit("Not a python file !")

total_line_goal = 0

try:
    with open(sys.argv[1], 'r') as f:
        total_line = 0
        for line in f:
            line = line.lstrip() # remove starts line with white space
            if not line.startswith("# ") and len(line) != 0:
                total_line += 1
    print(f"{sys.argv[1]} contains {total_line}")
except FileNotFoundError:
    sys.exit("File not found")

total_line_goal += total_line
if total_line_goal < 1000:
    print(f"total lines goal : {total_line_goal}")
