import tkinter as tk
from tkinter import filedialog
import re
import os


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("800x820")
        self.window.title("PARSER")
        self.window.configure(bg='#1c1c1c')

        self.label = MainHedge(self.window)
        self.file_selected_label = FileSelected(self.window)


        self.text = OutPutBox(self.window)

        # 2. Create GridSelectionButton SECOND (pass self.text.text_box)
        self.grid_buttons = GridSelectionButton(self.window, self.text.text_box)

        # 3. Create FileSelectButton LAST (needs self.grid_buttons AND self.file_selected_label)
        self.file_button = FileSelectButton(self.window, self.grid_buttons, self.file_selected_label)

        self.window.mainloop()


class MainHedge:
    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text=".OSU PARSER",
            fg="white",
            bg="#1c1c1c",
            font=("Times new roman", 50),
        )
        self.label.pack(pady=10)


class FileSelected:
    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text="no file selected",
            fg="white",
            bg="#1c1c1c",
            font=("Times new roman", 20),
        )
        self.label.pack(pady=5, anchor='center')

    def update_filename(self, filename):
        display_name = os.path.basename(filename)
        self.label.config(text=display_name)


class FileSelectButton:
    def __init__(self, parent, grid_selection_instance, file_selected_instance):
        self.grid_selection = grid_selection_instance   # Store reference
        self.file_selected = file_selected_instance     # Store reference to FileSelected
        self.button = tk.Button(
            parent,
            text="select .osu",
            font=("Times new roman", 20),
            command=self.select_file
        )
        self.button.pack(pady=5, anchor='center')

    def select_file(self):
        # Open file dialog to select .osu file
        filename = filedialog.askopenfilename(
            title="Select OSU file",
            filetypes=(("OSU files", "*.osu"), ("All files", "*.*"))
        )

        if filename:  # Only proceed if a file was selected
            # Pass the filename to GridSelectionButton
            self.grid_selection.set_file(filename)
            # Update the FileSelected label
            self.file_selected.update_filename(filename)


class GridSelectionButton:
    def __init__(self, parent, output_display):
        self.frame = tk.Frame(parent, bg="#1c1c1c")
        self.frame.pack(padx=20, pady=10)

        self.file_content = None              # Store file content
        self.output_display = output_display  # Reference to output display widget

        self.button1 = tk.Button(self.frame, text="File Version", font=("Times new roman", 12),     width=15, height=2,
                                 command=self.file_version)

        self.button2 = tk.Button(self.frame, text="General Data", font=("Times new roman", 12),     width=15, height=2,
                                 command=self.general_data)

        self.button3 = tk.Button(self.frame, text="MetaData",     font=("Times new roman", 12),     width=15, height=2,
                                 command=self.metadata_data)

        self.button4 = tk.Button(self.frame, text="Difficulty",   font=("Times new roman", 12),     width=15, height=2,
                                 command=self.difficulty_data)

        self.button5 = tk.Button(self.frame, text="Count Vowels", font=("Times new roman", 12),     width=15, height=2,
                                 command=self.count_vowels)

        self.button6 = tk.Button(self.frame, text="Clear",        font=("Times new roman", 12),     width=15, height=2,
                                 command=self.clear_output)

        self.button1.grid(row=0, column=0, padx=10, pady=10)
        self.button2.grid(row=0, column=1, padx=10, pady=10)
        self.button3.grid(row=0, column=2, padx=10, pady=10, columnspan=2, sticky="we")
        self.button4.grid(row=1, column=0, padx=10, pady=10)
        self.button5.grid(row=1, column=1, padx=10, pady=10)
        self.button6.grid(row=1, column=2, padx=10, pady=10, columnspan=2, sticky="we")


    # Opens the file from "FileSelectButton" from the "select_file" method
    def set_file(self, filename):
        with open(filename, encoding='utf-8') as f:
            self.file_content = f.readlines()

    def display_output(self, text):
        if isinstance(self.output_display, tk.Text):
            self.output_display.delete(1.0, tk.END)
            self.output_display.insert(1.0, text)
        elif isinstance(self.output_display, tk.Label):
            self.output_display.config(text=text)

    def file_version(self):
        if not self.file_content:
            self.display_output("No file selected!")
            return

        result = []
        for text in self.file_content:
            if re.search("^osu", text):
                result.append(text.strip())

        self.display_output("\n".join(result))

    def general_data(self):
        if not self.file_content:
            self.display_output("No file selected!")
            return

        in_general_section = False
        general_lines = []

        for line in self.file_content:
            # Check if we're entering the [General] section
            if re.search(r"^\[General]", line):
                in_general_section = True
                general_lines.append(line.strip())
                continue

            # Check if we've hit a new section
            if in_general_section and re.search(r"^\[.+]", line):
                break

            # Append lines while we're in the [General] section
            if in_general_section:
                general_lines.append(line.strip())

        self.display_output("\n".join(general_lines))

    def metadata_data(self):
        if not self.file_content:
            self.display_output("No file selected!")
            return

        in_metadata_section = False
        metadata_lines = []

        for line in self.file_content:
            # Check if we're entering the [Metadata] section
            if re.search(r"^\[Metadata]", line):
                in_metadata_section = True
                metadata_lines.append(line.strip())
                continue

            # Check if we've hit a new section
            if in_metadata_section and re.search(r"^\[.+]", line):
                break

            # Append lines while we're in the [Metadata] section
            if in_metadata_section:
                metadata_lines.append(line.strip())

        self.display_output("\n".join(metadata_lines))

    def difficulty_data(self):
        if not self.file_content:
            self.display_output("No file selected!")
            return

        in_difficulty_section = False
        difficulty_lines = []

        for line in self.file_content:
            # Check if we're entering the [Difficulty] section
            if re.search(r"^\[Difficulty]", line):
                in_difficulty_section = True
                difficulty_lines.append(line.strip())
                continue

            # Check if we've hit a new section
            if in_difficulty_section and re.search(r"^\[.+]", line):
                break

            # Append lines while we're in the [Difficulty] section
            if in_difficulty_section:
                difficulty_lines.append(line.strip())

        self.display_output("\n".join(difficulty_lines))

    def count_vowels(self):
        if not self.file_content:
            self.display_output("No file selected!")
            return

        in_metadata_section = False
        metadata_lines = []

        # First, extract the metadata section
        for line in self.file_content:
            # Check if we're entering the [Metadata] section
            if re.search(r"^\[Metadata]", line):
                in_metadata_section = True
                continue

            # Check if we've hit a new section
            if in_metadata_section and re.search(r"^\[.+]", line):
                break

            # Collect lines while we're in the [Metadata] section
            if in_metadata_section:
                metadata_lines.append(line)

        # Count vowels only in metadata
        vowel_count = 0
        for line in metadata_lines:
            vowels = re.findall("[aeiouAEIOU]", line)
            vowel_count += len(vowels)

        self.display_output(f"There were {vowel_count} vowels in the metadata section")

    def clear_output(self):
        self.display_output("")


class OutPutBox:
    def __init__(self, parent):
        self.text_box = tk.Text(
            parent,
            width=40,
            height=10,
            font=("Times new roman", 20),
            fg="white",
            bg="#2e2e2e",
            insertbackground="white"
        )
        self.text_box.pack(padx=10, pady=10)



MainWindow()