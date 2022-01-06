from tkinter import *
from tkinter import ttk, messagebox, font, _tkinter
from threading import Thread
from time import sleep
from PIL import ImageTk,Image
from Database import db

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

        button1 = Button(buttonGroup, text="Sửa file config", padx=5, pady=5, font=self.normalFont, command=self.onClickChangeConfigFileButton)
        blank = Label(buttonGroup, text="     ", padx=20)
        button2 = Button(buttonGroup, text="Xem lịch sử hoạt động", padx=5, pady=5, font=self.normalFont, command=self.historyActivityWindow)

        button1.grid(row=0, column=0)
        blank.grid(row=0, column=1)
        button2.grid(row=0, column=2)


    def onClickChangeConfigFileButton(self):
        thread = Thread(target=self.createChangeConfigWindow)
        thread.start()
        self.runProgressBar()
        

    def createChangeConfigWindow(self):
        if db.getFileContent("flag") == "1":
            # Toggle flag
            db.changeFileContent("flag", "0")

            # Set up new popup window
            newWindow = Toplevel()
            newWindow.geometry("600x300")
            newWindow.title('Sửa file config')
            newWindow.resizable(0,0)

            # Load config file content
            content = db.getFileContent("config")

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
            self.stopProgessBar()
            messagebox.showerror("Thông báo", "Đang có người chỉnh sửa file này.\n Xin quay lại sau ít phút nữa.")


    def insertTextIntoTextarea(self, content):
        self.textarea.delete("1.0", END)
        self.textarea.insert(INSERT, content)


    def changeConfigFile(self, newWindow):
        content = self.textarea.get("1.0", 'end-1c')
        db.changeFileContent("config", content)
        db.changeFileContent("flag", "1")
        messagebox.showinfo("Thông báo", "Sửa file thành công")
        newWindow.destroy()


    def onCloseChangeConfigWindow(self, newWindow):
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát?"):
            db.changeFileContent("flag", "1")
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

        listFolder = db.getListFolder()
        i = 0
        for folder in listFolder:
            button = Button(mainFrame, text=folder['title'], padx=5, pady=5, command=lambda folder=folder: self.viewImages(folder))
            button.grid(row=i, column=0)
            i += 1
        
        newWindow.mainloop()


    def viewImages(self, folder):
        newWindow = Toplevel()
        newWindow.title(folder['title'])

        data = db.getListImages(folder['id'])
        numImages = len(data)
        if numImages == 0:
            messagebox.showerror("Thông báo", "Không có hình để hiển thị")
            newWindow.destroy()
            return

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


    def _runProgressBar(self):
        self.progressBarWindow = Toplevel()
        self.progressBarWindow.geometry("300x50")
        self.progressBarWindow.title('Load')
        self.progressBarWindow.resizable(0,0)

        self.progressBar = ttk.Progressbar(self.progressBarWindow, orient="horizontal", length=286, mode="determinate", maximum=100)
        self.progressBar.pack()
        
        for i in range(101):
            sleep(0.02)
            self.progressBar['value'] = i
            self.progressBar.update()
        
        self.progressBarWindow.destroy()


    def runProgressBar(self):
        try:
            self._runProgressBar()
        except _tkinter.TclError:
            pass


    def stopProgessBar(self):
        self.progressBar.destroy()
        self.progressBarWindow.destroy()
            

def main():
    root = Tk()
    App(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()