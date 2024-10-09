import tkinter as tk
import extras

class Autoload_GUI(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        options = ["By Capture time", "By Watsapp (Experimental)"]

        self.option_var = tk.StringVar(self)
        self.option_var.set(options[0])

        opmenu = tk.OptionMenu(self, self.option_var, *options, command=self.change_type)
        opmenu.pack()
        
        self.settings_frame = tk.Frame(self, height=10, width=10)
        self.settings_frame.pack()
        button = tk.Button(self, text='Auto Load')
        button.pack()
        
        self.capture_time = Capture_time(master=self.settings_frame)
        self.wa = By_Watsapp(master=self.settings_frame)
        self.wa.pack()

    def change_type(self, option):
        if option == "By Capture time":
            self.capture_time.pack()
            
        if option == "By Watsapp (Experimental)":
            self.wa.pack()

class Capture_time(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = tk.Label(self, text="Paste/Write MR numbers in entry. Be sure they're seperated by newline.", wrap=230)
        label.grid(row=0, column=0, columnspan=3, sticky=tk.W)
        text = tk.Text(self, width=20, height=6)
        text.grid(row=1, column=0, columnspan=3)

        label = tk.Label(self, text="Time Seperation:")
        label.grid(row=2, column=0, sticky=tk.W)
        self.spinbox_val = tk.IntVar(self, value=20)
        spinbox = tk.Spinbox(self, width=4, textvariable=self.spinbox_val, from_=0, to=1000)
        spinbox.grid(row=2, column=1, sticky=tk.W)
        label = tk.Label(self, text="Minutes")
        label.grid(row=2, column=2, sticky=tk.W)


        
class By_Watsapp(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
##        open_wa_button = tk.Button(self, text='Open Watsapp', command=self.open_wa)
##        open_wa_button.grid(row=0, column=0, columnspan=3)
        label = tk.Label(self, text="Paste Watsapp messages into entry.", wrap=230)
        label.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        self.text = tk.Text(self, width=20, height=6)
        self.text.grid(row=2, column=0, columnspan=3)
        self.text.bind("<<paste>>", extras.custom_paste)

    def extract_data():
        watsapp = text.get("1.0", tk.END).split('[')
        for message in watsapp:
            if 'Aidhin' in message:
                if 'i have access' in message.lower() or 'i have gained access' in m.lower():
                    print(message)


                    
if __name__ == "__main__":
    import MR_Cards
    
    mr_cards = MR_Cards.MR_Cards(height=100, width=100, bg='Navy')
    mr_cards.pack()
    autoload_gui = Autoload_GUI(height=100, width=200, bg='Gray', text='Autoload settings')
    autoload_gui.pack()
    

# Autoload by Capture time

##import webbrowser
##
##webbrowser.open('https://web.whatsapp.com')



