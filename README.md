# README for the Duplicate File Finder Script

## Overview

This Python script is designed to find and handle duplicate files in user-specified directories. It utilizes a Graphical User Interface (GUI) implemented with Tkinter to provide an intuitive user interaction. The script allows the selection of directories to search, initiates the search process, and then either deletes found duplicates or moves them to a specified folder.

## Logic of Operation

### Finding Duplicates

- **Hash Calculation**: To identify duplicates, the script calculates the SHA-256 hash of each file's content. This allows for accurate identification of identical files regardless of their names or locations.
- **Optimization for Large Files**: The script reads files in fixed-size blocks to efficiently process large files and minimize memory usage.
- **Storing and Comparing Hashes**: The script stores the hash of each file in a dictionary where the hash is the key, and the file path is the value. If a file's hash already exists in the dictionary, that file is considered a duplicate.

### Graphical User Interface (GUI)

- **Directory Selection**: Users can add or remove directories for search through a dialog window.
- **Progress Display**: The search progress is displayed as a progress bar, providing feedback on the task's progress.
- **Search Results**: Upon completion of the search, a new window opens with a list of found duplicates. Each duplicate entry shows the path to the duplicate and the original file.

### Handling Duplicates

- **Deletion**: Users can delete all found duplicates, freeing up disk space.
- **Moving**: Alternatively, duplicates can be moved to a separate folder for further review.

## Usage

Python 3.6 or newer is required to run this script. The script does not require any external dependencies beyond the Python Standard Library.

1. Run the script from the command line or through an IDE.
2. Use the GUI to add directories where you want to search for duplicates.
3. Click "Start Search" to begin the search process.
4. After the search completes, review the found duplicates and choose further actions (delete or move).

## Development and Contributions

Developers are invited to improve the script by optimizing the search algorithm, enhancing the interface, or adding new features. Any changes or contributions should be made through pull requests to the project's repository.
