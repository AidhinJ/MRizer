import json
import tkinter as tk
from tkinter.filedialog import askdirectory

# Loads default settings as soon as program starts up
with open("data.json", 'r') as file:
    default = json.load(file)

ext = ' - Bank'
    
class DirSettings:
    def __init__(self):
        self.photos_dir = 'Select Directory'
        self.devices = [{'name': 'Camera', 'dir': '/run/user/1000/gvfs/gphoto2:host=NIKON_NIKON_DSC_COOLPIX_B500_000090070169/DCIM/100NIKON/', 'ext': '', 'showinfo': 'Copying photos...'},
                        {'name': '360s', 'dir': '/run/user/1000/gvfs/gphoto2:host=Ricoh_Company__Ltd._RICOH_THETA_SC2_20104154/DCIM/101RICOH/', 'ext': ext, 'showinfo': 'Copying 360s...'},
                        {'name': 'Disto', 'dir': '/media/c3po/07EF-0121/Apex Backups', 'ext': '', 'showinfo': 'Copying from disto...'}]
        self.output = default['output']
        self.output_var = tk.StringVar(value=f'Output: {self.output}')
        

    def open_dir_win(self, master):
        window = tk.Toplevel(master)
        window.title("Directories")
        window.geometry("200x200")

        add_dir_button = tk.Button(window, text='+',
                                   command=lambda: Device.add(master=window))
        add_dir_button.pack()
        for data in self.devices:
            device = Device(data['dir'], window, name=data['name'], ext=data['ext'], showinfo=data['showinfo'], bg='Gray')
            device.pack()
                
    def select_output(self):
        output = askdirectory(initialdir="/home")
        if output:  # If we cancel
            self.output = output
            self.output_var.set(f'Output: {output}')
            with open("data.json", 'w') as file:
                default['output'] = output
                json.dump(default, file)

class Device(tk.Frame):
    def __init__(self, dir, *args, name='Device', ext='', showinfo='', **kwargs):
        self.dir = dir
        self.name = name
        self.ext = ext
        self.showinfo = showinfo
        super().__init__(*args, **kwargs)
        self.button_var = tk.StringVar(value=f'{name}: {dir}')
        button = tk.Button(self, textvariable=self.button_var, command=self.select_dir)
        button.grid(column=0, row=0)
        remove_button = tk.Button(self, text='-', command=self.remove)
        remove_button.grid(column=1, row=0)
        self.data = {'dir': dir, 'ext': ext, 'showinfo': showinfo}

    @classmethod
    def add(cls, master, dir='Select', ext='', showinfo=''):
        device = cls("Select", master, ext=ext, showinfo=showinfo, bg='Gray')
        device.pack()
        
    def remove(self):
        del self.button_var
        self.destroy()
        
    def select_dir(self):
        self.dir = askdirectory(initialdir='/run/user/1000/gvfs/')
        self.button_var.set(f'{self.name}: {self.dir}')
        
        
                
