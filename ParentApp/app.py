import os
from datetime import datetime
import urllib.request
from tkinter import *
from tkinter import messagebox, font
from PIL import ImageTk, Image
from Database import db

APP_CONFIG_FOLDER_ID = '1TmOJkBPEIOJ__Brm35-SkUgPAmLHSija'
APP_DATA_FOLDER_ID = '1ZFtEonuzNd6qWbAQ2C7yMvLXwpvTd9H6'
CONFIG_FILE_ID = '1LoOWQtbZIIMlBOURkfJdH1mPwJURtn5Y'
FLAG_FILE_ID = '1iKmekqjUXNrWclopiqBFjyT48lsSH8QU'
PASSWORD_FILE_ID = '1j2XRACvcBA-nP1IhshdLomKfiLD4TbHz'

class App():
    def __init__(self, root):
        root.geometry("600x300")
        root.title('Parent Control Application')
        root.resizable(0,0)

        self.titleFont = font.Font(family='Arial', size=25, weight='bold')
        self.normalFont = font.Font(family='Arial', size=14, weight='normal')

        title = Label(root, text="Phần mềm giám sát trẻ em", font=self.titleFont, pady=30)
        title.pack()

        buttonGroup = Frame(root)
        buttonGroup.pack()

        button1 = Button(buttonGroup, text="Sửa file config", padx=5, pady=5, font=self.normalFont, command=self.changeConfigWindow)
        blank = Label(buttonGroup, text="     ", padx=20)
        button2 = Button(buttonGroup, text="Xem lịch sử hoạt động", padx=5, pady=5, font=self.normalFont, command=self.historyActivityWindow)

        button1.grid(row=0, column=0)
        blank.grid(row=0, column=1)
        button2.grid(row=0, column=2)
        
    def changeConfigWindow(self):
        if db.getFileContent(FLAG_FILE_ID) == "1":
            # Toggle flag
            db.setFileContent(FLAG_FILE_ID, "0")

            # Set up new popup window
            newWindow = Toplevel()
            newWindow.geometry("600x300")
            newWindow.title('Sửa file config')
            newWindow.resizable(0,0)

            # Load config file content
            content = db.getFileContent(CONFIG_FILE_ID)

            # Set up textarea
            container = LabelFrame(newWindow, text="config.txt", pady=5, font=self.normalFont)
            container.pack()

            scrollbar = Scrollbar(container)
            scrollbar.pack(side=RIGHT, fill=Y)

            self.textarea = Text(container, height=10, width=50, borderwidth=3, font=('Consolas', 12),  yscrollcommand=scrollbar.set)
            self.textarea.pack(side=LEFT, fill=BOTH)
            scrollbar.config(command=self.textarea.yview)

            self.insertTextIntoTextarea(content)

            # Set up button
            footer = Frame(newWindow, pady=10)
            footer.pack()

            button1 = Button(footer, text="Sửa", padx=5, pady=5, font=self.normalFont, command=lambda: self.changeConfigFile(newWindow))
            blank = Label(footer, text="     ", padx=10)
            button2 = Button(footer, text="Hoàn tác", padx=5, pady=5, font=self.normalFont, command=lambda: self.insertTextIntoTextarea(content))

            button1.grid(row=0, column=0)
            blank.grid(row=0, column=1)
            button2.grid(row=0, column=2)

            newWindow.protocol("WM_DELETE_WINDOW",lambda: self.onCloseChangeConfigWindow(newWindow))

        else:
            # self.stopProgessBar()
            messagebox.showerror("Thông báo", "Đang có người chỉnh sửa file này.\n Xin quay lại sau ít phút nữa.")


    def insertTextIntoTextarea(self, content):
        self.textarea.delete("1.0", END)
        self.textarea.insert(INSERT, content)


    def changeConfigFile(self, newWindow):
        content = self.textarea.get("1.0", 'end-1c')
        db.setFileContent(CONFIG_FILE_ID, content)
        db.setFileContent(FLAG_FILE_ID, "1")
        messagebox.showinfo("Thông báo", "Sửa file thành công")
        newWindow.destroy()


    def onCloseChangeConfigWindow(self, newWindow):
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát?"):
            db.setFileContent(FLAG_FILE_ID, "1")
            newWindow.destroy()


    def historyActivityWindow(self):
        newWindow = Toplevel()
        newWindow.geometry("600x300")
        newWindow.title('Xem lịch sử hoạt động')
        newWindow.resizable(0,0)

        title = Label(newWindow, text="Xem lịch sử theo ngày", font=('Arial', 14), pady=10)
        title.pack()

        mainFrame = Frame(newWindow, pady=10, padx=20)
        mainFrame.pack()

        listFolder = db.getListFoldersInFolder(APP_DATA_FOLDER_ID)

        for i in range(len(listFolder)):
            listFolder[i]['name'] = datetime.strptime(listFolder[i]['name'], '%Y-%m-%d')
        listFolder = sorted(listFolder, key=lambda i: i['name'], reverse=True)
        for i in range(len(listFolder)):
            listFolder[i]['name'] = listFolder[i]['name'].strftime('%d-%m-%Y')
        
        i = 0
        for folder in listFolder:
            button = Button(mainFrame, text=folder['name'], padx=5, pady=5, command=lambda folder=folder: self.viewImages(folder))
            button.grid(row=i, column=0)
            i += 1
        
        newWindow.mainloop()


    def viewImages(self, folder):
        newWindow = Toplevel()
        newWindow.title(folder['name'])

        data = db.getListFilesInFolder(folder['id'])
        numImages = len(data)
        if numImages == 0:
            messagebox.showerror("Thông báo", "Không có hình để hiển thị")
            newWindow.destroy()
            return

        # Download images into temp folder
        for i in range(len(data)):
            fullPath = os.path.join('./temp', 'image' + str(i+1) + '.jpg')
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

        imageView = Label(newWindow, image=imagesList[0])
        imageView.pack(fill='both', expand=True)

        def forward(image_number):
            
            imageView.configure(image=imagesList[image_number])
            
            button_forward.configure(command=lambda: forward(image_number+1), state=ACTIVE)
            button_back.configure(command=lambda: back(image_number-1), state=ACTIVE)
            
            if image_number == numImages - 1:
                button_forward.configure(state=DISABLED)


        def back(image_number):

            imageView.configure(image=imagesList[image_number])
            
            button_forward.configure(command=lambda: forward(image_number+1), state=ACTIVE)
            button_back.configure(command=lambda: back(image_number-1), state=ACTIVE)
            
            if image_number == 0:
                button_back.configure(state=DISABLED)


        footer = Frame(newWindow)
        footer.pack()

        button_back = Button(footer, text="<<", font=(14), state=DISABLED)
        button_forward = Button(footer, text=">>", font=(14), state=ACTIVE, command=lambda: forward(1))

        if numImages == 1:
            button_forward.configure(state=DISABLED)

        button_back.grid(row=0, column=0)
        button_forward.grid(row=0, column=1)

        newWindow.mainloop()


    # def _runProgressBar(self):
    #     self.progressBarWindow = Toplevel()
    #     self.progressBarWindow.geometry("300x50")
    #     self.progressBarWindow.title('Load')
    #     self.progressBarWindow.resizable(0,0)

    #     self.progressBar = ttk.Progressbar(self.progressBarWindow, orient="horizontal", length=286, mode="determinate", maximum=100)
    #     self.progressBar.pack()
        
    #     for i in range(101):
    #         sleep(0.0165)
    #         self.progressBar['value'] = i
    #         self.progressBar.update()
        
    #     self.progressBarWindow.destroy()


    # def runProgressBar(self):
    #     try:
    #         self._runProgressBar()
    #     except _tkinter.TclError:
    #         pass


    # def stopProgessBar(self):
    #     self.progressBar.destroy()
    #     self.progressBarWindow.destroy()
            

def main():
    root = Tk()
    App(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()