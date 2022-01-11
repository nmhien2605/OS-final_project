import os
from datetime import datetime
import urllib.request

from tkinter import *
from tkinter import messagebox
from tkscrolledframe import ScrolledFrame
from PIL import ImageTk, Image
from Database import db

APP_CONFIG_FOLDER_ID = '1TmOJkBPEIOJ__Brm35-SkUgPAmLHSija'
APP_DATA_FOLDER_ID = '1ZFtEonuzNd6qWbAQ2C7yMvLXwpvTd9H6'
CONFIG_FILE_ID = '1LoOWQtbZIIMlBOURkfJdH1mPwJURtn5Y'
FLAG_CONFIG_FILE_ID = '1Vk1wUgYdLCALaTD7TZOGV67WFwpfgBNT'
PASSWORD_FILE_ID = '1j2XRACvcBA-nP1IhshdLomKfiLD4TbHz'
FLAG_PASSWORD_FILE_ID = '1vI0UGh4dDePGYz0v1Z8L826tznW4hIeq'

class App():
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x350")
        self.root.resizable(0,0)

        self.mainWindow()

        self.root.protocol("WM_DELETE_WINDOW", self.onCloseWindow)

    
    def mainWindow(self):
        self.root.title('Parent Control Application')

        self.title = Label(self.root, text="Phần mềm giám sát trẻ em", font=('Arial', 25, 'bold'), pady=30)
        self.title.pack()

        self.buttonGroup = Frame(self.root)
        self.buttonGroup.pack()

        button1 = Button(self.buttonGroup, text="Quản lý thời gian", padx=5, pady=5, font=('Arial', 14), command=self.changeConfigWindow)
        button2 = Button(self.buttonGroup, text="Quản lý mật khẩu", padx=5, pady=5, font=('Arial', 14), command=self.changePasswordWindow)
        button3 = Button(self.buttonGroup, text="Xem lịch sử hoạt động", padx=5, pady=5, font=('Arial', 14), command=self.historyActivityWindow)

        button1.grid(row=0, column=0)
        button2.grid(row=1, column=0, pady=20)
        button3.grid(row=2, column=0)
        

    def changeConfigWindow(self):
        if db.getFileContent(FLAG_CONFIG_FILE_ID) == "1":
            # Toggle flag
            db.setFileContent(FLAG_CONFIG_FILE_ID, "0")

            # Set up new window
            self.root.title('Quản lý thời gian')
            self.title.destroy()
            self.buttonGroup.destroy()

            # Load config file content
            content = db.getFileContent(CONFIG_FILE_ID)

            # Set up textarea
            self.container = LabelFrame(self.root, text="config.txt", pady=5, font=('Arial', 14))
            self.container.pack()

            scrollbar = Scrollbar(self.container)
            scrollbar.pack(side=RIGHT, fill=Y)

            self.textarea = Text(self.container, height=12, width=55, borderwidth=3, font=('Consolas', 12),  yscrollcommand=scrollbar.set)
            self.textarea.pack(side=LEFT, fill=BOTH)
            scrollbar.config(command=self.textarea.yview)

            self.insertTextIntoTextarea(content)

            # Set up button
            self.footer = Frame(self.root, pady=10)
            self.footer.pack()

            btnEdit = Button(self.footer, text="Sửa", padx=5, pady=5, font=('Arial', 14), command=self.changeConfigFile)
            btnUndo = Button(self.footer, text="Hoàn tác", padx=5, pady=5, font=('Arial', 14), command=lambda: self.insertTextIntoTextarea(content))
            btnBack = Button(self.footer, text="Trở lại", padx=5, pady=5, font=('Arial', 14), command=lambda: self.onCloseWindow('config'))
            
            btnEdit.grid(row=0, column=0)
            btnUndo.grid(row=0, column=1, padx=10)
            btnBack.grid(row=0, column=2)

        else:
            # self.stopProgessBar()
            messagebox.showerror("Thông báo", "Đang có người chỉnh sửa file này.\n Xin quay lại sau ít phút nữa.")


    def changeConfigFile(self):
        content = self.textarea.get("1.0", 'end-1c')
        db.setFileContent(CONFIG_FILE_ID, content)
        db.setFileContent(FLAG_CONFIG_FILE_ID, "1")
        messagebox.showinfo("Thông báo", "Sửa file thành công")
        self.container.destroy()
        self.footer.destroy()
        self.mainWindow()


    def changePasswordWindow(self):
        if db.getFileContent(FLAG_PASSWORD_FILE_ID) == "1":
            # Toggle flag
            db.setFileContent(FLAG_PASSWORD_FILE_ID, "0")

            # Set up new window
            self.root.title('Quản lý mật khẩu')
            self.title.destroy()
            self.buttonGroup.destroy()

            # Load config file content
            content = db.getFileContent(PASSWORD_FILE_ID)

            # Set up textarea
            self.container = LabelFrame(self.root, text="password.txt", pady=5, font=('Arial', 14))
            self.container.pack()

            scrollbar = Scrollbar(self.container)
            scrollbar.pack(side=RIGHT, fill=Y)

            self.textarea = Text(self.container, height=12, width=55, borderwidth=3, font=('Consolas', 12),  yscrollcommand=scrollbar.set)
            self.textarea.pack(side=LEFT, fill=BOTH)
            scrollbar.config(command=self.textarea.yview)

            self.insertTextIntoTextarea(content)

            # Set up button
            self.footer = Frame(self.root, pady=10)
            self.footer.pack()

            btnEdit = Button(self.footer, text="Sửa", padx=5, pady=5, font=('Arial', 14), command=self.changePasswordFile)
            btnUndo = Button(self.footer, text="Hoàn tác", padx=5, pady=5, font=('Arial', 14), command=lambda: self.insertTextIntoTextarea(content))
            btnBack = Button(self.footer, text="Trở lại", padx=5, pady=5, font=('Arial', 14), command=lambda: self.onCloseWindow('config'))
            
            btnEdit.grid(row=0, column=0)
            btnUndo.grid(row=0, column=1, padx=10)
            btnBack.grid(row=0, column=2)

        else:
            messagebox.showerror("Thông báo", "Đang có người chỉnh sửa file này.\n Xin quay lại sau ít phút nữa.")


    def changePasswordFile(self):
        content = self.textarea.get("1.0", 'end-1c')
        db.setFileContent(PASSWORD_FILE_ID, content)
        db.setFileContent(FLAG_PASSWORD_FILE_ID, "1")
        messagebox.showinfo("Thông báo", "Sửa file thành công")
        self.container.destroy()
        self.footer.destroy()
        self.mainWindow()


    def insertTextIntoTextarea(self, content):
        self.textarea.delete("1.0", END)
        self.textarea.insert(INSERT, content)


    def historyActivityWindow(self):
        # set up new window
        self.root.title('Xem lịch sử hoạt động')
        self.title.destroy()
        self.buttonGroup.destroy()

        self.sf = ScrolledFrame(self.root)
        self.sf.pack(side="top", expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        self.sf.bind_arrow_keys(self.root)
        self.sf.bind_scroll_wheel(self.root)

        # Create a frame within the ScrolledFrame
        inner_frame = self.sf.display_widget(Frame, fit_width=True)

        title = Label(inner_frame, text="Xem lịch sử theo ngày", font=('Arial', 18), pady=10)
        title.pack()

        frame = Frame(inner_frame, pady=10, padx=20)
        frame.pack()

        listFolder = db.getListFoldersInFolder(APP_DATA_FOLDER_ID)

        for i in range(len(listFolder)):
            listFolder[i]['name'] = datetime.strptime(listFolder[i]['name'], '%Y-%m-%d')
        listFolder = sorted(listFolder, key=lambda i: i['name'], reverse=True)
        for i in range(len(listFolder)):
            listFolder[i]['name'] = listFolder[i]['name'].strftime('%d-%m-%Y')
        
        i = 0
        for folder in listFolder:
            button = Button(frame, text=folder['name'], font=('Arial', 14), padx=5, pady=5, command=lambda folder=folder: self.viewImagesWindow(folder))
            button.grid(row=i, column=0, pady=5)
            i += 1
        
        self.btnBack = Button(inner_frame, text="Trở lại", font=('Arial', 14), padx=5, pady=5, command=lambda: self.onCloseWindow('history'))
        self.btnBack.pack(pady=5)

    def viewImagesWindow(self, folder):
        # set up new window
        self.root.title(folder['name'])
        self.root.geometry("1000x550")
        self.root.resizable(1,1)
        self.sf.destroy()

        data = db.getListFilesInFolder(folder['id'])
        numImages = len(data)
        if numImages == 0:
            messagebox.showerror("Thông báo", "Không có hình để hiển thị")
            return self.onCloseWindow('viewImage')

        # Download images into temp folder
        for i in range(len(data)):
            extension = ''
            if data[i]['mimeType'] == 'image/png':
                extension = '.png'
            elif data[i]['mimeType'] == 'image/jpeg':
                extension = '.jpg'
            fullPath = os.path.join('./temp', 'image' + str(i+1) + extension)
            url = "https://drive.google.com/uc?export=view&id=" + data[i]['id']
            urllib.request.urlretrieve(url, fullPath)
            baseheight = 500
            img = Image.open(fullPath)
            wpercent = (baseheight/float(img.size[1]))
            wsize = int((float(img.size[0])*float(wpercent)))
            img = img.resize((wsize, baseheight), Image.ANTIALIAS)
            img.save(fullPath)

        imagesList = []
        for i in range(numImages):
            imagesList.append(ImageTk.PhotoImage(Image.open('./temp/image' + str(i+1) + '.jpg')))

        self.imageView = Label(self.root, image=imagesList[0])
        self.imageView.pack(fill='both', expand=True)

        def forward(image_number):
            
            self.imageView.configure(image=imagesList[image_number])
            
            button_forward.configure(command=lambda: forward(image_number+1), state=ACTIVE)
            button_back.configure(command=lambda: back(image_number-1), state=ACTIVE)
            
            if image_number == numImages - 1:
                button_forward.configure(state=DISABLED)


        def back(image_number):

            self.imageView.configure(image=imagesList[image_number])
            
            button_forward.configure(command=lambda: forward(image_number+1), state=ACTIVE)
            button_back.configure(command=lambda: back(image_number-1), state=ACTIVE)
            
            if image_number == 0:
                button_back.configure(state=DISABLED)


        self.footer = Frame(self.root)
        self.footer.pack()

        button_back = Button(self.footer, text="<<", font=(14), state=DISABLED)
        btnBack = Button(self.footer, text="Trở lại", font=('Arial', 14), command=lambda: self.onCloseWindow('viewImage'))
        button_forward = Button(self.footer, text=">>", font=(14), state=ACTIVE, command=lambda: forward(1))

        if numImages == 1:
            button_forward.configure(state=DISABLED)

        button_back.grid(row=0, column=0)
        btnBack.grid(row=0, column=1, padx=10)
        button_forward.grid(row=0, column=2)

    def onCloseWindow(self, window_type=None):
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát?"):
            if window_type == 'config':
                self.container.destroy()
                self.footer.destroy()
                db.setFileContent(FLAG_CONFIG_FILE_ID, "1")
                self.mainWindow()
            elif window_type == 'password':
                self.container.destroy()
                self.footer.destroy()
                db.setFileContent(FLAG_PASSWORD_FILE_ID, "1")
                self.mainWindow()
            elif window_type == 'history':
                self.sf.destroy()
                self.mainWindow()
            elif window_type == 'viewImage':
                self.root.geometry("600x350")
                self.root.resizable(0,0)
                self.imageView.destroy()
                self.footer.destroy()
                self.historyActivityWindow()
            elif window_type == None:
                self.root.destroy()
                db.setFileContent(FLAG_CONFIG_FILE_ID, "1")
                db.setFileContent(FLAG_PASSWORD_FILE_ID, "1")
            

def main():
    root = Tk()
    App(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()