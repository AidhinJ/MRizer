import json
import tkinter as tk
from tkinter.filedialog import askdirectory

# Loads default settings as soon as program starts up
with open("data.json", 'r') as file:
    default = json.load(file)

##devices = [{'name': 'Camera', 'dir': '/run/user/1000/gvfs/gphoto2:host=NIKON_NIKON_DSC_COOLPIX_B500_000090070169/DCIM/101NIKON/', 'is_360': False, 'showinfo': 'Copying photos...', 'resizable': True},
##           {'name': '360s', 'dir': '/run/user/1000/gvfs/gphoto2:host=Ricoh_Company__Ltd._RICOH_THETA_SC2_20104154/DCIM/101RICOH/', 'is_360': True, 'showinfo': 'Copying 360s...', 'resizable': False},
##           {'name': 'Disto', 'dir': '/media/c3po/07EF-0121/Apex Backups', 'is_360': False, 'showinfo': 'Copying from disto...', 'resizable': False}]
devices = default['devices']
    
class DirSettings():
    def __init__(self):
        self.photos_dir = 'Select Directory'
        self.output = default['output']
        self.output_var = tk.StringVar(value=f'Output: {self.output}')
        

    def open_dir_win(self, master):
        window = tk.Toplevel(master)
        window.title("Directories")
##        window.geometry("600x200")

        add_dir_button = tk.Button(window, text='+',
                                   command=lambda: Device.add(master=window))
        add_dir_button.pack()
        for data in devices:
            device = Device(window,
                            name=data['name'],
                            dir=data['dir'],
                            is_360=data['is_360'],
                            showinfo=data['showinfo'],
                            resizable=data['resizable'],
                            bg='Gray')
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
    def __init__(self, *args, name='Device', dir=None, is_360=False, showinfo='', resizable=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir = dir
        self.name = name
        self.showinfo = showinfo
        self.button_var = tk.StringVar(value=f'{name}: {dir}')
        button = tk.Button(self, textvariable=self.button_var, command=self.select_dir)
        button.grid(column=0, row=0)
        remove_button = tk.Button(self, text='-', command=self.remove)
        remove_button.grid(column=1, row=0)

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
        

if __name__ == '__main__':
    window = tk.Tk()
    dirsettings = DirSettings()
    dirsettings.open_dir_win(window)
