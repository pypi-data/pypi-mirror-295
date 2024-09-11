import os
import platform
import shutil
import argparse
import sys
import logging
from .constants import FILE_TYPES
from .utils import print_logic

__version__ = "1.0.4"
GLOBAL_QUIET = False

# def get_system_user_directories():
#     if platform.system() == 'Darwin':
#         print("MAC OS")
#     elif platform.system() == 'Linux':
#         print("Linux")
#     elif platform.system() == 'Windows':
#         print("Windows")
#     else:
#         print("Warning for use this script on your OS")

def remove_empty_dir(directory):
    if not os.path.isdir(directory):
        print_logic(f"Error: {directory} is not a valid directory.")
        return False

    if not os.listdir(directory):
        try:
            os.rmdir(directory)
            return True
        except Exception as e:
            print_logic(f"Error while deleting directory '{directory}': {e}", 'red', GLOBAL_QUIET)
            return False
    else:
        print_logic(f"Directory '{directory}' is not empty, deletion not performed.", 'red', GLOBAL_QUIET)
        return False

def create_master_folder(source_folder, simulation, custom_folder_name=None):
    folder_name = custom_folder_name if custom_folder_name else 'TidySorter'
    master_folder = os.path.join(source_folder, folder_name)
    
    if not simulation and not os.path.exists(master_folder):
        os.makedirs(master_folder)
    
    return master_folder

def handle_shortcuts(item_name, item_path, simulation, safe, master_folder):
    folder_path = os.path.join(master_folder, 'Shortcuts')

    if simulation:
        if safe:
            print_logic(f'[SIMULATION] {item_name} would be moved to {folder_path}', 'yellow', GLOBAL_QUIET)
        else:
            print_logic(f'[SIMULATION] Shortcut file "{item_name}" would be deleted.', 'red', GLOBAL_QUIET)
    elif safe:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        shutil.move(item_path, os.path.join(folder_path, item_name))
        print_logic(f'Shortcut file "{item_name}" moved to "{folder_path}".', 'green', GLOBAL_QUIET)
    else:
        os.remove(item_path)
        print_logic(f'Shortcut file "{item_name}" deleted.', 'red', GLOBAL_QUIET)

def organize_files(source_folder, simulation=False, recursive=False, custom_folder_name=None, safe=False, quiet=False):
    global GLOBAL_QUIET
    GLOBAL_QUIET = quiet
    master_folder = create_master_folder(source_folder, simulation, custom_folder_name)
    
    def process_folder(folder):
        for item_name in os.listdir(folder):
            item_path = os.path.join(folder, item_name)

            if item_name == 'TidySorter':
                continue

            if item_name.lower().endswith('.lnk'):
                handle_shortcuts(item_name, item_path, simulation, safe, master_folder)
                continue

            if os.path.isdir(item_path):
                folder_path = os.path.join(master_folder, 'Folders')
                
                if recursive:
                    process_folder(item_path)

                if simulation:
                    print_logic(f'[SIMULATION] Folder "{item_name}" would be checked and potentially moved to {folder_path}', 'yellow', GLOBAL_QUIET)
                else:
                    if remove_empty_dir(item_path):
                        print_logic(f"Empty directory '{item_path}' deleted.", 'red', GLOBAL_QUIET)
                    else:
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        shutil.move(item_path, os.path.join(folder_path, item_name))
                        print_logic(f'Folder "{item_name}" moved to {folder_path}', 'green', GLOBAL_QUIET)
                continue

            if os.path.isfile(item_path):
                file_ext = os.path.splitext(item_name)[1].lower()
                moved = False
                for folder_name, extensions in FILE_TYPES.items():
                    if file_ext in extensions:
                        folder_path = os.path.join(master_folder, folder_name)
                        if simulation:
                            print_logic(f'[SIMULATION] {item_name} would be moved to {folder_path}', 'yellow', GLOBAL_QUIET)
                        else:
                            if not os.path.exists(folder_path):
                                os.makedirs(folder_path)
                            shutil.move(item_path, os.path.join(folder_path, item_name))
                            print_logic(f'{item_name} moved to {folder_path}', 'green', GLOBAL_QUIET)
                        moved = True
                        break

                if not moved and simulation:
                    print_logic(f'[SIMULATION] {item_name} does not match any defined category.', 'yellow', GLOBAL_QUIET)
    process_folder(source_folder)

def main() -> None:
    parser = argparse.ArgumentParser(description="Effortlessly organize your files into neatly categorized folders, making it easier to prepare for system formatting or reinstallation, or simply to clean up cluttered directories filled with accumulated files. Compatible with macOS, Linux, and Windows.")
    parser.add_argument('source_folder', nargs='?', help="The source folder to sort")
    parser.add_argument("-f", "--folder", type=str, help="Custom name of the master folder.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all console output (quiet mode)")
    # parser.add_argument('-r', '--revert', action='store_true', help="Revert everything (requires log)")
    parser.add_argument("-R", "--recursive", action="store_true", help="Apply sorting recursively to subfolders")
    parser.add_argument('-s', '--simulate', action='store_true', help='Enable simulation mode (no changes will be made)')
    parser.add_argument("-S", "--safe", action="store_true", help="Prevent deletion of empty folders and shortcut files. By default, empty folders and shortcut files will be removed during sorting.")
    parser.add_argument("-v", "--version", action="version", version=__version__, help="Display the version number")
    # parser.add_argument('-w', '--without-log', action='store_true', help='Without logs')

    args = parser.parse_args()

    if args.recursive:
        try:
            print_logic("Warning: You have selected recursive sorting. This will process all subdirectories.", 'yellow')
            confirmation = input("Do you want to continue? (y / yes to confirm): ").strip().lower()

            if confirmation not in ['y', 'yes']:
                print_logic("Operation cancelled by the user.", 'red')
                sys.exit(1)
        
        except KeyboardInterrupt:
            print_logic("Operation cancelled by the user via Ctrl+C.", 'red')
            sys.exit(1)

    if args.source_folder:
        print_logic(f"Processing folder: {args.source_folder}", '', args.quiet)
    else:
        print("No source folder provided. Use -h for help.")
        sys.exit()
        
    if not os.path.isdir(args.source_folder):
        print(f"Error: {args.source_folder} is not a valid folder.")
        sys.exit()

    organize_files(
        args.source_folder,
        simulation=args.simulate,
        recursive=args.recursive,
        safe=args.safe,
        quiet=args.quiet,
        custom_folder_name=args.folder
    )

if __name__ == "__main__":
    main()