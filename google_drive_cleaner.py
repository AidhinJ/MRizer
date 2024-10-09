import os
import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def main():
    # Authenticate with Google Drive using OAuth 2.0
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
##    if gauth.credentials is None:
##        gauth.LocalWebserverAuth()
##    elif gauth.access_token_expired:
##        gauth.Refresh()
##    else:
##        gauth.GetCredentials()

    # Get a list of all files in the root folder, sorted by modified time
    file_list = drive.ListFile({'q': "'sharedWithMe' in parents and trashed=false"}).GetList()
    print(file_list[:1])
    file_list.sort(key=lambda file: file['modifiedTime'])

    # Calculate the cutoff date for files to be deleted
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=30)

    # Delete files older than the cutoff date
    for file in file_list:
        file_modified_time = datetime.datetime.strptime(file['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if file_modified_time < cutoff_date:
##            file.Delete()
            print(f"Deleted file: {file['title']}")

if __name__ == '__main__':
    main()
