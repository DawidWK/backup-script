from backup import make_backup
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    FOLDER_ID = os.getenv('FOLDER_ID')
    FILE_PATH = os.getenv('FILE_PATH')
    # FOLDER_ID = '1RXkq5-CkGNiKLeYmdbc3GHGjgVs7qGFD'
    # FILE_PATH = '/mnt/c/Users/bazzu/Documents/Backup/Passwords.kdbx'

    make_backup(FOLDER_ID, FILE_PATH)
