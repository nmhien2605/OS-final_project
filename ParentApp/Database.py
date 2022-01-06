from os import error
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from datetime import date, datetime

appConfigFolderID = '1TmOJkBPEIOJ__Brm35-SkUgPAmLHSija'
appDataFolderID = '1ZFtEonuzNd6qWbAQ2C7yMvLXwpvTd9H6'
configFileID = '1LoOWQtbZIIMlBOURkfJdH1mPwJURtn5Y'
flagFileID = '1iKmekqjUXNrWclopiqBFjyT48lsSH8QU'

class Database:
    def __init__(self):
        self.appConfigFolderID = appConfigFolderID
        self.appDataFolderID = appDataFolderID
        self.configFileID = configFileID
        self.flagFileID = flagFileID

        gauth = GoogleAuth('./config/settings.yaml')
        self.drive = GoogleDrive(gauth)

    def getFileContent(self, fileName):
        if fileName == "config":
            fileMetadata = { 'id': self.configFileID }
        elif fileName == "flag":
            fileMetadata = { 'id': self.flagFileID }

        file = self.drive.CreateFile(fileMetadata)
        content = file.GetContentString()
        return content

    def changeFileContent(self, fileName, fileContent):
        if fileName == "config":
            fileMetadata = {'id': self.configFileID}
        elif fileName == "flag":
            fileMetadata = { 'id': self.flagFileID }
            
        file = self.drive.CreateFile(fileMetadata)
        file.SetContentString(fileContent)
        file.Upload()

    def getListFolder(self):
        res = []
        listFolder = self.drive.ListFile({'q': "'" + appDataFolderID + "' in parents and trashed=false"}).GetList()
        for folder in listFolder:
            res.append({
                'title': folder['title'], 
                'id': folder['id']
            })
        for i in range(len(res)):
            res[i]['title'] = datetime.strptime(res[i]['title'], '%Y-%m-%d')
        res = sorted(res, key=lambda i: i['title'], reverse=True)
        for i in range(len(res)):
            res[i]['title'] = res[i]['title'].strftime('%d-%m-%Y')
        return res

    def getListImages(self, folderID):
        res = []
        listImages = self.drive.ListFile({'q': "'" + folderID + "' in parents and trashed=false"}).GetList()
        for image in listImages:
            res.append({
                'title': image['title'], 
                'id': image['id'],
                'embedLink': image['embedLink']
            })
        return res
    




db = Database()