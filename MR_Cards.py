import tkinter as tk
from datetime import datetime as dt
import logging
import json
import extras
import rat_info
import fuel_claim_calc

# Load data
with open('data.json') as file:
    data = json.load(file)
    
# Configure logging (optional, but recommended for clean formatting)
logging.basicConfig(filename="mr.log", level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a logger for this module
logger = logging.getLogger(__name__)

apps_dict = {}
end_time = dt.today()
class MR_Cards(tk.Frame):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = tk.Label(self, text='Appointment Date_time', width=30, height=2, bg='white', font=('Ariel', '12'))
        label.grid(row=0, column=0)

        label = tk.Label(self, text='MR Number', width=30, height=2, bg='white', font=('Ariel', '12'))
        label.grid(row=0, column=1)

        self.add_app_button = tk.Button(self, text='+', font=('Ariel', '30'), command=self.add_app)
        self.add_app_button.grid(row=0, column=2)

        self.app_frame = tk.Frame(self, width=100, height=30, bg='Grey')
        self.app_frame.grid(row=1, columnspan=3)

        tk.Button(self, text='Remove All', command=self.remove_all_apps).grid(row=0, column=3)

        # Bind Ctrl+h to the hotkey_function
        self.bind("<Button-1>", lambda event: self.focus_set())
        self.bind("<Control-v>", self.paste_rat) 
        
    def add_app(self, app_time='', mr=''):
        # If applying app_time, needs to be date_time
        app_row = App_Row(master=self.app_frame, app_time=app_time, mr=mr)
        app_row.check_valid_time(None) #Calling the binded event
        logger.info("Added appointment stack")

    def remove_all_apps(self):
        for index in list(apps_dict.keys()):
            apps_dict[index].remove()

    def enable_add(self, enabled=True):
        if enabled:
            self.add_app_button['state'] = tk.ACTIVE
        else:
            self.add_app_button['state'] = tk.DISABLED

    @staticmethod
    def rearrange():
        """Rearrange the app_row as well as apps_dict."""
        apps = sorted(apps_dict.items(), key=lambda x: x[1].date_time_var.get())
        number = 0
        apps_dict.clear()
        for id, app_row in apps:
            apps_dict[id] = app_row
            number+=1
            app_row.grid(row=number)

    def paste_rat(self, event):
        clipboard = self.clipboard_get()
        # If the clipboard contains a watsapp date_time it suggests it's watsapp
        if fuel_claim_calc.has_date_time(clipboard):
            apps = fuel_claim_calc.get_wa_page(clipboard)
        else:
            apps = rat_info.get_rat_page(clipboard)
            
        for app in apps:
            self.add_app(app_time=app[0], mr=app[1])
            
    
class App_Row(tk.Frame):
    ID = 0
    def __init__(self, *args, app_time='', mr='', **kwargs):
        super().__init__(*args, **kwargs)
        self.default_col = 'White'
        if app_time == '':
            app_time = dt.today()
        self.date_time_var = tk.StringVar(self, value=app_time)
        self.app_time = tk.Entry(self, width=23, font=('Ariel', '15'), borderwidth=5, textvariable=self.date_time_var)
        self.app_time.bind("<Key>", self.check_valid_time)
        self.app_time.grid(row=0, column=0)

        # Add Options
        collapsible_options = extras.CollapsibleFrame(self, title='Options')
        collapsible_options.grid(row=1, column=0, columnspan=2)
        options_frame = tk.Frame(collapsible_options._contents)
        options_frame.grid(row=0, column=0)
        
        collapsible_note = extras.CollapsibleFrame(options_frame, title='Notes') 
        collapsible_note.grid(row=0, column=0, sticky='N')
        label = tk.Label(collapsible_note._contents, text='Name: ')
        label.grid(row=0, column=0)
        self.note_name = tk.StringVar(self, value="Note.txt")
        entry = tk.Entry(collapsible_note._contents, textvariable=self.note_name)
        entry.grid(row=0, column=1)
        self.note = tk.Text(collapsible_note._contents, width=30, height=10)
        self.note.grid(row=1, column=0, columnspan=2)

        self.property_type = tk.StringVar(self, value='Bank')
        property_type_frame = tk.LabelFrame(options_frame, text='Property Type')
        property_type_frame.grid(row=0, column=1, sticky='N')
        public_radio = tk.Radiobutton(property_type_frame, text='Bank',
                                      variable=self.property_type,
                                      value='Bank',
                                      command=self.set_property_type)
        private_radio = tk.Radiobutton(property_type_frame, text='Private',
                                       variable=self.property_type,
                                       value='Pvt',
                                       command=self.set_property_type)
        public_radio.grid(row=1, column=0, sticky='W')
        private_radio.grid(row=2, column=0, sticky='W')

        self.MRnumber = tk.StringVar(self)
        self._360_name = tk.StringVar(self)
        file_name_frame = tk.LabelFrame(options_frame, text='File Names')
        file_name_frame.grid(row=0, column=2, sticky='N')
        label = tk.Label(file_name_frame, text='MR Number')
        label.grid(row=1, column=0)
        entry = tk.Entry(file_name_frame, textvariable=self.MRnumber)
        entry.grid(row=1, column=1)
        label = tk.Label(file_name_frame, text='360 File Name')
        label.grid(row=2, column=0)
        entry = tk.Entry(file_name_frame, textvariable=self._360_name)
        entry.grid(row=2, column=1)
        
        # Create ID. Every App has it's ID
        App_Row.ID += 1
        self.id = App_Row.ID
        apps_dict[App_Row.ID] = self

        # Note var
        self.note_var = tk.StringVar(self)
        
        mr_labelframe = tk.LabelFrame(self, text=mr, width=300, height=50, font=('Ariel', '12'), bg='white')
        mr_labelframe.bind('<Button-1>', self.mr_rename)
        mr_labelframe.grid(row=0, column=1)
        mr_labelframe.ent_var = tk.StringVar(self, value='MR') # Create a var in the widget

        # Access arranged?
        self.access_text_var = tk.StringVar(self, value='Access')
        self.access_text = tk.Label(mr_labelframe,
                                    textvariable=self.access_text_var,
                                    bg='White',
                                    fg='Green')
        self.access_text.place(x=100, y=-22)
        
        if mr == '':
            self.mr_rename(widget=mr_labelframe)
        else:
            self.set_all_from_text(mr, mr_labelframe)

        # Remove app button
        remove_label_button = tk.Button(mr_labelframe, text='-', command=self.remove)
        remove_label_button.place(x=250, y=-5)

    def mr_rename(self, event=None, widget=None):
        def rename(e):
            text = label.ent_var.get()
            if text == '':
                text = 'MR'
            self.set_all_from_text(text, label)
            entry.destroy()
            logger.info(f"change text to: {text}")

        def cancel(event):
            if label['text'] == '':
                label['text'] = 'MR'
            label.ent_var.set(orig)
            entry.destroy()

        def custom_paste(event):
            try:
                event.widget.delete("sel.first", "sel.last")  # Remove selected text
            except:
                pass
            event.widget.insert("insert", event.widget.clipboard_get())  # Paste from clipboard
            return "break"  # Prevent default paste behavior

        # label must be the widget (label widget)
        if widget:
            label = widget
        else:
            label = event.widget
        orig = label.ent_var.get()
        entry = tk.Entry(label, textvariable=label.ent_var)
        entry.bind("<<Paste>>", custom_paste)
        entry.focus_set()
        entry.place(x=0, y=-0)
        entry.select_range(start=0, end=len(label.ent_var.get()))
        entry.bind('<Return>', rename)
        entry.bind('<FocusOut>', rename)
        entry.bind('<Escape>', cancel)
        
        

    def set_all_from_text(self, text, label):
        """Set the Appointment options, etc(based on the inputted text). The Label
Widget is needed to assign the main entry"""
        global end_time
        mr_name = text[0:8]
        label['text'] = mr_name
        if text.lower() == 'end':
            end_time = dt.fromisoformat(self.app_time.get())
            self.app_time["bg"] = self.default_col = 'Yellow'
            return
        property_type = self.get_property_type(text)
        self.property_type.set(property_type)
        self.MRnumber.set(mr_name)
        self._360_name.set(mr_name + ' - ' + property_type)
        if property_type == 'Bank':
            label['fg'] = 'Orange'
        else:
            label['fg'] = 'Purple'
        if mr_name in data["storedMRnumbers"]:
            label['bg'] = 'Gray'
        else:
            label['bg'] = 'White'
        self.access_text_var.set(self.get_access_type(text))
        self.access_text.place(x=100, y=-22) # Place the access text.

    def get_property_type(self, text):
        if text[-1].lower() == 'p' or 'private' in text.lower() or 'pvt' in text.lower():
            return 'Pvt'
        else:
            return 'Bank'

    def set_property_type(self):
        self._360_name.set(self.MRnumber.get() + ' - ' + self.property_type.get())

    def get_access_type(self, text):
        if 'no access' in text.lower() or 'na' in text.lower():
            self.access_text['fg'] = 'Red'
            return 'No access'
        else:
            self.access_text['fg'] = 'Green'
            return 'Access'
    
    def remove(self):
        del apps_dict[self.id]
        self.destroy()

    def check_valid_time(self, e):
        def check():
            try:
                dt.strptime(self.date_time_var.get(), '%Y-%m-%d %H:%M:%S.%f')
                self.app_time["bg"] = self.default_col
            except ValueError:
                try:
                    dt.strptime(self.date_time_var.get(), '%Y-%m-%d %H:%M:%S')
                    self.app_time["bg"] = self.default_col
                except ValueError:
                    self.app_time["bg"] = 'Red'
                MR_Cards.rearrange()
                return
            MR_Cards.rearrange()
        self.after(100, check)




if __name__ == '__main__':
    mr_cards = MR_Cards(height=100, width=100, bg='Blue')
    mr_cards.pack()
    

