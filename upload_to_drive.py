import os
import threading
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json

with open('data.json') as file:
    data = json.load(file)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folders_to_upload_dir = f'{data["output"]}/Photos' # get the output

threads = []
def upload_file(file_path, folder):
    def task():
        # Define File Metadata for upload
        filename = os.path.basename(file_path)
        file_meta = {
            'title': filename,
            'parents': [{'id': folder['id']}]
            }
        file_to_upload = drive.CreateFile(file_meta)
        
        print('Uploading:', file_path)
        file_to_upload.SetContentFile(file_path)
        file_to_upload.Upload()

    thread = threading.Thread(target=task)
    threads.append(thread)
    thread.start()
    
def upload_to_drive(path, folder_id):
    title = os.path.basename(path)
    # First check if folder exist on drive. If so, create another folder.
    file_list = drive.ListFile({'q': "'{}' in parents and title = '{}'".format(folder_id, title)}).GetList()
    if file_list:
        for num in range(1, 10):
            # Search for existing folder duplicates from 1 - 10
            new_title = f"{title}({num})"
            file_list = drive.ListFile({'q': "'{}' in parents and title = '{}'".format(folder_id, new_title)}).GetList()
            if not file_list:
                break
            if num == 10:
                # If this loop successfully reaches 10, then raise an error
                raise ValueError(f"{title}. There are too many duplicates with that name.")
        title = new_title

    # Create folder
    folder_meta = {'parents': [{'id': folder_id}], 'title': title, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_meta)
    folder.Upload()

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            upload_file(item_path, folder)
        else:  # Assuming it's a directory
            upload_to_drive(folder_id=folder['id'], path=item_path)
            
                    
def execute():
    """Go to the output directory and upload folders to drive"""
    for folder_name in os.listdir(folders_to_upload_dir):
        path = os.path.join(folders_to_upload_dir, folder_name)
        if 'Bank' in folder_name or 'Pvt' in folder_name:
            upload_to_drive(folder_id=data["folder_360_id"], path=path)
        else:
            upload_to_drive(folder_id=data["my_folder_id"], path=path)
    # Wait for all threads to finish
    for thread in threads:
        thread.join()


##file1 = drive.CreateFile({'parents': [{'id': my_folder}], 'title': 'hello.txt'})
##file1.SetContentString('Hello World')
##file1.Upload()
if __name__ == '__main__':
    pass
    execute()
