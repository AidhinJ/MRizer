from datetime import datetime as dt
import os
import json
import shutil
import settings2
import logging
import extras
import MR_Cards


    
# Configure logging (optional, but recommended for clean formatting)
logging.basicConfig(filename="mr.log", level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a logger for this module
logger = logging.getLogger(__name__)

class PhotoSorter:        
    def get_app_data(self):
        """Pack all the info from the appointment stack, MR, start_time, end_time"""
        mr_date_time = []
        app_stack = list(MR_Cards.apps_dict.values())
        for index, app in enumerate(app_stack):
            try:
                next_app = app_stack[index+1]
                end_time = dt.fromisoformat(next_app.date_time_var.get())
            except IndexError:
                end_time = MR_Cards.end_time
            mr_date_time.append([
                app.MRnumber.get(),
                app._360_name.get(),
                dt.fromisoformat(app.date_time_var.get()),
                end_time
                ])
        return mr_date_time

    def print_notes(self):
        logger.info("Printing notes")
        app_stack = list(MR_Cards.apps_dict.values())
        for app in app_stack:
            MRnumber = app.MRnumber.get()
            text = app.note.get('1.0', 'end').strip()
            if text != '':
                directory = f'{self.output}/Photos/{MRnumber}/'
                if not os.path.exists(directory):
                    logger.info(f"{directory} doesn't exist. Creating it.")
                    os.makedirs(directory)
                with open(f'{directory}/Note.txt', 'w') as file:
                    file.write(app.note.get('1.0', 'end'))
                    logger.info(directory)
            

    def file_iter(self, device_args=None, is_360=False, resize=lambda file: 0):
        self.file_list = os.listdir()
        for file in self.file_list:
            dir_output = self.organize(file, is_360=is_360)
            try:
                # While we have the directory, lets resize if possible
                # And check for faces. So we can move them.
                resize(dir_output)
                self.face_photo_move(dir_output)
                
            except Exception as e:
                logger.error(e)
            
    def organize(self, file, method='Copy', is_360=False):
        # Get each file creation time (Note getctime doesn't quite work on my os)
        creation_time = os.path.getmtime(file)
        creation_time_dt = dt.fromtimestamp(creation_time)
        logger.info(f'file: {file}, creation_time: {creation_time_dt}')

        # Compare
        for MRnumber, _360, start_time, end_time in self.appointment_data:
            if creation_time_dt >= start_time and creation_time_dt < end_time:
                if is_360:
                    directory = f'{self.output}/Photos/{_360}/'
                    logger.info(f'{file} belongs to {_360}.\n    start_time: {start_time}, end_time: {end_time}')
                else:
                    directory = f'{self.output}/Photos/{MRnumber}/'
                    logger.info(f'{file} belongs to {MRnumber}.\n    start_time: {start_time}, end_time: {end_time}')
                if not os.path.exists(directory):
                    logger.info(f"{directory} doesn't exist. Creating it.")
                    os.makedirs(directory)
                shutil.copy(f'{file}', directory)
                return f'{directory}{file}'

    def device_iter(self):
        orig_dir = os.getcwd()
        for device in settings2.get_data()['devices']:
            try:
                os.chdir(device['dir'])
            except Exception as e:
                logger.exception(e)
                continue
            if device['resizable']:
                resize = extras.image_resize
            else:
                resize = lambda file: None
            self.file_iter(is_360=device['is_360'], resize=resize)
            os.chdir(orig_dir) # Once finished, revert to the default dir
        

    def tasks(self):
        # Get appointment data
        self.appointment_data = self.get_app_data()
        if self.appointment_data == []:
            raise ValueError("No appointments", "No appointment data to MR-ize.")
        
        # Getting current output before beginning mrizing
        self.output = settings2.get_data()['output']
        
        
        print(self.appointment_data)
        self.start_mrizing_time = dt.now() # For logging purposes.
        logger.info(f"MRrizing.............................................")

##        self.device_iter()
##        self.print_notes()
##        tasks = task_manager.get('1.0', 'end').split()
        tasks = ['device_iter', 'print_notes'] # override for test purposes
        for task in tasks:
            getattr(self, task)()
        # self.resize_photos
        # post_file_move

        self.store_mr_numbers()
        
        logger.info(f"MRrizing Complete. Time: {dt.now() - self.start_mrizing_time}")
        os.system(f'notify-send "MRizer" "MRrizing Complete. Time: {dt.now() - self.start_mrizing_time}"')

    def face_photo_move(self, dir):
        # This method is primarily meant for 360 photos that have faces.
        # The assuption is if there's a face, i've taken the 360 photo
        # as a normal photo and need to extract the desired view.
        # Hence seperate it from other photos. Note: Doesn't always work
        _output = f'{os.path.dirname(dir)}/Detected faces'
        try:
            _faces = extras.detect_faces(dir)
        except Exception as e:
            print(e, dir)
            
        if len(_faces) != 0:
            if not os.path.exists(_output):
                    os.makedirs(_output)
            try:
                shutil.move(dir, _output)
            except Exception as e:
                logger.error(e)
                print(e, dir)

    def store_mr_numbers(self):
        # Stores MR numbers. (Granted there's data)
        data = ""
        for appointment in self.appointment_data:
            data = settings2.get_data()
            mr = appointment[0]
            data['storedMRnumbers'].append(mr)
        if data:
            with open('data.json', 'w') as file:        
                json.dump(data, file)
        



if __name__ == "__main__":
    import tkinter as tk
    
    photosorter = PhotoSorter()
    mr_cards = MR_Cards.MR_Cards(height=100, width=100, bg='Navy')
    mr_cards.pack()

    button = tk.Button(text='Run', command=photosorter.tasks)
    button.pack()

    task_manager = tk.Text(width=20, height=10)
    task_manager.pack()
    
