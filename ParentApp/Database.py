import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from datetime import datetime
import urllib.request
from PIL import Image

appConfigFolderID = '1TmOJkBPEIOJ__Brm35-SkUgPAmLHSija'
appDataFolderID = '1ZFtEonuzNd6qWbAQ2C7yMvLXwpvTd9H6'
configFileID = '1LoOWQtbZIIMlBOURkfJdH1mPwJURtn5Y'
flagFileID = '1iKmekqjUXNrWclopiqBFjyT48lsSH8QU'
passwordFileID = '1j2XRACvcBA-nP1IhshdLomKfiLD4TbHz'

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
                'url': "https://drive.google.com/uc?export=view&id=" + image['id']
            })
        for i in range(len(res)):
            fullPath = os.path.join(os.path.dirname(__file__), 'temp', 'image' + str(i+1) + '.jpg')
            urllib.request.urlretrieve(res[i]['url'], fullPath)
            baseheight = 500
            img = Image.open(fullPath)
            wpercent = (baseheight/float(img.size[1]))
            wsize = int((float(img.size[0])*float(wpercent)))
            img = img.resize((wsize, baseheight), Image.ANTIALIAS)
            img.save(fullPath)
        return res
    

db = Database()