import os
import asyncio
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folders_to_upload_dir = '/home/c3po/Desktop/Photos' # Don't forget to set it to MRizer Output as we're pulling it from there
my_folder_id = '1ixdDaRNmi3Yf0zqm1fDsaY9Ka8KN5KeJ'
folder_360_id = '1CCUBuc8z0AENcWFUc0nCnDzTFex5swOd'

async def upload_file(file_path, folder):
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

async def upload_to_drive(id, folder_name):
    tasks = []
##    # Use query to search for folders with matching title
##    query = f"'title': '{folder_name}' and trashed=false" 
##    file_list = drive.ListFile({'q': query}).GetList()
##
##    # Check if any folders were found
##    if len(file_list) > 0:
##        print(f'Folder "{folder_name}" already exists on your Drive.')
##        
##    else:   # Folder not found, proceed with folder creation
##        # Create a new File object representing the folder
    # Folder creation with mimeType for clarity
    folder_meta = {'parents': [{'id': id}], 'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_meta)
    folder.Upload()

    directory = os.path.join(folders_to_upload_dir, folder_name) # path
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        tasks.append(asyncio.create_task(upload_file(file_path, folder)))
    await asyncio.gather(*tasks)
                    
def execute():
    """Go to the output directory and upload folders to drive"""
    for folder_name in os.listdir(folders_to_upload_dir):
        if 'Bank' in folder_name or 'Pvt' in folder_name:
            asyncio.run(upload_to_drive(id=folder_360_id, folder_name=folder_name))
        else:
            asyncio.run(upload_to_drive(id=my_folder_id, folder_name=folder_name))


##file1 = drive.CreateFile({'parents': [{'id': my_folder}], 'title': 'hello.txt'})
##file1.SetContentString('Hello World')
##file1.Upload()
if __name__ == '__main__':
    execute()
