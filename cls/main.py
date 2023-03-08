#!/usr/bin/env python3.10

import os
import subprocess
import sys

# Set the root directory to search and define the Rofi theme to use
root_dir = os.path.expanduser("~/code")
rofi_theme = os.path.expanduser("~/code/themes/redblack.rasi")

# Get a list of all subdirectories in the root directory that are not hidden, have subdirectories,
# and have at least one file or symlink in them
all_subdirs = [
    subdir_path for root, dirs, files in os.walk(root_dir)
    if not os.path.basename(root).startswith(".") and not os.path.basename(root) in ["__pycache__", ".git"]
    for subdir in dirs
    for subdir_path in [os.path.join(root, subdir)]
    if os.path.isdir(subdir_path) and not subdir.startswith(".") and os.listdir(subdir_path)
]

# Sort the list of directories alphabetically and use rofi to display a menu of them
selected_dir = subprocess.check_output(
    ["rofi", "-dmenu", "-p", "Select directory:", "-format", "s", "-theme", rofi_theme],
    input="\n".join(sorted(all_subdirs)),
    text=True,
).strip()

# Exit gracefully if no directory is selected
if not selected_dir:
    sys.exit()

# Use rofi to display a menu of the applications to open the selected directory in
selected_app = subprocess.check_output(
    [
        "rofi",
        "-dmenu",
        "-p",
        "Select application:",
        "-format",
        "s",
        "-theme",
        rofi_theme,
    ],
    input="Visual Studio Code\nNemo\nAlacritty",
    text=True,
).strip()

# Open the selected directory in the selected application
if selected_app == "Visual Studio Code":
    subprocess.Popen(["code", "-n", selected_dir])
elif selected_app == "Nemo":
    subprocess.Popen(
        ["nemo", selected_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
elif selected_app == "Alacritty":
    subprocess.Popen(["alacritty", "-e", "cd", selected_dir])
