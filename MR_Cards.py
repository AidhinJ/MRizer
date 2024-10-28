import customtkinter as ctk
from datetime import datetime as dt

apps_dict = {}
end_time = dt.today()

class AppCard(ctk.CTkFrame):
    ID = 0
    def __init__(self, *args, app_time=dt.today(), mr='MR', **kwargs):
        super().__init__(*args, **kwargs)

        # Create ID. Every App has it's ID
        AppCard.ID += 1
        self.id = AppCard.ID
        apps_dict[AppCard.ID] = self

        # Create an Entry widget on the left side, Time
        self.date_time_var = ctk.StringVar(self, value=app_time)
        self.left_entry = ctk.CTkEntry(self, textvariable=self.date_time_var)
        self.left_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Create an Entry widget on the right side, MR number
        self.mr_number_var = ctk.StringVar(self, value=mr)
        self.right_entry = ctk.CTkEntry(self, textvariable=self.mr_number_var)
        self.right_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Create a remove widget on the right side
        self.remove_button = ctk.CTkButton(self, text='-', font=("Arial", 20), width=20)
        self.remove_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    def check_valid_time(self, e):
        def check():
            try:
                dt.strptime(self.date_time_var.get(), '%Y-%m-%d %H:%M:%S.%f')
                self.left_entry["bg"] = "White"
            except ValueError:
                try:
                    dt.strptime(self.date_time_var.get(), '%Y-%m-%d %H:%M:%S')
                    self.left_entry["bg"] = "White"
                except ValueError:
                    self.left_entry["bg"] = 'Red'
                MR_Cards.rearrange()
                return
            MRCards.rearrange()
        self.after(100, check)

        
class MRCards(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_app_button = ctk.CTkButton(self, text='Add appointment', command=self.add_app)
        self.add_app_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.initial_message_label = ctk.CTkLabel(self, text="Add an appointment\nOr paste from Rat/Watsapp", text_color='Grey')
        self.initial_message_label.grid(row=1, column=0, padx=100, pady=180, sticky="nsew")

    def add_app(self, app_time=dt.today(), mr='MR'):
        # If applying app_time, needs to be date_time
        self.initial_message_label.grid_forget()
        app_card = AppCard(self, app_time=app_time, mr=mr)
        app_card.check_valid_time(None) #Calling the binded event
##        logger.info("Added appointment stack")

    @staticmethod
    def rearrange():
        """Rearrange the app_row as well as apps_dict."""
        apps = sorted(apps_dict.items(), key=lambda x: x[1].date_time_var.get())
        number = 0
        apps_dict.clear()
        for id, app_card in apps:
            apps_dict[id] = app_card
            number+=1
            app_card.grid(row=number, column=0, padx=5, pady=5)



window = ctk.CTk()
window.configure(fg_color="gray")

frame = MRCards(window, width=370, height=500, fg_color='#AAAAAA', border_color='#FFCC70', border_width=2, orientation="vertical")
frame.pack(expand=True)
