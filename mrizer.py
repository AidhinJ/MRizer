import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import settings2
import PhotoSorter
import MR_Cards
import properties_GUI
import detect_mounting

photosorter = PhotoSorter.PhotoSorter()

def get_version():
    file_size = os.path.getsize('mrizer.py')
    return f'1.{str(file_size / 1000)[:4]}'

def open_folder(dir):
    #Check if there's contents
    try:
        contents = os.listdir(dir)
    except NameError:
        return
    
    if contents:
        print('There are files in output directory')

    # Open the folder in file explorer
    if os.name == 'nt':  # Windows
        subprocess.Popen(['explorer', dir])
    elif os.name == 'posix':  # macOS/Linux
        subprocess.Popen(['xdg-open', dir])

def mrize():
    # Before we begin, turn off detect mounting
    detect_mounting.dm.stop_listen()
    try:
        photosorter.tasks()
    except Exception as e:
        tk.messagebox.showinfo(e.args[0], e.args[1])
    # Resume detect mounting
    detect_mounting.dm.resume_listen()
        

def main():
    root = tk.Tk()
    root.title(f"MRizer v{get_version()}")

    mrize_ico_path = "MRizer.png"

    logo_image = tk.PhotoImage(file=mrize_ico_path)  # Replace with your image path
    root.wm_iconphoto(False, logo_image)
    
    mr_cards = MR_Cards.MR_Cards(height=100, width=100, bg='Navy')
    mr_cards.grid(row=0, column=0, sticky='n')

    mrize_ico = tk.PhotoImage(file=mrize_ico_path)
    button = tk.Button(root, image=mrize_ico, command=mrize)
    button.grid(row=1, column=0)

##    task_manager = tk.Text(width=20, height=10)
##    task_manager.pack()

    properties = properties_GUI.PropertiesFrame(root, borderwidth=5, bg='Grey')
    properties.grid(row=0, column=1, sticky='n')

    try:
        open_folder(f"{settings2.default['output']}/Photos")
    except Exception as e:
        pass
##        tk.messagebox.askquestion("MR-izer setup", "Welcome to MRizer. Would you like to quickly setup?")
    root.mainloop()

if __name__ == "__main__":
    main()
