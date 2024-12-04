import os
import sys
from pathspec import PathSpec

def load_gitignore(path):
    """
    Load the .gitignore file and parse its patterns.
    :param path: The directory containing the .gitignore file.
    :return: A PathSpec object with the parsed patterns or None if no .gitignore is found.
    """
    gitignore_path = os.path.join(path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as file:
            patterns = file.read().splitlines()
        return PathSpec.from_lines("gitwildmatch", patterns)
    return None

def print_directory_tree(path, prefix="", spec=None):
    """
    Recursively prints the directory structure in a tree format, ignoring files specified in .gitignore.
    Also explicitly ignores 'node_modules' folders.
    :param path: The directory path to scan.
    :param prefix: The prefix used to format the tree structure.
    :param spec: The PathSpec object containing ignore rules.
    """
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        print(f"{prefix}Permission denied: {path}")
        return
    except FileNotFoundError:
        print(f"{prefix}Path not found: {path}")
        return

    for index, entry in enumerate(entries):
        entry_path = os.path.join(path, entry)
        
        if entry == "node_modules" and os.path.isdir(entry_path):
            continue
        
        if spec and spec.match_file(entry_path.replace("\\", "/")):
            continue

        connector = "└── " if index == len(entries) - 1 else "├── "
        print(f"{prefix}{connector}{entry}")
        if os.path.isdir(entry_path):
            extension = "    " if index == len(entries) - 1 else "│   "
            print_directory_tree(entry_path, prefix + extension, spec)

def main():
    """
    Main program loop for generating directory trees.
    """
    print("Welcome to Directory Structure Viewer!")
    print("Enter a directory path to generate its tree structure, or type 'exit' to quit.\n")
    
    while True:
        path = input("Enter directory path: ").strip()
        
        if path.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break

        if not os.path.exists(path):
            print("Invalid path. Please enter a valid directory path.\n")
            continue
        
        gitignore_spec = load_gitignore(path)

        print(f"\nDirectory Tree for: {path}\n")
        print(path)
        print_directory_tree(path, spec=gitignore_spec)
        print("\nTree generated successfully. Enter another path or type 'exit' to quit.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting now.")
        sys.exit(0)
