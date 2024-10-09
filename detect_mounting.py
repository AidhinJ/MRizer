import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json
import logging

# Load data from startup
with open('data.json') as file:
    data = json.load(file)

# Create a logger for this module
##logger = logging.getLogger(__name__)

directory_paths = "/run/user/1000/gvfs", "/media/"
with open('ignored_dirs.json') as file:
    ignore_dir_data = json.load(file)
    ignore_devices = ignore_dir_data["ignored_dirs"]

def save_ignored_devices():
    """Save the file paths to ignored_dirs."""
    # So that if device is detected again it won't be prompted to be added

    with open('ignored_dirs.json') as file:
        ignore_dir_data = json.load(file)
    
    with open('ignored_dirs.json', 'w') as file:
        ignore_dir_data["ignored_dirs"].extend(ignore_devices)
        json.dump(ignore_dir_data, file)

class DetectMounting:
    def get_values_for_key(self, list_of_dicts, key):
        """Gets the values for a given key from a list of dictionaries.

        Args:
            dicts: A list of dictionaries.
            key: The key to search for.

            Returns:
                A list of values corresponding to the given key.
        """

        return [dict[key] for dict in list_of_dicts if key in dict]

    def detect_mounting(self, path, mounting_type, input_output_gui):
        items = os.listdir(path)
        if items:
            for device in items:
                device_path = os.path.join(path, device)
##                saved_dirs = self.get_values_for_key(data["devices"], "dir")
                if device_path not in ignore_devices:
                    answer = messagebox.askyesnocancel(
                        f"{mounting_type} detected.",
                        f"{device}\n\nWould you like to add this {mounting_type} to MRizer?"
                    )
                    if answer is True:
                        path = filedialog.askdirectory(initialdir=f"{path}/{device}")
                        input_output_gui.add_device(title=f'{device}', device={"name": f'{device}', "dir": f"{path}", "is_360": False, "resizable": True})
                        ignore_devices.append(device_path)
                    elif answer is False:
                        ignore_devices.append(device_path)
                        save_ignored_devices()
                    else:
                        ignore_devices.append(device_path)
                    print(ignore_devices)

    def check_media(self, input_output_gui):
        username = os.listdir(directory_paths[1])[0]
        path = f"{directory_paths[1]}/{username}"
        self.detect_mounting(path, "Media Directory", input_output_gui)

    def check_devices(self, input_output_gui):
        path = directory_paths[0]
        self.detect_mounting(path, "Device", input_output_gui)

    def listen(self, input_output_gui):
        """Checks mounting directories every 3 seconds for devices."""
        self.widget = input_output_gui
        def task():
            try:
                self.check_media(input_output_gui)
                self.check_devices(input_output_gui)
            except FileNotFoundError as e:
                print(e)
            self.timer_id = input_output_gui.after(3000, task)
        task() # Start

    def stop_listen(self):
        self.widget.after_cancel(self.timer_id)

    def resume_listen(self):
        self.listen(self.widget)

dm = DetectMounting()


if __name__ == "__main__":
    class IOGuiTest(tk.Frame):
        def add_device(self, title, device):
            print('Adding', title, device)

    win = tk.Tk()
    input_output_gui = IOGuiTest(win, width=1000, height=1000, bg='Blue')
    input_output_gui.grid(column=0, row=0)
    button = tk.Button(input_output_gui, text='Hello', command=dm.stop_listen)
    button.grid(column=0, row=0)
            
    dm.listen(input_output_gui)
