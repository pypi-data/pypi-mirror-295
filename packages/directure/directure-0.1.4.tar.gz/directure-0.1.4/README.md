
# Directure = Directory + Structure

**Motivation**  
I created this tool after struggling to explain project structures and errors to ChatGPT. It was difficult to clearly communicate my project's directory structure and file contents. With this tool, you can easily generate a visual representation of your project's directory structure, including file contents if desired, which can then be shared or used to debug with AI models like ChatGPT.

## Features
- **Visualize Directory Structure**: Print the entire directory structure of your project.
- **Include File Contents**: Optionally append the contents of specific files or directories to the output for detailed exploration.
- **Ignore List**: Specify files and folders to ignore while exploring the structure.
- **Full Explore List**: Define directories for detailed exploration and file content output.
- **Write Output to File**: Generate an output file containing the directory structure and selected file contents.

## Usage

Run `directure.py` from the command line with several options:

```bash
python directure.py [options]
```

### Options:

- `-w`: Writes the directory structure and contents to an output file `structure.txt`.
- `--explore "path/to/directory"`: Limits exploration to a specific directory or set of directories/files.
- Directories or files can be ignored by listing them after the main command.

## Example Usage

Given the following sample directory structure:

```
project_root/
│-- src/
│   │-- app.py
│   │-- utils.py
│-- docs/
│   │-- README.md
│-- tests/
    │-- test_app.py
    │-- test_utils.py
```

### 1. Default Behavior:

Running the script with no additional flags will print the entire directory structure, ignoring the default ignore list (e.g., `venv`, `__pycache__`, `.git`).

```bash
python directure.py
```

Output:

```
|-- project_root
    |-- src
        |-- app.py
        |-- utils.py
    |-- docs
        |-- README.md
    |-- tests
        |-- test_app.py
        |-- test_utils.py
```

### 2. Writing Output to File:

You can save the structure and file contents into a file by using the `-w` flag.

```bash
python directure.py -w
```

This will create `structure.txt` in the current directory, containing:

```
Directory Structure:

|-- project_root
    |-- src
        |-- app.py
        |-- utils.py
    |-- docs
        |-- README.md
    |-- tests
        |-- test_app.py
        |-- test_utils.py


File Contents:

----------------------------------------
Content of app.py:

<file content>

----------------------------------------
Content of utils.py:

<file content>

----------------------------------------
Content of README.md:

<file content>

----------------------------------------
Content of test_app.py:

<file content>

----------------------------------------
Content of test_util.py:

<file content>

...
```

### 3. Exploring a Specific Directory:

To explore only a specific directory or file, use the `--explore` flag followed by the directory path. For example:

```bash
python directure.py --explore "src"
```

Output:

```
|-- project_root
    |-- src
        |-- app.py
        |-- utils.py
    |-- docs
    |-- tests
```

### 4. Exploring a Directory and Writing to File:

You can combine the `--explore` flag with the `-w` flag to write the structure and contents of the explored directory to the output file.

```bash
python directure.py --explore "src" -w
```

This will create or overwrite the `structure.txt` file with the content from the `src` directory only.

---

## Default Ignore List

By default, the following directories and files are ignored:

- `venv`
- `__pycache__`
- `.git`

You can extend this list by adding items as arguments when running the script.

---
## How It Works

- **`print_directory_structure(path, ignore_list, full_explore_list)`**: Recursively prints the directory structure, ignoring any directories or files on the ignore list and optionally fully exploring directories on the explore list.
  
- **`write_file_contents(path, ignore_list, full_explore_list)`**: Appends the contents of files in explored directories to the output.

- **`write_structure_and_contents(directory_path, ignore_list, output_filename, full_explore_list)`**: Combines the directory structure and file content writing functionalities into a single output file.

---

You can use this tool to generate a clean, structured output of your project that you can share or use for troubleshooting with AI tools.

---

## Further Resources

For more details, check out our [Github](https://github.com/Atharvatonape/Directure).
