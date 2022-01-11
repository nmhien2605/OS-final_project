from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from datetime import date, datetime
import urllib.request
from PIL import ImageTk,Image

appConfigFolderID = '1TmOJkBPEIOJ__Brm35-SkUgPAmLHSija'
appDataFolderID = '1ZFtEonuzNd6qWbAQ2C7yMvLXwpvTd9H6'
configFileID = '1LoOWQtbZIIMlBOURkfJdH1mPwJURtn5Y'
passwordFileID = '1j2XRACvcBA-nP1IhshdLomKfiLD4TbHz'
flagFileID = '1iKmekqjUXNrWclopiqBFjyT48lsSH8QU'

class DataDrive:
    def __init__(self):
        self.appConfigFolderID = appConfigFolderID
        self.appDataFolderID = appDataFolderID
        self.configFileID = configFileID
        self.passwordFileID = passwordFileID
        self.flagFileID = flagFileID

        gauth = GoogleAuth('./config/settings.yaml')
        self.drive = GoogleDrive(gauth)


    def getFileContent(self, fileName):
        if fileName == "config":
            fileMetadata = { 'id': self.configFileID }
        elif fileName == "password":
            fileMetadata = { 'id': self.passwordFileID }
        elif fileName == "flag":
            fileMetadata = { 'id': self.flagFileID }

        file = self.drive.CreateFile(fileMetadata)
        content = file.GetContentString()
        return content


Database = DataDrive()
