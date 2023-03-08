#!/usr/bin/env python3.10

import subprocess
from pathlib import Path
from rofi_menu import Menu, Back, run_menu


# Set the root directory to search and define the Rofi theme to use
root_dir = Path("~/code").expanduser()
rofi_theme = Path("~/code/themes/redblack.rasi").expanduser()

# Define the directory menu
def directory_menu():
    # Get a list of all subdirectories in the root directory that are not hidden, have subdirectories,
    # and have at least one file or symlink in them, and do not contain .git or __pycache__
    all_subdirs = [
        subdir for subdir in root_dir.glob("**/*")
        if subdir.is_dir() and not any(name in str(subdir) for name in [".git", "__pycache__"])
    ]

    # Sort the list of directories alphabetically and use rofi to display a menu of them
    return Menu(options=sorted(str(subdir) for subdir in all_subdirs), prompt="Select directory:")


# Define the application menu
def application_menu(selected_dir):
    # Use rofi to display a menu of the applications to open the selected directory in
    return Menu(
        options=["Visual Studio Code", "Nemo", "Alacritty"],
        prompt=f"Select application to open {selected_dir} in:",
    )


# Define the main function to run the menus
def main():
    # Run the directory menu
    selected_dir = run_menu(directory_menu(), rofi_args=["-theme", str(rofi_theme)])
    if not selected_dir:
        return

    # Run the application menu
    selected_app = run_menu(application_menu(selected_dir), rofi_args=["-theme", str(rofi_theme)])
    if not selected_app:
        return

    # Open the selected directory in the selected application
    if selected_app == "Visual Studio Code":
        subprocess.Popen(["code", "-n", selected_dir])
    elif selected_app == "Nemo":
        subprocess.Popen(
            ["nemo", selected_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    elif selected_app == "Alacritty":
        subprocess.Popen(["alacritty", "-e", "cd", selected_dir])

if __name__ == "__main__":
    main()
