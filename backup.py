import os
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def authenticate_google():
    """Handles Google oAuth and returns google drive object 
    """
    gauth = GoogleAuth()  
    gauth.LocalWebserverAuth()       
    drive = GoogleDrive(gauth)
    return drive


def get_current_datetime():
    """Returns current date time in YYYY-MM-DD-hh-mm-ss format 
    """
    now = str(datetime.datetime.now())[:19]
    now = now.replace(":", "-")
    now = now.replace(" ", "-")
    return str(now)


def google_list_drive_files(drive, folder_id):
    """Retruns list of files in google drive folder

    :param drive: GoogleDrive instance.
    :type drive: pydrive.drive.GoogleDrive

    :param folder_id: Parent folder id (from google drive url).
    :type folder_id: string
    """
    files = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    return files


def google_upload_file(drive, folder_id, file):
    """Uploads file to google drive

    :param drive: GoogleDrive instance.
    :type drive: pydrive.drive.GoogleDrive

    :param folder_id: Parent folder id (from google drive url).
    :type folder_id: string
    
    :param file: file path
    :type file: string

    :returns: gfile instance 
    """
    gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
    gfile.SetContentFile(file)
    gfile.Upload()
    return gfile


def google_update_file_title(gfile, new_title):
    """Updates file title in google drive

    :param gfile: GoogleDriveFile instance.
    :type gfile: pydrive.drive.GoogleDrive.GoogleDriveFile

    :param new_title: file path
    :type new_title: string
    """    
    gfile.update({"title": new_title})
    gfile.Upload()


def google_delete_redundant_files(files, number_of_files_avaliable):
    """If there is more than number_of_files_avaliable in files list,
    removes the oldest one 

    :param files: List with GoogleDriveFile instances.
    :type files: List

    :param number_of_files_avaliable: number of files avaliable in folder
    :type number_of_files_avaliable: int
    """    
    if len(files) < number_of_files_avaliable:
        return
 
    oldest_file = (files[0].metadata.get("createdDate"), files[0])
    for file in files:
        if file.metadata.get("createdDate") <= oldest_file[0]:
            oldest_file = (file.metadata.get("createdDate"), file)

    oldest_file[1].Trash()


def make_backup(google_drive_folder_id, file_path, file_name=None, auto_date=True, number_of_files_avaliable=6):
    """Creates backup file in google drive folder with current timestamp.
    Removes oldest file if there is more than number_of_files_avaliable in folder.

    :param google_drive_folder_id: Google Drive folder id.
    :type google_drive_folder_id: string

    :param file_path: Path to file.
    :type file_path: string

    :param file_name: Sets different file name 
    :type file_name: string
    :default file_name: None | same file as from path

    :param auto_date: List with GoogleDriveFile instances.
    :type auto_date: boolean
    :default auto_date: True

    :param number_of_files_avaliable: number of files avaliable in folder
    :type number_of_files_avaliable: int
    :default number_of_files_avaliable: 6 
    """    
    if file_name == None:
        file_name = os.path.split(file_path)[1] # sets same file name from path

    if auto_date:
        now = get_current_datetime()
        file_name = f"-{now}.".join(file_name.rsplit(".", 1)) # adds date before extension

    drive = authenticate_google()
    
    all_files = google_list_drive_files(drive, google_drive_folder_id)
    google_delete_redundant_files(all_files, number_of_files_avaliable)

    gfile = google_upload_file(drive, google_drive_folder_id, file_path)
    google_update_file_title(gfile, file_name)

