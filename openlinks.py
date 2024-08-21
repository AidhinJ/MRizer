import tkinter as tk
import webbrowser as wb

class OpenLinks_GUI(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        button = tk.Button(self, text='Open All', command=self.open_all)
        button.pack(fill=tk.X)
        self.links = {'Watsapp': 'https://web.whatsapp.com/',
                      'RAT': 'https://rat.myroof.co.za/dashboard',
                      'Drive': 'https://drive.google.com/drive/u/1/folders/1WKGcfNlx7xHypydgUWWplPWDvtpyLyjb',
                      'Google Maps': 'https://www.google.com/maps/',
                      'Fuel Claim': 'https://docs.google.com/spreadsheets/d/1tqDsMnzfz3p-7KQeg2HhDUm7FstsXxBxGJUAWEGljdg/',
                      'Google One': 'https://one.google.com/u/1/storage/management/drive/large?g1_landing_page=1&utm_source=app_launcher&utm_medium=web&utm_campaign=all'
                      }
        for website in self.links:
            button = tk.Button(self, text=f'Open {website}')
            button.pack(fill=tk.X)
            button.bind('<Button-1>', self.open)

    def open(self, event):
        text = event.widget['text']
        text = text[5:]
        wb.open(self.links[text])

    def open_all(self):
        for website in self.links.values():
            wb.open(website)

if __name__ == "__main__":
    olg = OpenLinks_GUI()
    olg.pack()
##    olg.open_all()
