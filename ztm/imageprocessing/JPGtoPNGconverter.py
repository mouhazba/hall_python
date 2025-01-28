import sys
import os
from PIL import Image

# Get the input path (source directory) and output directory from command-line arguments
path = sys.argv[1]
directory = sys.argv[2]

# Create the output directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Iterate through all files in the source directory
for filename in os.listdir(path):
    # Remove the file extension from the filename
    clean_name = os.path.splitext(filename)[0] 
    # Open the image file
    img = Image.open(f'{path}{filename}')

    # Save the image in the output directory as a PNG file
    img.save(f'{directory}/{clean_name}.png', 'png')
    print('all done!')