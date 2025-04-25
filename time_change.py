import csv
import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta

def modify_time(time_str, hour_shift, min_shift, sec_shift):
    """Modify timestamp by shifting hours, minutes, and seconds."""
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
        dt += timedelta(hours=hour_shift, minutes=min_shift, seconds=sec_shift)
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Keep millisecond precision
    except Exception as e:
        print("Error modifying time:", e)
        return time_str

def process_csv(file_path, hour_shift, min_shift, sec_shift):
    """Process CSV file and shift timestamps."""
    base_name = os.path.basename(file_path)
    output_file = os.path.join(os.path.dirname(file_path), "mod_" + base_name)

    with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)  # Read header
        writer.writerow(header)  # Write header

        for row in reader:
            if len(row) > 1:
                row[1] = modify_time(row[1], hour_shift, min_shift, sec_shift)  # Modify time
            writer.writerow(row)

    print("Processed file saved as:", output_file)

def select_file():
    """Open file dialog and process CSV file with user-defined time shifts."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            shift_hours = int(entry_hours.get())
            shift_minutes = int(entry_minutes.get())
            shift_seconds = int(entry_seconds.get())
            process_csv(file_path, shift_hours, shift_minutes, shift_seconds)
        except ValueError:
            print("Please enter valid integer values for hours, minutes, and seconds.")

# GUI Setup
root = tk.Tk()
root.title("CSV Time Modifier")

tk.Label(root, text="Shift Hours (+/-):").grid(row=0, column=0)
entry_hours = tk.Entry(root)
entry_hours.grid(row=0, column=1)

tk.Label(root, text="Shift Minutes (+/-):").grid(row=1, column=0)
entry_minutes = tk.Entry(root)
entry_minutes.grid(row=1, column=1)

tk.Label(root, text="Shift Seconds (+/-):").grid(row=2, column=0)
entry_seconds = tk.Entry(root)
entry_seconds.grid(row=2, column=1)

tk.Button(root, text="Select CSV & Process", command=select_file).grid(row=3, column=0, columnspan=2)

root.mainloop()
