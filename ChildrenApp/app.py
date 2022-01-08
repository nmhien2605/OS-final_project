from threading import Thread
import time
import pyautogui
import tkinter as tk
from tkinter.constants import FALSE, TRUE
import tkinter.messagebox as msg
from tkinter import font
from data import Database as db

TIME_RELOGIN = 5
TIME_SHUTDOWN =  5
WAIT = True
PARENT = False


def check_login(password):
    passList = db.getPassword()
    if password == passList[0]:
        return True
    return False


def shutdown():
    print("shutdown\n")
    # do something in here
    #
    #


def wait_shutdown():
    print("waiting to shutdown...\n")
    time.sleep(TIME_SHUTDOWN)
    print(PARENT, "\n")
    if not(PARENT):
        shutdown()


def check_schedule():
    schedule = db.getSchedule()
    return True


def record(): # take screenshot or record keyboard action
    print("record")
    while True:
        srceenshot = pyautogui.screenshot()
        srceenshot.save(r'ChildrenApp\screenshot\test.png')
        time.sleep(10)
        # do something in here


def on_top_window(root):
    while True:
        print("top\n")
        root.lift()
        # root.attributes('-topmost', True)
        # root.update()
        # root.attributes('-topmost', False)
        time.sleep(1)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Children Control Application")
        self.state("zoomed")
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, ipadx=10, ipady=10)
        container.grid_rowconfigure(0, minsize=400, weight=1)
        container.grid_columnconfigure(0, minsize=400, weight=1)

        self.frames = {}
        self.number = 2
        for F in (LoginPage,):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")
    #     self.on_top()

    # def on_top(self):
    #     thr = Thread(target=on_top_window, args=(self), daemon=True)
    #     thr.start()

    # switch to screen page_name
    def show_frame(self, page_name):

        frame = self.frames[page_name]
        frame.tkraise()

    def login(self, password):
        checkLogin = check_login(password)
        checkSchedule = check_schedule()

        global PARENT, CHILDREN, WAIT

        if checkLogin:
            PARENT = True
            WAIT = True
            self.destroy()
        else:
            PARENT = False
            if checkSchedule:
                thr = Thread(target=record, daemon=True)
                thr.start()
                WAIT = False
                self.destroy()
            else:
                thr = Thread(target=wait_shutdown, daemon=True)
                thr.start()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter password", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        lblPass = tk.Label(self, text="Password")
        entryPass = tk.Entry(self)
        btnEnter = tk.Button(self, text="Enter", command=lambda: controller.login(entryPass.get()))
        # btnBack = tk.Button(self, text="Back", command=lambda: controller.show_frame("Search"))
        # btnBackMain = tk.Button(self, text="Back to Main", command=lambda: controller.show_frame("MainPage"))

        lblPass.pack(pady=3)
        entryPass.pack(pady=3)
        btnEnter.pack(pady=3)
        # btnBack.pack(pady=3)
        # btnBackMain.pack(pady=3)


# class MainPage(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="Info", font=controller.title_font)
#         label.pack(side="top", fill="x", pady=10)

        # btnConnect = tk.Button(self, text="Connect to Server", command=lambda: controller.connect_server())

        # btnConnect.pack(pady=3)


def to_top(root):
   root.lift()


def stay_on_top(root):
    while True:
        to_top(root)
        time.sleep(1)
   #root.after(2000, stay_on_top(root))


if __name__ == "__main__":

    # content = db.getFileContent("config")
    # print(content)
    root = App()
    # stay_on_top(root)
    thr = Thread(target=on_top_window, args=(root), daemon=True)
    thr.start()
    
    while WAIT:

        WAIT = False

        root.mainloop()

        if PARENT:
            if not(WAIT):
                break # delete here when release
                WAIT = True
            else:
                time.sleep(TIME_RELOGIN)
        else:
            time.sleep(1)
            # do something
    
    print("exit")