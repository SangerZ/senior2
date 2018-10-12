#!/usr/bin/env python

import tkinter as tk     
import tkinter.font as tkfont
import tk_tools
import pymysql


class HydroponicApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StatusPage, SettingPage, RecalibratePage, ConnectionPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StatusPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StatusPage(tk.Frame):

    global ecCounter
    global phCounter
    ecCounter = 0.0
    phCounter = 0.0

    def __init__(self, parent, controller):
        global ecCounter, phCounter
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        leftFrame = tk.Frame(self, bg = 'cyan', width = 100, height = 100)
        rightFrame = tk.Frame(self, width = 100, height = 100)
        leftFrame.grid(row = 0, column = 0)
        rightFrame.grid(row = 0, column = 1, padx = 70)

        btn1 = tk.Button(leftFrame, text = "Status",
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn1.grid(row = 0, column = 0, sticky = 'w')

        btn2 = tk.Button(leftFrame, text = "Settings", command=lambda: controller.show_frame("SettingPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn2.grid(row = 1, column = 0, sticky = 'w')

        btn3 = tk.Button(leftFrame, text = "Recalibration", command=lambda: controller.show_frame("RecalibratePage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn3.grid(row = 2, column = 0, sticky = 'w')

        btn4 = tk.Button(leftFrame, text = "Connection", command=lambda: controller.show_frame("ConnectionPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn4.grid(row = 3, column = 0, sticky = 'w')

        ecTitle = tk.Label(rightFrame, text = "EC Value", font = ("Helvetica, 35"))
        ecTitle.grid(row = 0, column = 0)

        phTitle = tk.Label(rightFrame, text = "pH Value", font = ("Helvetica, 35"))
        phTitle.grid(row = 0, column = 1, padx = 100)


        #ecVal = tk.Label(rightFrame, text = ecCounter, pady = 60, font = ("Helvetica, 30"))
        #ecVal.grid(row = 2, column = 0)
        
        #phVal = tk.Label(rightFrame, text = phCounter, pady = 60, font = ("Helvetica, 30"))
        #phVal.grid(row = 2, column = 1)

        ecGauge = tk_tools.Gauge(rightFrame, height=150, max_value=10, label='ec', unit='us/cm', divisions=10)
        ecGauge.grid(row = 2, column = 0)

        phGauge = tk_tools.Gauge(rightFrame, height=150, max_value=14, label='pH', unit=' ', divisions=14, red_low=20, yellow_low=35, yellow=80, red=90)
        phGauge.grid(row = 2, column = 1)

        def getNew():
            global ecCounter, phCounter
            db = pymysql.connect("localhost", "root", "009564", "Status")
            cursor = db.cursor()
            sql= "SELECT ec, ph FROM ecphCurrent WHERE id=1"
            try:
                cursor.execute(sql)
                result = cursor.fetchone()
                ecCounter = result[0]
                phCounter = result[1]
            except:
                ecCounter = 0
                phCounter = 0
            #ecVal.config(text = round(ecCounter,1))
            #phVal.config(text = round(phCounter,1))
            ecGauge.set_value(ecCounter)
            phGauge.set_value(phCounter)
            db.close()
            self.after(1000, getNew)
        getNew()
           

class SettingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        leftFrame = tk.Frame(self, bg = 'cyan', width = 100, height = 100)
        rightFrame = tk.Frame(self, width = 100, height = 100)
        leftFrame.grid(row = 0, column = 0)
        rightFrame.grid(row = 0, column = 1, padx = 50)

        btn1 = tk.Button(leftFrame, text = "Status", command=lambda: controller.show_frame("StatusPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn1.grid(row = 0, column = 0, sticky = 'w')

        btn2 = tk.Button(leftFrame, text = "Settings", 
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn2.grid(row = 1, column = 0, sticky = 'w')

        btn3 = tk.Button(leftFrame, text = "Recalibration", command=lambda: controller.show_frame("RecalibratePage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn3.grid(row = 2, column = 0, sticky = 'w')

        btn4 = tk.Button(leftFrame, text = "Connection", command=lambda: controller.show_frame("ConnectionPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn4.grid(row = 3, column = 0, sticky = 'w')

        volumeLabel = tk.Label(rightFrame, text = "Volume", font = ("Helvetica, 13"))
        ecThresholdLabel = tk.Label(rightFrame, text = "ec Threshold", font = ("Helvetica, 13"))
        phThresholdLabel = tk.Label(rightFrame, text = "ph Threshold", font = ("Helvetica, 13"))
        ecIntensityLabel = tk.Label(rightFrame, text = "ec Intensity", font = ("Helvetica, 13"))
        phIntensityLabel = tk.Label(rightFrame, text = "ph Intensity", font = ("Helvetica, 13"))

        volumeLabel.grid(row = 0, column = 0, sticky = 'w')
        ecThresholdLabel.grid(row = 1, column = 0, sticky = 'w', ipady = 3)
        phThresholdLabel.grid(row = 2, column = 0, sticky = 'w', ipady = 3)
        ecIntensityLabel.grid(row = 3, column = 0, sticky = 'w', ipady = 3)
        phIntensityLabel.grid(row = 4, column = 0, sticky = 'w', ipady = 3)

        volumeEntry = tk.Label(rightFrame, text = 0, font = ("Helvetica, 13"), width = 15, bg = "#FFFFFF")
        ecThresholdEntry = tk.Label(rightFrame, text = 0, font = ("Helvetica, 13"), width = 15, bg = "#FFFFFF")
        phThresholdEntry = tk.Label(rightFrame, text = 0, font = ("Helvetica, 13"), width = 15, bg = "#FFFFFF")
        ecIntensityEntry = tk.Label(rightFrame, text = 0, font = ("Helvetica, 13"), width = 15, bg = "#FFFFFF")
        phIntensityEntry = tk.Label(rightFrame, text = 0, font = ("Helvetica, 13"), width = 15, bg = "#FFFFFF")

        volumeEntry.grid(row = 0, column = 1, padx = 10, pady = 5)
        ecThresholdEntry.grid(row = 1, column = 1, padx = 10, pady = 5)
        phThresholdEntry.grid(row = 2, column = 1, padx = 10, pady = 5)
        ecIntensityEntry.grid(row = 3, column = 1, padx = 10, pady = 5)
        phIntensityEntry.grid(row = 4, column = 1, padx = 10, pady = 5)

        volumeScale = tk.Scale(rightFrame, orient = 'horizontal', from_ = 40, to = 300, width = 20, length = 200)
        ecThresholdScale = tk.Scale(rightFrame, orient = 'horizontal', from_ = 1.0, to = 5.0, resolution = 0.1, width = 20, length = 200)
        phThresholdScale = tk.Scale(rightFrame, orient = 'horizontal', from_ = 3.0, to = 8.0, resolution = 0.1, width = 20, length = 200)
        ecIntensityScale = tk.Scale(rightFrame, orient = 'horizontal', from_ = 0, to = 100, resolution = 0.1, width = 20, length = 200)
        phIntensityScale = tk.Scale(rightFrame, orient = 'horizontal', from_ = 0, to = 100, resolution = 0.1, width = 20, length = 200)

        volumeScale.grid(row = 0, column = 2)
        ecThresholdScale.grid(row = 1, column = 2)
        phThresholdScale.grid(row = 2, column = 2)
        ecIntensityScale.grid(row = 3, column = 2)
        phIntensityScale.grid(row = 4, column = 2)

        def setEntry():
            vol = volumeScale.get()
            ect = ecThresholdScale.get()
            pht = phThresholdScale.get()
            eci = ecIntensityScale.get()
            phi = phIntensityScale.get()

            volumeEntry.config(text = vol)
            ecThresholdEntry.config(text = ect)
            phThresholdEntry.config(text = pht)
            ecIntensityEntry.config(text = eci)
            phIntensityEntry.config(text = phi)
            
            return

        applyBtn = tk.Button(rightFrame, text = "Apply", font = ("Helvetica, 13"), command = setEntry)
        applyBtn.grid(row = 5, column = 2, pady = 20)

class RecalibratePage(tk.Frame):

    global ecCounter1
    global phCounter1
    ecCounter1 = 0
    phCounter1 = 0
    global ecText
    global phText
    phText = ["Start Calibrate pH", "pH 4 Solution", "pH 8 Solution", "Finish"]
    ecText = ["Start Calibrate EC", "EC 1.4 Solution", "EC 12.8 Solution", "Finish"]

    def __init__(self, parent, controller):
        global ecCounter1, phCounter1, ecText, phText
        tk.Frame.__init__(self, parent)
        self.controller = controller

        leftFrame = tk.Frame(self, bg = 'cyan', width = 100, height = 100)
        rightFrame = tk.Frame(self, width = 300, height = 300)
        leftFrame.grid(row = 0, column = 0)
        rightFrame.grid(row = 0, column = 1)

        btn1 = tk.Button(leftFrame, text = "Status", command=lambda: controller.show_frame("StatusPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn1.grid(row = 0, column = 0, sticky = 'w')

        btn2 = tk.Button(leftFrame, text = "Settings", command=lambda: controller.show_frame("SettingPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn2.grid(row = 1, column = 0, sticky = 'w')

        btn3 = tk.Button(leftFrame, text = "Recalibration", 
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn3.grid(row = 2, column = 0, sticky = 'w')

        btn4 = tk.Button(leftFrame, text = "Connection", command=lambda: controller.show_frame("ConnectionPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn4.grid(row = 3, column = 0, sticky = 'w')

        ecLabel = tk.Label(rightFrame, text = "EC Calibration", font = ("Helvetica, 13"))
        ecLabel.grid(row = 0, column = 0)

        phLabel = tk.Label(rightFrame, text = "pH Calibration", font = ("Helvetica, 13"))
        phLabel.grid(row = 0, column = 1)

        photo = tk.PhotoImage(file = "ecGraph.png")
        ecGraph = tk.Label(rightFrame, image = photo)
        ecGraph.image = photo
        ecGraph.grid(row = 1, column = 0)

        phGraph = tk.Label(rightFrame, image = photo)
        phGraph.image = photo
        phGraph.grid(row = 1, column = 1)

        ecStatus = tk.Label(rightFrame, text = ecText[ecCounter1], font = ("Helvetica, 13"))
        ecStatus.grid(row = 2, column = 0)

        phStatus = tk.Label(rightFrame, text = phText[phCounter1], font = ("Helvetica, 13"))
        phStatus.grid(row = 2, column = 1)
        
        def setecText():
            global ecCounter1, ecText
            if ecCounter1 == 0:
                ecCounter1 = 1
                ecStatus.config(text = ecText[ecCounter1])
            elif ecCounter1 == 1:
                ecCounter1 = 2
                ecStatus.config(text = ecText[ecCounter1])
            elif ecCounter1 == 2:
                ecCounter1 = 3
                ecStatus.config(text = ecText[ecCounter1])
            elif ecCounter1 == 3:
                ecCounter1 = 0
                ecStatus.config(text = ecText[phCounter1])               
            
        def setpHText():
            global phCounter1, phText
            if phCounter1 == 0:
                phCounter1 = 1
                phStatus.config(text = phText[phCounter1])
            elif phCounter1 == 1:
                phCounter1 = 2
                phStatus.config(text = phText[phCounter1])
            elif phCounter1 == 2:
                phCounter1 = 3
                phStatus.config(text = phText[phCounter1])
            elif phCounter1 == 3:
                phCounter1 = 0
                phStatus.config(text = phText[phCounter1])
                
        
        ecBtn = tk.Button(rightFrame, text = "Proceed", font = ("Helvetica, 13"), command = setecText)
        ecBtn.grid(row = 3, column = 0, padx = 5)

        phBtn = tk.Button(rightFrame, text = "Proceed", font = ("Helvetica, 13"), command = setpHText)
        phBtn.grid(row = 3, column = 1, padx = 5)

        

class ConnectionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        leftFrame = tk.Frame(self, bg = 'cyan', width = 100, height = 100)
        rightFrame = tk.Frame(self, width = 100, height = 100)
        leftFrame.grid(row = 0, column = 0)
        rightFrame.grid(row = 0, column = 1)

        btn1 = tk.Button(leftFrame, text = "Status", command=lambda: controller.show_frame("StatusPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn1.grid(row = 0, column = 0, sticky = 'w')

        btn2 = tk.Button(leftFrame, text = "Settings", command=lambda: controller.show_frame("SettingPage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn2.grid(row = 1, column = 0, sticky = 'w')

        btn3 = tk.Button(leftFrame, text = "Recalibration", command=lambda: controller.show_frame("RecalibratePage"),
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn3.grid(row = 2, column = 0, sticky = 'w')

        btn4 = tk.Button(leftFrame, text = "Connection", 
                      width = 15, height = 7, pady = 7, font = ("Helvetica, 10"))
        btn4.grid(row = 3, column = 0, sticky = 'w')
        
if __name__ == "__main__":
    app = HydroponicApp()
    app.attributes('-fullscreen', True)
    app.bind('<Escape>', lambda e: app.destroy())
    app.mainloop()

