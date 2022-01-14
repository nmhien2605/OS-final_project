import os
from threading import Thread
import time
from datetime import datetime
import tkinter
import pyautogui
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import font
from data import Database as db

TIME_RELOGIN = 3600
TIME_SHUTDOWN =  15
TIME_SCREENSHOT = 60
TIME_UPDATE = 60
START_TIME = 0
DURATION_TIME = 0
INTERRUPT_TIME = 0
BREAK_TIME = 0
LOGIN_CHECK = -1
STUDING = False
WAIT = True
PARENT = False

APP_CONFIG_FOLDER_ID = '1TmOJkBPEIOJ__Brm35-SkUgPAmLHSija'
APP_DATA_FOLDER_ID = '1ZFtEonuzNd6qWbAQ2C7yMvLXwpvTd9H6'
CONFIG_FILE_ID = '1LoOWQtbZIIMlBOURkfJdH1mPwJURtn5Y'
FLAG_CONFIG_FILE_ID = '1Vk1wUgYdLCALaTD7TZOGV67WFwpfgBNT'
PASSWORD_FILE_ID = '1j2XRACvcBA-nP1IhshdLomKfiLD4TbHz'
FLAG_PASSWORD_FILE_ID = '1vI0UGh4dDePGYz0v1Z8L826tznW4hIeq'


def get_time_now():
    date = datetime.now()
    return date.hour * 60 + date.minute


def check_login(password):
    data = db.getFileContent(PASSWORD_FILE_ID)
    passList = data.splitlines()
    if password == passList[0]:
        return 0
    elif password == passList[1]:
        return 1
    return 2


def shutdown():
    print("shutdown")
    os.system("shutdown /s /t 1")


def wait_shutdown():
    print("waiting to shutdown...")
    time.sleep(TIME_SHUTDOWN)
    print(PARENT, "")
    if not(PARENT):
        shutdown()


def convert_schedule(data):
    lines = data.splitlines()
    list = []
    for line in lines:
        list.append(line.split(' '))
    schedule = []
    for i in range(len(list)):
        schedule.append([])
        for j in range(2):
            time = datetime.strptime(list[i][j].replace(list[i][j][0], ''), '%H:%M')
            schedule[i].append(time.hour * 60 + time.minute)
        for j in range(2, len(list[i])):
            schedule[i].append(int(list[i][j].replace(list[i][j][0], '')))
    return schedule


def get_schedule():
    data = db.getFileContent(CONFIG_FILE_ID)
    schedule = convert_schedule(data)
    return schedule


def check_study(item, time):
    global STUDING, DURATION_TIME, INTERRUPT_TIME, BREAK_TIME
    
    if len(item) > 3:
        BREAK_TIME = item[3]
        if STUDING:
            duration = time - DURATION_TIME
            if len(item) > 4:
                tmp = (time - START_TIME) // (item[2] + item[3])
                sum = item[2] * tmp + (duration)
                if sum >= item[4]:
                    return False
                elif item[4] - sum < 2:
                    msg.showinfo('Notification', '1 minute left until stop study!')
                    return True

            if duration >= item[2]:
                STUDING = False
                INTERRUPT_TIME = time
            elif item[2] - duration < 2:
                msg.showinfo('Notification', '1 minute left until break time!')

        else:
            interrupt = time - INTERRUPT_TIME
            if interrupt >= item[3]:
                STUDING = True
                DURATION_TIME = time
            elif item[3] - interrupt < 2:
                msg.showinfo('Notification', '1 minute left until study time!')

    elif len(item) == 3:
        sum = time - START_TIME
        if sum >= item[2]:
            return False
        elif item[2] - sum < 2:
            msg.showinfo('Notification', '1 minute left until stop study!')

    return True


def check_schedule():
    schedule = get_schedule()
    time = get_time_now()
    for item in schedule:
        if item[0] <= time and time < item[1]:
            if WAIT == True:
                check = check_study(item, time)
                if not(check):
                    return False
            if item[1] - time < 2:
                msg.showinfo('Notification', '1 minute left until stop study and shutdown!')
            return True
    return False


def get_folder(folderName):
    list = db.getListFoldersInFolder(APP_DATA_FOLDER_ID)
    for folder in list:
        if folderName == folder['name']:
            return folder['id']
    return db.createFolder(folderName, APP_DATA_FOLDER_ID)


def record(): # take screenshot or record keyboard action
    print("record")
    while True:
        srceenshot = pyautogui.screenshot()
        date = datetime.now()
        dateString = date.strftime("%Y-%m-%d-%H-%M-%S")
        folderName = date.strftime("%Y-%m-%d")
        fileName = dateString + str('.png')
        srceenshot.save('screenshot\\' + fileName)
        db.uploadFile(fileName, './screenshot/' + fileName, get_folder(folderName))
        time.sleep(TIME_SCREENSHOT)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Children Control Application")
        self.attributes("-fullscreen", True)
        self.title_font = font.Font(family='Helvetica', size=36, weight="bold", slant="italic")
        
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
    
    def show_frame(self, page_name):

        frame = self.frames[page_name]
        frame.tkraise()

    def login(self, password):
        checkLogin = check_login(password)
        checkSchedule = check_schedule()

        global PARENT, CHILDREN, WAIT, LOGIN_CHECK

        if checkLogin == 0:
            PARENT = True
            WAIT = True
            LOGIN_CHECK = -1
            self.destroy()
        else:
            PARENT = False
            if checkSchedule:
                if checkLogin == 1:
                    thr = Thread(target=record, daemon=True)
                    thr.start()
                    WAIT = True
                    LOGIN_CHECK = -1
                    self.destroy()
                else:
                    if LOGIN_CHECK == -1:
                        LOGIN_CHECK = 2
                    elif LOGIN_CHECK == 0:
                        thr = Thread(target=wait_shutdown, daemon=True)
                        thr.start()
                        thr.join()
                    else:
                        LOGIN_CHECK -= 1
            else:
                thr = Thread(target=wait_shutdown, daemon=True)
                thr.start()
                LOGIN_CHECK = -1


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter password", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        lblPass = tk.Label(self, text="Password", font=('Arial', 14))
        entryPass = tk.Entry(self, font=('Arial', 14))
        btnEnter = tk.Button(self, text="Enter", font=('Arial', 14), command=lambda: controller.login(entryPass.get()))

        lblPass.pack(pady=3)
        entryPass.pack(pady=3)
        btnEnter.pack(pady=3)


def window_break(time):
    win = tkinter.Tk()
    win.attributes("-fullscreen", True)

    tk.Label(win, text= "This is break time!", font=('Helvetica 36 bold')).pack(pady=20)

    win.after(time, lambda:win.destroy())
    win.mainloop()


def study():
    global START_TIME, DURATION_TIME, STUDING, BREAK_TIME
    START_TIME = get_time_now()
    DURATION_TIME = START_TIME
    STUDING = True
    duration = True
    study = True

    while study:
        time.sleep(TIME_UPDATE)
        if check_schedule():
            if not(STUDING):
                if duration:
                    duration = False
                    breakTime = BREAK_TIME * 60000
                    Thr = Thread(target=window_break, args=(breakTime,), daemon=True)
                    Thr.start()
            else:
                duration = True
            print('check')
        else:
            study = False
            shutdown()


if __name__ == "__main__":

    while WAIT:
        WAIT = False
        root = App()
        root.attributes('-topmost', True)
        root.update()
        root.attributes('-topmost', False)
        root.mainloop()

        if PARENT:
            if not(WAIT):
                break
            else:
                time.sleep(TIME_RELOGIN)
        else:
            if not(WAIT):
                break
            else:
                study()
    
    print("exit")
