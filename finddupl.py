import os
import shutil
import hashlib
from tkinter import (Tk, filedialog, Toplevel, Button, Label, StringVar, Text, Scrollbar, Frame, VERTICAL, END, messagebox, IntVar, Listbox)
from tkinter.ttk import Progressbar

HASH_CHUNK_SIZE = 4096
HASH_LIMIT_SIZE = 1 * 1024 * 1024

def hash_file(filename):
    h = hashlib.sha256()
    with open(filename, 'rb') as f:
        chunk = f.read(HASH_CHUNK_SIZE)
        while chunk:
            h.update(chunk)
            if h.digest_size >= HASH_LIMIT_SIZE:
                break
            chunk = f.read(HASH_CHUNK_SIZE)
    return h.hexdigest()

def find_duplicates(directories, update_callback):
    hashes = {}
    duplicates = []
    all_files = []

    for directory in directories:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                full_path = os.path.join(foldername, filename)
                all_files.append(full_path)

    total_files = len(all_files)
    for index, filename in enumerate(all_files):
        file_hash = hash_file(filename)
        if file_hash in hashes:
            duplicates.append((filename, hashes[file_hash]))
        else:
            hashes[file_hash] = filename

        percentage_done = (index+1) / total_files * 100
        update_callback(percentage_done)

    return duplicates

def delete_duplicates(duplicates):
    total_size = 0
    for duplicate in duplicates:
        duplicate_path = duplicate[0]
        total_size += os.path.getsize(duplicate_path)
        os.remove(duplicate_path)
    return total_size

def move_duplicates(duplicates, search_directory):
    duplicates_folder = os.path.join(search_directory, "duplicates")
    if os.path.exists(duplicates_folder):
        counter = 1
        base_name = "duplicates"
        while os.path.exists(duplicates_folder):
            duplicates_folder = os.path.join(search_directory, f"{base_name}_{counter}")
            counter += 1
    os.makedirs(duplicates_folder)

    for duplicate in duplicates:
        duplicate_path = duplicate[0]
        target_path = os.path.join(duplicates_folder, os.path.basename(duplicate_path))
        base, ext = os.path.splitext(os.path.basename(duplicate_path))
        counter = 1
        while os.path.exists(target_path):
            target_path = os.path.join(duplicates_folder, f"{base}_{counter}{ext}")
            counter += 1
        shutil.move(duplicate_path, target_path)

def add_directory():
    directory = filedialog.askdirectory(title="Select a directory", mustexist=True)
    if directory:
        dir_listbox.insert(END, directory)

def remove_directory():
    selected_idx = dir_listbox.curselection()
    if selected_idx:
        dir_listbox.delete(selected_idx)

def display_results(duplicates, directories):
    if not duplicates:
        messagebox.showinfo("Info", "No duplicates found.")
        return

    results_win = Toplevel(root)
    results_win.title("Search Results")

    txt_frame = Frame(results_win)
    txt_frame.pack(fill="both", expand=True)

    txt = Text(txt_frame, wrap="word", height=20, width=80)
    scrollbar = Scrollbar(txt_frame, command=txt.yview, orient=VERTICAL)
    txt.configure(yscrollcommand=scrollbar.set)

    for duplicate in duplicates:
        txt.insert(END, f"Duplicate: {duplicate[0]}\nOriginal: {duplicate[1]}\n\n")
    txt.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    action_frame = Frame(results_win)
    action_frame.pack(pady=10)

    def on_delete():
        total_size_deleted = delete_duplicates(duplicates)
        size_in_mb = total_size_deleted / (1024 * 1024)
        messagebox.showinfo("Info", f"Deleted duplicates. Total size freed: {size_in_mb:.2f} MB.")
        results_win.destroy()

    def on_move():
        for directory in directories:
            move_duplicates(duplicates, directory)
        messagebox.showinfo("Info", "Duplicates moved to the 'duplicates' directory in each search directory.")
        results_win.destroy()

    Button(action_frame, text="Delete Duplicates", command=on_delete).pack(side="left", padx=5)
    Button(action_frame, text="Move Duplicates", command=on_move).pack(side="left", padx=5)
    Button(action_frame, text="Close", command=results_win.destroy).pack(side="left", padx=5)

def on_search():
    directories = list(dir_listbox.get(0, END))
    if not directories:
        messagebox.showwarning("Warning", "Please select at least one directory.")
        return
    progress_win = Toplevel(root)
    progress_win.title("Searching...")
    progress = Progressbar(progress_win, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)
    progress_percent = StringVar()
    progress_percent.set("0%")
    progress_label = Label(progress_win, textvariable=progress_percent)
    progress_label.pack(pady=10)

    def update_progress(percentage):
        progress['value'] = percentage
        progress_percent.set(f"{percentage:.2f}%")
        progress_win.update_idletasks()

    duplicates = find_duplicates(directories, update_progress)
    progress_win.destroy()
    display_results(duplicates, directories)

def main():
    global dir_listbox, root
    root = Tk()
    root.title("Duplicate Finder")

    Label(root, text="Choose directories to search for duplicates.").pack(pady=10)
    dir_listbox = Listbox(root)
    dir_listbox.pack(pady=10)
    Button(root, text="Add Directory", command=add_directory).pack(pady=5)
    Button(root, text="Remove Selected Directory", command=remove_directory).pack(pady=5)
    Button(root, text="Start Search", command=on_search).pack(pady=10)
    Button(root, text="Exit", command=root.destroy).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
