#!/usr/bin/env python3.10

import os
import subprocess
import sys

# Set the root directory to search
root_dir = os.path.expanduser('~/code')

# Define the Rofi theme to use
rofi_theme = os.path.expanduser('~/code/themes/redblack.rasi')

# Get a list of all directories in the root directory that are not hidden and not __pycache__
dirs = [d for d in sorted(os.listdir(root_dir))
        if os.path.isdir(os.path.join(root_dir, d))
        and not d.startswith('.')
        and d != '__pycache__']

# Get a list of all subdirectories of each directory in dirs that are not hidden, have subdirectories, and have at least one file or symlink in them
for d in dirs[:]:
    subdirs = [sd for sd in sorted(os.listdir(os.path.join(root_dir, d)))
               if os.path.isdir(os.path.join(root_dir, d, sd))
               and not sd.startswith('.')
               and sd != '__pycache__'
               and (os.listdir(os.path.join(root_dir, d, sd)) or os.path.islink(os.path.join(root_dir, d, sd)))]
    if subdirs:
        dirs.extend([os.path.join(d, sd) for sd in subdirs])
    elif not os.path.isfile(os.path.join(root_dir, d)) and not os.path.islink(os.path.join(root_dir, d)):
        dirs.remove(d)

# Sort the list of directories alphabetically
dirs.sort()

# Use rofi to display a menu of the directories and get the selected directory
selected_dir = subprocess.check_output(['rofi', '-dmenu', '-p', 'Select directory:', '-format', 's', '-theme', rofi_theme], input='\n'.join([os.path.join(root_dir, d) for d in dirs]), text=True).strip()

# Exit gracefully if no directory is selected
if not selected_dir:
    sys.exit()

# Use rofi to display a menu of the applications to open the selected directory in
selected_app = subprocess.check_output(['rofi', '-dmenu', '-p', 'Select application:', '-format', 's', '-theme', rofi_theme], input='Visual Studio Code\nNemo\nAlacritty', text=True).strip()

# Open the selected directory in the selected application
if selected_app == 'Visual Studio Code':
    subprocess.Popen(['code', '-n', selected_dir])
elif selected_app == 'Nemo':
    subprocess.Popen(['nemo', selected_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
elif selected_app == 'Alacritty':
    subprocess.Popen(['alacritty', '-e', 'cd', selected_dir])
