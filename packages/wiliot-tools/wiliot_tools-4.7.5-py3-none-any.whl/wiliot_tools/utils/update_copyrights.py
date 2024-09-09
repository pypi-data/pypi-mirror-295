import os
import tkinter as tk
from tkinter import filedialog, messagebox

current_year = 2024


def update_copyright_year(folder_path, year):
    original_copyright = "Copyright (c) 2016- 2024"
    updated_copyright = f"Copyright (c) 2016- {year}"

    for root_folder, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root_folder, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if original_copyright in content:
                    content = content.replace(original_copyright, updated_copyright)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        update_copyright_year(folder_path, current_year)
        messagebox.showinfo("Completed", "Copyright year updated in all matching files.")
        root.destroy()


root = tk.Tk()
root.title("Update Copyright Year")
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)
label = tk.Label(frame, text="Select the folder to process:")
label.pack(pady=5)
browse_button = tk.Button(frame, text="Browse", command=browse_folder)
browse_button.pack(pady=5)

root.mainloop()
