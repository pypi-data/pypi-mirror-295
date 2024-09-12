import os
import sys

# First function to print the full directory structure (always shown)
def print_full_directory_structure(path, indent_level=0, ignore_list=None, output_file=None):
    items = os.listdir(path)

    if ignore_list is None:
        ignore_list = []

    for item in items:
        if item in ignore_list:
            continue  # Skip items that are in the ignore list

        item_path = os.path.join(path, item)
        line = ' ' * indent_level + '|-- ' + item
        print(line)

        if output_file:
            output_file.write(line + "\n")

        # Recursively explore subdirectories
        if os.path.isdir(item_path):
            print_full_directory_structure(item_path, indent_level + 4, ignore_list, output_file)

# Second function to append the contents of files (only for specified directories)
def write_file_contents(path, ignore_list=None, output_file=None, full_explore_list=None):
    items = os.listdir(path)

    if ignore_list is None:
        ignore_list = []

    if full_explore_list is None:
        full_explore_list = []

    for item in items:
        if item in ignore_list:
            continue  # Skip items that are in the ignore list

        item_path = os.path.join(path, item)

        # Write only the contents of the files in the full_explore_list
        if any(os.path.basename(path_set) in item for path_set in full_explore_list):
            if os.path.isfile(item_path) and output_file:
                output_file.write("\n" + "-" * 40 + "\n")
                output_file.write(f"Content of {item}:\n\n")
                try:
                    with open(item_path, 'r') as file:
                        output_file.write(file.read())
                except Exception as e:
                    output_file.write(f"Error reading file {item}: {e}")
                output_file.write("\n" + "-" * 40 + "\n\n")

            # Recursively explore subdirectories for files
            elif os.path.isdir(item_path):
                write_file_contents(item_path, ignore_list, output_file, full_explore_list)

# Function to handle writing both structure and content in two phases
def write_structure_and_contents(directory_path, ignore_list, output_filename, full_explore_list):
    with open(output_filename, 'w') as f:
        # First, print the full directory structure (but don't write contents)
        print_full_directory_structure(directory_path, ignore_list=ignore_list, output_file=f)

        # Then, write the contents of the files only for specified directories
        write_file_contents(directory_path, ignore_list=ignore_list, output_file=f, full_explore_list=full_explore_list)

# Parse full explore list if provided
def parse_full_explore_list(explore_input):
    full_explore_list = []
    if explore_input:
        # Split by commas to allow multiple directories/files
        for path in explore_input.split(','):
            full_explore_list.append(path.strip())
    return full_explore_list

# Default files and directories to ignore
default_ignore_list = ['venv', '__pycache__', '.git']

# Get the list of command-line arguments
args = sys.argv[1:]

# Check if -w flag is present for writing output to a file
write_mode = '-w' in args

# If -w is present, remove it from args and get the filename to write
if write_mode:
    args.remove('-w')
    output_filename = "directory_structure_and_contents.txt"

# Handle the explore option
explore_index = None
if '--explore' in args:
    explore_index = args.index('--explore')
    full_explore_input = args[explore_index + 1]  # The user-provided directories to fully explore
    args = args[:explore_index]  # Remove explore part from args
    full_explore_list = parse_full_explore_list(full_explore_input)
else:
    # If no explore option is given, set full_explore_list to None, meaning fully explore everything
    full_explore_list = None

# The remaining args are additional files and directories to ignore
ignore_list = default_ignore_list + args

# Use current working directory if no path is provided
directory_path = os.getcwd()

# If write_mode is enabled, write the structure and contents to the output file
if write_mode:
    write_structure_and_contents(directory_path, ignore_list, output_filename, full_explore_list)
    print(f"\nDirectory structure and contents written to {output_filename}")
else:
    # Just print the directory structure if -w flag is not provided
    print_full_directory_structure(directory_path, ignore_list=ignore_list)
