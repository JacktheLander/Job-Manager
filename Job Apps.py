import os
import csv
import re
import pandas as pd
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import os.path
import shutil
from datetime import datetime

# Make a directory for the app
appdata = os.getenv('APPDATA')
base_path = os.path.join(appdata, 'Job Apps')
# Ensure the directory exists (create it if necessary)
if not os.path.exists(base_path):
    os.makedirs(base_path)

Data_path = os.path.join(base_path, 'JobData.csv')
Output_path = os.path.join(base_path, 'JobOutput.csv')
Notes_path = os.path.join(base_path, 'JobNotes.csv')
Sorted_path = os.path.join(base_path, 'JobSorted.csv')

#os.remove(Data_path)       ### Deletes cache
#os.remove(Output_path)
#os.remove(Notes_path)
#os.remove(Sorted_path)

if not os.path.isfile(Sorted_path):
    print("creating sorted")
    with open(Sorted_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Position", "Location", "Status"])
if not os.path.isfile(Data_path):
    print("creating data")
    with open(Data_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Position", "Location", "Status"])
if not os.path.isfile(Notes_path):
    print("creating data")
    with open(Notes_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Job", "Notes"])
class ModernCSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Applications Manager")
        self.root.geometry("900x600")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Frame to contain all form elements, initially hidden
        self.form_frame = ctk.CTkFrame(root, border_width=2)
        self.form_frame2 = ctk.CTkFrame(root, border_width=2)
        self.table_frame = ctk.CTkFrame(root)
        self.header_frame = ctk.CTkFrame(root)

        self.create_button = ctk.CTkButton(self.header_frame, text="+", width=30, font=("Arial", 18),
                                           command=self.Create)
        self.load_button = ctk.CTkButton(self.header_frame, text="Import", command=lambda: self.upload_csv())
        self.download_button = ctk.CTkButton(self.header_frame, text="Download", command=lambda: self.export_csv())
        self.clear_button = ctk.CTkButton(
            self.header_frame,
            text="Clear Cache",
            fg_color="#FF0000",  # Red background color
            hover_color="#CC0000",  # Darker red when hovered
            text_color="#FFFFFF",  # White text color
            command=lambda: self.clear()
        )
        self.filters_label = ctk.CTkLabel(master=self.header_frame, text="Sort by:")
        selected_option = ctk.StringVar(value="Company")
        self.filters = ctk.CTkOptionMenu(
            master=self.header_frame,
            values=["Company", "Location", "Status"],
            variable=selected_option,
        )
        self.filters.configure(command=lambda value, filters=self.filters: self.sort(value))
        self.table = None
        ctk.set_appearance_mode("Light")
        # ctk.set_default_color_theme("blue")
        self.create_button.pack(side="left", padx=10, pady=10)
        self.load_button.pack(side="left", padx=10, pady=10)
        self.download_button.pack(side="left", padx=10, pady=10)
        self.filters_label.pack(side="left", padx=10, pady=10)
        self.filters.pack(side="right", padx=10, pady=10)
        self.header_frame.pack(side="top", pady=20)
        self.sort("Status")
        self.table_frame.pack(side="bottom", fill=ctk.BOTH, expand=1)

    def Create(self):
        def add():
            # Get the input values
            company = entry_company.get()
            position = entry_position.get()
            location = entry_location.get()

            # Check if any of the fields are empty
            if not company or not position or not location:
                messagebox.showerror("Input Error", "Please fill in all fields")
                return

            data = {"Company": [company], "Position": [position], "Location": [location], "Status": ["Not Applied"]}
            df = pd.DataFrame(data)
            df.to_csv(Output_path, index=False)
            self.load_csv()                     # Adds output to data
            self.display_csv(Data_path)
            return

        def minimize():
            self.form_frame.pack_forget()
            self.mainframe.destroy()
            return

        exists = self.form_frame.winfo_children()
        if exists:
            minimize()
            return

        if not exists:
            self.mainframe = ctk.CTkFrame(self.form_frame)
            # Create input fields
            label_company = ctk.CTkLabel(self.mainframe, text="Company:")
            label_company.grid(row=0, column=0, padx=10, pady=10)
            entry_company = ctk.CTkEntry(self.mainframe)
            entry_company.grid(row=0, column=1, padx=10, pady=10)

            label_position = ctk.CTkLabel(self.mainframe, text="Position:")
            label_position.grid(row=0, column=2, padx=10, pady=10)
            entry_position = ctk.CTkEntry(self.mainframe)
            entry_position.grid(row=0, column=3, padx=10, pady=10)

            label_location = ctk.CTkLabel(self.mainframe, text="Location:")
            label_location.grid(row=0, column=5, padx=10, pady=10)
            entry_location = ctk.CTkEntry(self.mainframe)
            entry_location.grid(row=0, column=6, padx=10, pady=10)

            # Create Add button
            button_add = ctk.CTkButton(self.mainframe, text="Add", command=add, width=60)
            button_add.grid(row=0, column=7, padx=10, pady=10)

            # Create Close button
            button_close = ctk.CTkButton(self.mainframe, text="-", font=("Arial", 18), width=30, command=minimize)
            button_close.grid(row=0, column=8, padx=10, pady=10)

            self.mainframe.pack()

        self.form_frame.pack()
        return
    def load_csv(self):
        file_path = Output_path
        if file_path:
            try:
                df1 = pd.read_csv(Data_path)

                # Read the second CSV file
                df2 = pd.read_csv(Output_path)

                # Ensure the columns are the same and in the same order
                common_columns = ['Company', 'Position', 'Location', 'Status']
                df1 = df1[common_columns]
                df2 = df2[common_columns]

                # Append the rows of the first DataFrame to the second DataFrame
                combined_df = pd.concat([df1, df2], ignore_index=True)

                # Save the combined DataFrame back to the second CSV file
                combined_df.to_csv(Data_path, index=False)
                self.display_csv(Data_path)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file: {e}")
        return

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:  # Check if a file has been submitted
            Input = pd.read_csv(file_path)
            status = []
            pos = []
            comp = []
            loc = []
            length = len(Input['Position'])
            count = 0

            for i in range(0, length):
                pos.append(Input['Position'].iloc[i])
                comp.append(Input['Company'].iloc[i])
                status.append(Input['Status'].iloc[i])
                loc.append(Input['Location'].iloc[i])
                count += 1
                data = {"Company": comp, "Position": pos, "Location": loc,
                        "Status": status}  # Writes to the output file should be done outside of loop
                df = pd.DataFrame(data)
                df.to_csv(Output_path, index=False)
                print("Loading")
                self.load_csv()
        else:
            messagebox.showwarning("No file selected", "Please select a CSV file to upload.")
        return

    def display_csv(self, file_path):

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        df = pd.read_csv(file_path)

        self.table = ctk.CTkScrollableFrame(self.table_frame)
        self.table.pack(fill=ctk.BOTH, expand=1)

        cols = [item for item in list(df.columns) if item != "Status"]
        cols.append("Application Status")  # Add the new "Call Status" column

        # Create table headers
        for i, col in enumerate(cols):
            label = ctk.CTkLabel(self.table, text=col, font=("Arial", 16, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

        # Create table data and Call Status dropdown
        for i, row in df.iterrows():
            for j, val in enumerate(row):
                label = ctk.CTkLabel(self.table, text=str(val), font=("Arial", 14))
                label.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")

            status = df["Status"].iloc[i]

            # Add Call Status dropdown
            status_var = ctk.StringVar(value=status)
            dropdown = ctk.CTkOptionMenu(
                self.table,
                variable=status_var,
                values=["Not Applied", "Submitted", "Responded", "DNA", "Rejected"],
                button_color=self.get_color(status),
                fg_color=self.get_color(status)
            )
            dropdown.configure(command=lambda value, i=i, dropdown=dropdown: self.change_color(value, i, dropdown))
            dropdown.grid(row=i + 1, column=len(cols) - 1, padx=5, pady=5, sticky="nsew")

            # Add a notes button
            notes_button = ctk.CTkButton(self.table, text="Notes")
            notes_button.configure(command=lambda i=i: self.open_more_info_window(i))
            notes_button.grid(row=i + 1, column=len(cols), padx=5, pady=5, sticky="nsew")

        for i in range(len(cols)):
            self.table.grid_columnconfigure(i, weight=1)
        return

    def change_color(self, value, i, dropdown):
        print("changing color")
        new_color = self.get_color(value)
        dropdown.configure(button_color=new_color, fg_color=new_color)
        self.change_status(value, i, dropdown)

    def get_color(self, value):
        color_map = {
            "Not Applied": "gray",
            "Submitted": "orange",
            "Responded": "green",
            "DNA": "purple",
            "Rejected": "red"
        }
        return color_map.get(value, "gray")

    def change_status(self, value, i, dropdown):
        # Load the CSV file
        df = pd.read_csv(Data_path)

        match = re.search(r'(\d+)$', str(dropdown))
        if match:
            i = int(match.group(1))
        else:
            i = 1

        # Change the status column
        df.loc[i - 1, 'Status'] = value

        # Save the updated dataframe back to the CSV file
        df.to_csv(Data_path, index=False)

        return

    def open_more_info_window(self, i):
        Data = pd.read_csv(Data_path)

        # Create the new window
        new_window = ctk.CTkToplevel(root)
        new_window.title(f"Notes for " + Data["Position"].iloc[i]+" at " + Data["Company"].iloc[i])
        new_window.geometry("900x400")
        new_window.configure(fg_color="white")

        # Make the new window stay in front of the root window
        new_window.transient(root)
        new_window.focus()
        notes_frame = ctk.CTkFrame(new_window)
        notes_frame.pack(fill="both", expand=True, side="right", padx=10, pady=10)
        notes_frame.configure(fg_color="white")

        # Notes section
        notes_label = ctk.CTkLabel(notes_frame, text="Notes:", anchor="w", text_color="black")
        notes_label.pack(fill="x", padx=10)

        notes_text = ctk.CTkTextbox(notes_frame)
        notes_text.pack(fill="both", expand=True, padx=10, pady=5)

        notes = pd.read_csv(Notes_path)
        exist = False
        j=0
        # Load existing notes if any
        for row in range(len(notes["Job"])):
            job = Data["Position"].iloc[i]+" at " + Data["Company"].iloc[i]
            if job == notes["Job"].iloc[row] and len(str(notes["Notes"].iloc[row])) > 3:
                notes_text.insert("1.0", notes["Notes"].iloc[row])
                exist = True
                j = row
                break
        def delete(i):
            new_window.destroy()
            data = pd.read_csv(Data_path)
            try:
                data = data.drop(data.index[i])
            except:
                return

            # Write the DataFrame back to a CSV file
            data.to_csv(Data_path, index=False)
            self.display_csv(Data_path)
            return

        delete_button = ctk.CTkButton(
            notes_frame,
            text="Delete Lead",
            fg_color="#FF0000",  # Red background color
            hover_color="#CC0000",  # Darker red when hovered
            text_color="#FFFFFF"  # White text color
        )
        delete_button.configure(command=lambda i=i:
        delete(i))
        delete_button.pack(side="bottom", anchor="e", pady=0)

        # Bind the save_notes function to the window close event
        new_window.protocol("WM_DELETE_WINDOW",
                            lambda: (self.save_notes(i, notes, exist, notes_text, Data, j), new_window.destroy()))
        return

    def save_notes(self, i, notes, exist, notes_text, Data, row):
        print("Saves")
        job = Data["Position"].iloc[i] + " at " + Data["Company"].iloc[i]
        if exist:
            notes["Notes"].iloc[row] = str(notes_text.get("1.0", "end-1c"))
        else:
            new_row = {col: '' for col in notes.columns}  # Create an empty row with the same columns
            new_row["Job"] = job  # Set the new line name
            text = notes_text.get("1.0", "end-1c")
            if text:
                new_row["Notes"] = text
                notes = notes.append(new_row, ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        notes.to_csv(Notes_path, index=False)
        return



    def sort(self, option):
        # Read the CSV file into a DataFrame
        data = pd.read_csv(Data_path)

        if option == "Company":
            data['company_order'] = data["Company"].apply(lambda x: x)
            # Sort the DataFrame by alphabet and then number

            sortedvals = data.sort_values(by=['company_order'])
            # Drop the temporary columns as they are no longer needed
            sortedvals = sortedvals.drop(columns=['company_order'])
            sortedvals.to_csv(Sorted_path, index=False)

        elif option == "Status":
            # Define the custom order for sorting
            status_order = {"Not Applied": 0, "Submitted": 1, "Responded": 2, "DNA": 3, "Rejected": 4}
            # Add a column with the custom order values
            data['status_order'] = data['Status'].map(status_order)
            sortedvals = data.sort_values(by='status_order')
            sortedvals = sortedvals.drop(columns=['status_order'])
            sortedvals.to_csv(Sorted_path, index=False)

        elif option == "Location":
            data['state'] = data['Location'].apply(lambda x: x.split()[-1] if isinstance(x, str) else x)
            sortedvals = data.sort_values(by='state')
            sortedvals = sortedvals.drop(columns=['state'])
            sortedvals.to_csv(Sorted_path, index=False)

        out = pd.read_csv(Sorted_path)
        out = out[["Company", "Position", "Location", "Status"]]
        out.to_csv(Data_path, index=False)
        self.display_csv(Data_path)
        return

    def export_csv(self):
        # Get the user's desktop directory
        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Define the folder path for "Job Applications" on the Desktop
        job_applications_folder = os.path.join(desktop_dir, 'Job Applications')

        # Ensure the "Job Applications" folder exists (create it if necessary)
        if not os.path.exists(job_applications_folder):
            os.makedirs(job_applications_folder)
            print(f"Created folder: {job_applications_folder}")

        # Get the current date formatted as YYYY-MM-DD
        current_date = datetime.now().strftime("%Y-%m-%d")
        # Create the new file name with the date
        new_file_name = f"JobList_{current_date}.csv"
        # Define the destination path in the "Job Applications" folder
        destination_path = os.path.join(job_applications_folder, new_file_name)
        shutil.copy(Data_path, destination_path)
        return

    def clear(self):
        def delete():
            os.remove(Data_path)       ### Deletes cache
            os.remove(Output_path)
            os.remove(Notes_path)
            os.remove(Sorted_path)

            if not os.path.isfile(Sorted_path):
                print("creating sorted")
                with open(Sorted_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Company", "Position", "Location", "Status"])
            if not os.path.isfile(Data_path):
                print("creating data")
                with open(Data_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Company", "Position", "Location", "Status"])
            if not os.path.isfile(Notes_path):
                print("creating data")
                with open(Notes_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Job", "Notes"])

        response = messagebox.askokcancel("Warning", "Table will be emptied but automatically download,\nDo you want to proceed?")

        if response:  # True if "OK" is pressed
            self.export_csv()
            delete()
        else:
            print("Clear Cache was canceled.")
        return


if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernCSVViewerApp(root)
    root.mainloop()
