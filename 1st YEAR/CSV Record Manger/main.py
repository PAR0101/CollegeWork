import tkinter as tk                                            # Import tkinter for GUI
import pandas as pd                                             # Import pandas for CSV file handling
from tkinter import ttk, messagebox, filedialog                 # Import UI tools
import os                                                       # Import os for file checking

#osu_2023 
#records  

FILE_NAME = "records.csv"                                       # CSV file name
font = "Arial"                                                  # Default font used across UI


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()  # Create the main application window

        # Window customization
        self.window.geometry("900x1000")                                        # Set window size
        self.window.title("RECORD MANAGEMENT")                                  # Set title
        self.window.configure(bg="#1c1c1c")                                   # Set background color

        # Create UI sections
        self.Mainhedge = MainHedge(self.window)                             # Title header
        self.box = CellBlocks(self.window)                                  # Table / data display section
        self.button_layout = GridSelectionButtons(self.window, self.box)    # Buttons section

        self.window.mainloop()  


class MainHedge:        # Display title label at top of window
    def __init__(self, parent):
        tk.Label(
            parent,
            text="RECORD MANAGER",
            fg="white",
            bg="#1c1c1c",
            font=(font, 50),
        ).pack(pady=10)


class CellBlocks:
    def __init__(self, parent):
        # Frame that holds the table
        self.frame = tk.Frame(parent, bg="#1c1c1c")
        self.frame.pack(expand=True, fill="both")

        self.create_file()  # Create CSV if it does not exist

        # Configure Treeview style
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1c1c1c",
            foreground="white",
            fieldbackground="#1c1c1c",
            font=(font, 20),
            rowheight=30,
        )
        
        style.configure(
            "Treeview.Heading",
            background="#2c2c2c",
            foreground="white",
            font=(font, 20, "bold"),
        )

        # Treeview widget = Table that displays data
        self.tree = ttk.Treeview(self.frame)

        # Default columns
        self.columns = ["ID", "Name", "Age", "Course"]
        self.tree["columns"] = self.columns
        self.tree["show"] = "headings"

        # Create headings dynamically
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(expand=True, fill="both")

        # Enable double-click editing
        self.tree.bind("<Double-1>", self.edit_cell)

        self.load_data()  # Load CSV data

    def create_file(self):  # Create CSV file if it does not exist
        if not os.path.exists(FILE_NAME):
            df = pd.DataFrame(columns=["ID", "Name", "Age", "Course"])
            df.to_csv(FILE_NAME, index=False)

    def load_data(self):    # Read CSV and load into table
        df = pd.read_csv(FILE_NAME, dtype=str)

        # Clear table before loading new data
        self.tree.delete(*self.tree.get_children())

        # Update columns dynamically from CSV
        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        # Recreate headings dynamically
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Insert rows into table
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def edit_cell(self, event):
        # Detect clicked region (cell or heading)
        region = self.tree.identify_region(event.x, event.y)
        column = self.tree.identify_column(event.x)

        if not column:
            return

        col_index = int(column.replace("#", "")) - 1

        #  HEADING EDIT 
        if region == "heading":
            old_heading = self.tree["columns"][col_index]

            # Popup window to rename column
            dialog = tk.Toplevel(self.frame)
            dialog.title("Edit Heading")
            dialog.geometry("500x250")
            dialog.configure(bg="#1c1c1c")

            tk.Label(
                dialog,
                text=f"Rename column '{old_heading}':",
                font=(font, 25),
                fg="white",
                bg="#1c1c1c",
            ).pack(pady=20)

            entry = tk.Entry(dialog, font=(font, 22), width=25)
            entry.pack(pady=10)
            entry.insert(0, old_heading)
            entry.focus()

            def save_heading():
                new_heading = entry.get().strip()

                if new_heading and new_heading != old_heading:
                    df = pd.read_csv(FILE_NAME, dtype=str)
                    cols = list(df.columns)
                    cols[col_index] = new_heading       # Replace column name
                    df.columns = cols
                    df.to_csv(FILE_NAME, index=False)

                    self.load_data()                     # Refresh table

                dialog.destroy()

            tk.Button(
                dialog,
                text="Save",
                font=(font, 20),
                width=12,
                height=2,
                command=save_heading,
            ).pack(pady=20)

            return

        #  CELL EDIT 
        if region == "cell":
            row = self.tree.identify_row(event.y)
            if not row:
                return

            # Safely grab the bounding box (prevents crash if cell is off-screen)
            bbox = self.tree.bbox(row, column)
            if not bbox:
                return
            x, y, width, height = bbox

            # Safely grab the old value
            try:
                old_value = self.tree.item(row)["values"][col_index]
            except IndexError:
                old_value = ""

            # Create entry widget directly inside the table
            entry = tk.Entry(self.tree, font=(font, 20))
            entry.place(x=x, y=y, width=width, height=height)

            entry.insert(
                0,
                "" if old_value is None or old_value == "None" else str(old_value),
            )
            entry.focus()

            def save_edit(event=None):
                new_value = entry.get()
                values = list(self.tree.item(row)["values"])

                # Pad the values list in case it's shorter than expected
                # Extend list if needed
                while len(values) <= col_index:
                    values.append("")

                values[col_index] = new_value

                self.tree.item(row, values=values)
                entry.destroy()
                self.save_tree_to_csv()

            entry.bind("<Return>", save_edit)
            entry.bind("<FocusOut>", lambda e: entry.destroy())

    def save_tree_to_csv(self):
        # Save table data back into CSV
        rows = []

        for item in self.tree.get_children():
            rows.append(self.tree.item(item)["values"])

        df = pd.DataFrame(rows, columns=self.tree["columns"])
        df.to_csv(FILE_NAME, index=False)

    #  BUTTON METHODS 
    def add_row(self):
        # Window to add new record
        window = tk.Toplevel(self.frame)
        window.title("Add Record")
        current_cols = list(self.tree["columns"])   # Pull current columns dynamically

        # Make window height adapt to number of columns
        base_height = 150
        row_height = 60
        new_height = base_height + (len(current_cols) * row_height)
        window.geometry(f"600x{new_height}")    #   Determines the height for the window
        window.configure(bg="#1c1c1c")

        entries = {}

        # Create input fields dynamically for each column
        for i, label in enumerate(current_cols):
            tk.Label(
                window,
                text=label,
                font=(font, 25),
                fg="white",
                bg="#1c1c1c",
            ).grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(window, width=20, font=(font, 22))
            entry.grid(row=i, column=1, padx=10, pady=5)

            entries[label] = entry

        
        def save_record():  #   Saves a new entry for a new row
            new_data = {key: entries[key].get() for key in entries}

            df = pd.read_csv(FILE_NAME, dtype=str)
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)

            self.load_data()
            messagebox.showinfo("Success", "Record Added!")
            window.destroy()

        def add_new_column_prompt():
                    # Create a custom popup window
            col_window = tk.Toplevel(window)
            col_window.title("New Column")
            col_window.geometry("500x300")
            col_window.configure(bg="#1c1c1c")
                    
            # Make it stay on top and grab focus
            col_window.transient(window)
            col_window.grab_set()
            tk.Label(
                col_window,
                text="Enter New Column Name:",
                font=(font, 25),
                fg="white",
                bg="#1c1c1c",
            ).pack(pady=30)

            col_entry = tk.Entry(col_window, font=(font, 22), width=25)
            col_entry.pack(pady=10)
            col_entry.focus()

            def confirm_column():
                new_col_name = col_entry.get().strip()
                        
                if new_col_name != "":
                    df = pd.read_csv(FILE_NAME, dtype=str)

                    if new_col_name in df.columns:
                        messagebox.showerror("Error", "Column already exists!")
                        return

                    df[new_col_name] = ""  # Add new column
                    df.to_csv(FILE_NAME, index=False)

                    self.load_data()
                    messagebox.showinfo("Success", f"Column '{new_col_name}' added!")

                    col_window.destroy() # Close the small popup
                    window.destroy()     # Close the "Add Record" window
                    self.add_row()       # Re-open "Add Record" to show new column
                else:
                    col_window.destroy()

            tk.Button(
                col_window,
                text="Add Column",
                font=(font, 20),
                width=15,
                height=2,
                command=confirm_column,
            ).pack(pady=20)

        # Bottom button frame
        button_frame = tk.Frame(window, bg="#1c1c1c")
        button_frame.grid(
            row=len(current_cols) + 1,
            column=0,
            columnspan=2,
            pady=15,
            sticky="we",
        )

        tk.Button(
            button_frame,
            text="Save",
            font=(font, 20),
            width=12,
            height=2,
            command=save_record,
        ).pack(side="right", padx=10)

        tk.Button(
            button_frame,
            text="+ New Column",
            font=(font, 20),
            width=12,
            height=2,
            command=add_new_column_prompt,
        ).pack(side="left", padx=10)

    def delete_row(self):
        # Window for deleting row by ID
        window = tk.Toplevel(self.frame)
        window.title("Delete Row")
        window.geometry("500x250")
        window.configure(bg="#1c1c1c")

        tk.Label(
            window,
            text="Enter ID",
            font=(font, 20),
            fg="white",
            bg="#1c1c1c",
        ).pack(pady=20)

        entry = tk.Entry(window, font=(font, 20))
        entry.pack()

        def delete():
            df = pd.read_csv(FILE_NAME, dtype=str)

            #   Deletes the Specified row with the give ID(referring to the first column)
            df = df[df.iloc[:, 0] != entry.get()]
            df.to_csv(FILE_NAME, index=False)
            self.load_data()
            messagebox.showinfo("Deleted", "Record Deleted")
            window.destroy()

        #   Makes the button attached with the function delete
        tk.Button(
            window,
            text="Delete",
            font=(font, 20),
            command=delete,
        ).pack(pady=10)

    def search_record_window(self):
        #   Window for searching by ID
        window = tk.Toplevel(self.frame)
        window.title("Search")
        window.geometry("500x250")
        window.configure(bg="#1c1c1c")

        tk.Label(
            window,
            text="Enter ID",
            font=(font, 25),
            fg="white",
            bg="#1c1c1c",
        ).pack(pady=20)

        entry = tk.Entry(window, font=(font, 20), width=30)
        entry.pack(pady=10)

        def search():
            df = pd.read_csv(FILE_NAME, dtype=str)
            value = entry.get().strip()
            col = df.columns[0]

            result = df[df[col].astype(str) == value]

            self.tree.delete(*self.tree.get_children())

            for _, row in result.iterrows():
                self.tree.insert("", "end", values=list(row))

            window.destroy()

        tk.Button(
            window,
            text="Search",
            font=(font, 20),
            width=15,
            height=2,
            command=search,
        ).pack(pady=15)

    def load_csv(self):
        # Load external CSV file into program
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            df = pd.read_csv(path, dtype=str)
            df.to_csv(FILE_NAME, index=False)
            self.load_data()
            messagebox.showinfo("Success", "CSV Loaded")

    def save_as_csv(self):
        # Export current table as new CSV
        df = pd.read_csv(FILE_NAME)
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
        )
        if path:
            df.to_csv(path, index=False)
            messagebox.showinfo("Success", "Exported")


class GridSelectionButtons:
    def __init__(self, parent, table):
        # Frame for bottom buttons
        self.frame = tk.Frame(parent, bg="#1c1c1c")
        self.frame.pack(padx=20, pady=10)

        font_size = 20
        self.table = table

        # Buttons with attached table functions
        self.button1 = tk.Button(
            self.frame,
            text="Add",
            font=(font, font_size),
            width=15,
            height=2,
            command=self.table.add_row,
        )

        self.button2 = tk.Button(
            self.frame,
            text="Delete",
            font=(font, font_size),
            width=15,
            height=2,
            command=self.table.delete_row,
        )

        self.button3 = tk.Button(
            self.frame,
            text="Display",
            font=(font, font_size),
            width=15,
            height=2,
            command=self.table.load_data,
        )

        self.button4 = tk.Button(
            self.frame,
            text="Search",
            font=(font, font_size),
            width=15,
            height=2,
            command=self.table.search_record_window,
        )

        self.button5 = tk.Button(
            self.frame,
            text="Load CSV",
            font=(font, font_size),
            width=15,
            height=2,
            command=self.table.load_csv,
        )

        self.button6 = tk.Button(
            self.frame,
            text="Save as CSV",
            font=(font, font_size),
            width=15,
            height=2,
            command=self.table.save_as_csv,
        )

        # Grid layout for buttons
        self.button1.grid(row=0, column=0, padx=10, pady=10)
        self.button2.grid(row=0, column=1, padx=10, pady=10)
        self.button3.grid(row=0, column=2, padx=10, pady=10, columnspan=2, sticky="we")
        self.button4.grid(row=1, column=0, padx=10, pady=10)
        self.button5.grid(row=1, column=1, padx=10, pady=10)
        self.button6.grid(row=1, column=2, padx=10, pady=10, columnspan=2, sticky="we")


if __name__ == "__main__":
    MainWindow()  
