#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# file_organizer.py
# Author: Kartikey Tripathi
# Date: July 2025

# A beginner-friendly script to organize your messy folders by file type.
# It moves .pdf files into a 'pdf' folder, .jpg files into 'jpg', etc.

import os
import shutil
from pathlib import Path
import argparse

print("""
Hey there 👋

This script helps you organize your files by extension.

Example: .jpg files go in a 'jpg' folder, .pdf in a 'pdf' folder, and so on.
You can clean any folder — just paste its path when asked.

If you don’t give a path, it’ll clean the folder where this script is saved.

Let’s do this. 🚀
""")

# Setting up command-line argument
parser = argparse.ArgumentParser(description="Organize files in a folder by extension.")
parser.add_argument('--path', type=str, help="Optional: Path to the folder you want to organize")
args = parser.parse_args()

# Use CLI path if given, else ask user
if args.path:
    path = Path(args.path)
else:
    user_input = input("Enter folder path (or press Enter to use current directory): ").strip()
    path = Path(user_input) if user_input else Path.cwd()

# Safety checks
if not path.exists():
    print(f"❌ Path doesn't exist: {path}")
    exit(1)

if not path.is_dir():
    print(f"❌ Not a directory: {path}")
    exit(1)

print(f"📁 Organizing files in: {path.resolve()}\n")

# Get all files in the folder
file_list = [f for f in path.iterdir() if f.is_file()]

if not file_list:
    print("No files found to organize.")
    exit(0)

# Build a list of extensions (like 'jpg', 'pdf', etc.)
extensions = set()
for file in file_list:
    ext = file.suffix.lower().lstrip('.')  # Removes dot and makes lowercase
    if ext:  # skip files without extension
        extensions.add(ext)

# Create folders for each extension
for ext in extensions:
    folder = path / ext
    if not folder.exists():
        folder.mkdir()

# Start moving files
files_moved = 0
skipped = 0

for file in file_list:
    ext = file.suffix.lower().lstrip('.')
    if not ext:
        continue  # skip files without extension

    dest = path / ext / file.name

    if dest.exists():
        print(f"⚠️  Skipping '{file.name}' — already exists in '{ext}/'")
        skipped += 1
        continue

    try:
        shutil.move(str(file), str(dest))
        print(f"✅ Moved: {file.name} → {ext}/")
        files_moved += 1
    except Exception as e:
        print(f"❌ Failed to move {file.name}: {e}")
        skipped += 1

# Clean up any empty folders (in case)
for ext in extensions:
    folder = path / ext
    if folder.exists() and not any(folder.iterdir()):
        try:
            folder.rmdir()
            print(f"🧹 Removed empty folder: {ext}/")
        except:
            pass  # Ignore errors

# Final summary
print("\n🎯 Summary:")
print(f"Files moved: {files_moved}")
print(f"Files skipped: {skipped}")
print("Done! Your folder should look a lot cleaner now.")
