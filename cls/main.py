#!/usr/bin/env python3.10

import os
import subprocess
import sys
from pathlib import Path

# Set the root directory to search and define the Rofi theme to use
root_dir = Path("~/code").expanduser()
rofi_theme = Path("~/code/themes/redblack.rasi").expanduser()

# Get a list of all subdirectories in the root directory that are not hidden, have subdirectories,
# and have at least one file or symlink in them, and do not contain .git or __pycache__
all_subdirs = [
    str(subdir) for subdir in root_dir.glob("**/*")
    if subdir.is_dir() and not any(name in str(subdir) for name in [".git", "__pycache__"])
]

# Sort the list of directories alphabetically and use rofi to display a menu of them
selected_dir = subprocess.check_output(
    ["rofi", "-dmenu", "-p", "Select directory:", "-format", "s", "-theme", str(rofi_theme)],
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
        str(rofi_theme),
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
