import os
import sys

# First function to print the directory structure
def print_directory_structure(path, indent_level=0, ignore_list=None, output_file=None, full_explore_list=None):
    items = os.listdir(path)

    if ignore_list is None:
        ignore_list = []

    if full_explore_list is None:
        full_explore_list = []

    for item in items:
        if item in ignore_list:
            continue  # Skip items that are in the ignore list

        item_path = os.path.join(path, item)

        line = ' ' * indent_level + '|-- ' + item
        print(line)

        if output_file:
            output_file.write(line + "\n")

        # If it's a directory, decide whether to fully explore or just show its name
        if os.path.isdir(item_path):
            # Fully explore if no explore list is specified or if the current directory is in the explore list
            if not full_explore_list or any(item in path_set for path_set in full_explore_list):
                print_directory_structure(item_path, indent_level + 4, ignore_list, output_file, full_explore_list)
            else:
                # If it's not in the explore list, just show the directory name and move on
                continue

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

        # If no full_explore_list is provided, write all file contents
        def is_explored_directory(current_path):
            if not full_explore_list:  # If explore list is empty, include all
                return True
            path_parts = os.path.abspath(current_path).split(os.sep)
            return any(dir_name in path_parts for dir_name in full_explore_list) or \
                   any(current_path.startswith(os.path.join(path, *path_set)) for path_set in full_explore_list)

        # If it's a file and its directory is marked for exploration (or no list is provided), write its content
        if os.path.isfile(item_path):
            if output_file and is_explored_directory(item_path):
                output_file.write("\n" + "-" * 40 + "\n")
                output_file.write(f"Content of {item}:\n\n")
                try:
                    with open(item_path, 'r') as file:
                        output_file.write(file.read())
                except Exception as e:
                    output_file.write(f"Error reading file {item}: {e}")
                output_file.write("\n" + "-" * 40 + "\n\n")

        # If it's a directory, recursively explore further if it matches the explore criteria
        elif os.path.isdir(item_path):
            if is_explored_directory(item_path):
                write_file_contents(item_path, ignore_list, output_file, full_explore_list)


def write_structure_and_contents(directory_path, ignore_list, output_filename, full_explore_list):
    with open(output_filename, 'w') as f:
        f.write("Directory Structure:\n\n")
        print_directory_structure(directory_path, ignore_list=ignore_list, output_file=f, full_explore_list=full_explore_list)
        f.write("\n\nFile Contents:\n\n")
        write_file_contents(directory_path, ignore_list=ignore_list, output_file=f, full_explore_list=full_explore_list)

def parse_full_explore_list(explore_input):
    full_explore_list = []
    if explore_input:
        entries = explore_input.split(',')
        for entry in entries:
            path_components = entry.strip().split('/')
            if len(path_components) > 1:
                full_explore_list.append(path_components)
            else:
                full_explore_list.append(entry.strip())
    return full_explore_list

def main():
    default_ignore_list = ['venv', '__pycache__', '.git']
    args = sys.argv[1:]

    write_mode = '-w' in args
    if write_mode:
        args.remove('-w')
        output_filename = "structure.txt"

    explore_index = None
    if '--explore' in args:
        explore_index = args.index('--explore')
        full_explore_input = args[explore_index + 1]
        args = args[:explore_index]
        full_explore_list = parse_full_explore_list(full_explore_input)
    else:
        full_explore_list = None

    ignore_list = default_ignore_list.copy()

    # Handle --ignore flag
    if '--ignore' in args:
        ignore_index = args.index('--ignore')
        ignore_input = args[ignore_index + 1]
        ignore_list += ignore_input.split(',')
        args = args[:ignore_index]  # Remove the --ignore and its argument

    ignore_list += args
    directory_path = os.getcwd()

    if write_mode:
        if full_explore_list is None:  # If no --explore flag, write everything
            full_explore_list = []  # Empty list means fully explore everything

        write_structure_and_contents(directory_path, ignore_list, output_filename, full_explore_list)
        print(f"\nDirectory structure and contents written to {output_filename}")
    else:
        print_directory_structure(directory_path, ignore_list=ignore_list, full_explore_list=full_explore_list)

if __name__ == '__main__':
    main()