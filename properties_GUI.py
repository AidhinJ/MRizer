import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser as wb
import json
import extras
import fuel_claim_calc
import upload_to_drive

with open('data.json') as file:
    data = json.load(file)


class OpenLinks_GUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.links = data['links']
        for website in self.links:
            button = tk.Button(self, text=f'Open {website}')
            button.pack(fill=tk.X)
            button.bind('<Button-1>', self.open)
        self.pack()

    def open(self, event):
        text = event.widget['text']
        text = text[5:]
        wb.open(self.links[text])

    def open_all(self):
        for website in self.links.values():
            wb.open(website)

# C is short for collapsable like C_Device or C_OpenLinks

class C_Device(extras.CollapsibleFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=tk.X)
        dir_button = tk.Button(self._contents, text='Nothing here')
        dir_button.pack()
        

class CollapsibleDevice(extras.CollapsibleFrame):
    ID = 0

    def __init__(self, *args, device={"name": "No Name", "dir": "", "is_360": False, "resizable": True}, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=tk.X)

        self.id = CollapsibleDevice.ID
        CollapsibleDevice.ID += 1

        self.name_var = tk.StringVar(self._contents, value=device["name"])
        self.name_var.trace("w", self.notify_changes)
        name_label = tk.Label(self._contents, text="Name:")
        name_label.grid(column=0, row=0, sticky=tk.W)
        name_entry = tk.Entry(self._contents, textvariable=self.name_var)
        name_entry.grid(column=1, row=0, sticky=tk.W)

        self.path = device["dir"]
        select_button = tk.Button(self._contents, text="Select Path", command=self.select_path)
        select_button.grid(column=0, row=1, sticky=tk.W)

        self.path_var = tk.StringVar(self._contents, value=self.path)
        self.path_var.trace("w", self.notify_changes)
        self.path_entry = tk.Entry(self._contents, textvariable=self.path_var, width=50)
        self.path_entry.grid(column=1, row=1, sticky=tk.W)

        self.is_360_var = tk.BooleanVar(self._contents, value=device["is_360"])
        self.is_360_var.trace("w", self.notify_changes)
        check_button_360 = tk.Checkbutton(self._contents, text="Is 360 directory", variable=self.is_360_var)
        check_button_360.grid(column=0, row=2, sticky=tk.W)

        self.resizable_var = tk.BooleanVar(self._contents, value=device["resizable"])
        self.resizable_var.trace("w", self.notify_changes)
        check_resizable = tk.Checkbutton(self._contents, text="Auto Resize\n(1920x1080p)", variable=self.resizable_var)
        check_resizable.grid(column=0, row=3, sticky=tk.W)

        remove_button = tk.Button(self._contents, text="Remove", command=self.remove)
        remove_button.grid(column=0, row=10, sticky=tk.W)  # Making sure it's the last option

        self.save_button = tk.Button(self._contents, text="Saved", bg="green", command=self.save_changes, state=tk.DISABLED)
        self.save_button.grid(column=1, row=4, sticky=tk.E)

    def select_path(self):
        self.path = filedialog.askdirectory()
        if self.path:
            self.path_var.set(self.path)

    def remove(self):
        result = messagebox.askquestion(
            "Confirm Remove",
            f'Are you sure you want to Remove "{self.name_var.get()}" from MRizer?'
        )
        if result == "yes":
            with open('data.json', 'w') as file:
                try:
                    devices = data["devices"]
                    del devices[self.id]  # Indexing the array using ID
                except IndexError:  # If IndexError, device doesn't exist. Just leave it
                    pass
                json.dump(data, file)
            self.destroy()

    def notify_changes(self, var_name=0, index=0, mode=0):
        self.save_button["text"] = "Save changes"
        self.save_button["state"] = tk.NORMAL

    def save_changes(self):
        devices = data["devices"]
        try:
            device = devices[self.id]  # Indexing the array using ID
        except IndexError:  # If IndexError, device doesn't exist, hence create it.
            device = {}
            devices.append(device)
            
        with open('data.json', 'w') as file:
            device['name'] = self.name_var.get()
            device['dir'] = self.path_var.get()
            device['is_360'] = self.is_360_var.get()
            device['resizable'] = self.resizable_var.get()
            json.dump(data, file)  # Save
            
        self.save_button['text'] = 'Saved'
        self.save_button['state'] = tk.DISABLED


class CUploadToDrive(extras.CollapsibleFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=tk.X)

        self.folder_id_var = tk.StringVar(self._contents, value='device["name"]')
        folder_id_label = tk.Label(self._contents, text="Folder ID:")
        folder_id_label.grid(column=0, row=0, sticky=tk.W)
        folder_id_entry = tk.Entry(self._contents, textvariable=self.folder_id_var)
        folder_id_entry.grid(column=1, row=0, sticky=tk.W)

        self.folder_360_id_var = tk.StringVar(self._contents, value='device["name"]2')
        folder_360_id_label = tk.Label(self._contents, text="360 Folder ID:")
        folder_360_id_label.grid(column=2, row=0, sticky=tk.W)
        folder_360_id_entry = tk.Entry(self._contents, textvariable=self.folder_360_id_var)
        folder_360_id_entry.grid(column=3, row=0, sticky=tk.W)

        upload_button = tk.Button(self._contents, text="Upload", command=upload_to_drive.execute)
        upload_button.grid(column=0, row=1, sticky=tk.W)

        self.is_auto_upload = tk.BooleanVar(self._contents)
        check_auto_upload = tk.Checkbutton(self._contents, text="Auto Upload", variable=self.is_auto_upload)
        check_auto_upload.grid(column=0, row=2, sticky=tk.W)

        
class C_OpenLinks(extras.CollapsibleFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=tk.X)
        openLinks_gui = OpenLinks_GUI(self._contents)
        open_all_button = tk.Button(self,
                                    text='Open All',
                                    command=openLinks_gui.open_all)
        open_all_button.pack(fill=tk.X)


class C_InputOutput(extras.CollapsibleFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=tk.X)
        self.output_button = tk.Button(self, text=f'Output: {data["output"]}', bg='#FFEEAA', command=self.select_output_path)
        self.output_button.pack(fill=tk.X)

        add_device_button = tk.Button(self._contents, text='+', command=self.add_device)
        add_device_button.pack()
        
        # Load all devices
        for device in data['devices']:
            CollapsibleDevice(master=self._contents, title=device['name'], device=device, borderwidth=5)

    def select_output_path(self):
        self.output_path = filedialog.askdirectory()
        if self.output_path:
            with open('data.json', 'w') as file:
                data['output'] = self.output_path
                json.dump(data, file)
            self.output_button['text'] = f'Output: {self.output_path}'

    def add_device(self):
        device = CollapsibleDevice(master=self._contents, title='No Name', borderwidth=5)
        device.notify_changes()
            


class C_FuelClaim(extras.CollapsibleFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=tk.X)
        self.input = tk.Text(self._contents)
        self.input.pack(fill=tk.X)

        # Create a button to trigger copying
        self.copy_button = tk.Button(self._contents,
                                     text="Copy to Clipboard",
                                     bg='White',
                                     command=self.copy_to_clipboard)
        self.copy_button.pack()

    def copy_to_clipboard(self):
        """get_wa_page and copy to clipboard.

        Args:
            data (str): The text content of the page.

        Returns:
            str: A str of the fuel claim with tabs. Mean't to be pasted in the
            fuel claim.
        """
        def reset():
            self.copy_button['text'] = 'Copy to Clipboard'
            self.copy_button['bg'] = 'White'
            self.copy_button['activebackground'] = 'White'

        data = self.input.get("1.0", tk.END)
        apps = fuel_claim_calc.get_wa_page(data)
        string = ''
        for datetime, name, distance in apps:
            string=f'{string}{name[:8]}\t{distance}\t'
            
        self.clipboard_clear()  # This is needed to overwrite previous clipboard content
        self.clipboard_append(string)

        self.copy_button['text'] = 'Copied to Clipboard'
        self.copy_button['bg'] = self.copy_button['activebackground'] = 'gray'
        self.copy_button.after(10000, reset)



class PropertiesFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        collapsible_option = C_InputOutput(self, title='Input/Output')
        collapsible_option = C_OpenLinks(self, title='Open links')
        collapsible_option = CUploadToDrive(self, title='Upload to Drive')
        collapsible_option = C_FuelClaim(self, title='Fuel claim')
        collapsible_option = C_Device(self, title='Tasks')

        
if __name__ == "__main__":
    root = tk.Tk()
    pf = PropertiesFrame(root)
    pf.pack()
    
