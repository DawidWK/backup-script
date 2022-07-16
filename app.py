from backup import make_backup
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    FOLDER_ID = os.getenv('FOLDER_ID')
    FILE_PATH = os.getenv('FILE_PATH')

    make_backup(FOLDER_ID, FILE_PATH)
