import os
import io
import mimetypes
from Google import Create_Service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload

CLIENT_SECRET_FILE = './config/secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

APP_CONFIG_FOLDER_ID = '1TmOJkBPEIOJ__Brm35-SkUgPAmLHSija'
APP_DATA_FOLDER_ID = '1ZFtEonuzNd6qWbAQ2C7yMvLXwpvTd9H6'
CONFIG_FILE_ID = '1LoOWQtbZIIMlBOURkfJdH1mPwJURtn5Y'
FLAG_CONFIG_FILE_ID = '1Vk1wUgYdLCALaTD7TZOGV67WFwpfgBNT'
PASSWORD_FILE_ID = '1j2XRACvcBA-nP1IhshdLomKfiLD4TbHz'
FLAG_PASSWORD_FILE_ID = '1vI0UGh4dDePGYz0v1Z8L826tznW4hIeq'

class Database:
    def __init__(self):
        self.service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Tạo thư mục trong thư mục cha hoặc không, trả ra id thư mục vừa tạo
    def createFolder(self, folderName, parentFolderID=None):
        file_metadata = {
            'name': folderName,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parentFolderID is not None:
            file_metadata['parents'] = [parentFolderID]
        folder = self.service.files().create(body=file_metadata).execute()
        return folder['id']

    # Tạo file và tải lên thư mục cha hoặc không, trả ra id file vừa tạo
    # tên file bao gồm cả phần đuôi extension
    def uploadFile(self, fileName, filePath, folderID=None):
        file_metadata = {
            'name': fileName,
        }
        if folderID is not None:
            file_metadata['parents'] = [folderID]
        fileType = mimetypes.guess_type(fileName)
        media = MediaFileUpload(filePath, mimetype=fileType[0])

        fileID = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return fileID

    # Tải về một file trên drive dựa vào id
    def getFile(self, fileID, fileName, folderPath=None):
        request = self.service.files().get_media(fileId=fileID)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)

        done = False

        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)

        if folderPath is not None:
            full_path = os.path.join(folderPath, fileName)
        else:
            full_path = fileName
        
        with open(full_path, 'wb') as f:
            f.write(fh.read())
            f.close()

    # Tải xuống nội dung file TEXT có sẵn trên cloud 
    def getFileContent(self, fileID):
        request = self.service.files().get_media(fileId=fileID)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)

        done = False

        while not done:
            status, done = downloader.next_chunk()

        content = fh.getvalue()

        return content.decode('utf-8')
        
    # Thay đổi nội dung file TEXT có sẵn trên cloud
    def setFileContent(self, fileID, fileContent):

        file_content = MediaIoBaseUpload(io.BytesIO(fileContent.encode('utf-8')), mimetype='text/plain')

        self.service.files().update(
            fileId=fileID,
            media_body=file_content,
        ).execute()


    def getListFilesInFolder(self, folderID):
        query = f"parents = '{ folderID }' and trashed=false"
        response = self.service.files().list(q=query).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = self.files().list(q=query, pageToken=nextPageToken).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')

        res = [file for file in files if file['mimeType'] != 'application/vnd.google-apps.folder']

        return res

    def getListFoldersInFolder(self, folderID):
        query = f"parents = '{ folderID }' and trashed=false"
        response = self.service.files().list(q=query).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = self.files().list(q=query, pageToken=nextPageToken).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')

        res = [file for file in files if file['mimeType'] == 'application/vnd.google-apps.folder']

        return res

Database = Database()