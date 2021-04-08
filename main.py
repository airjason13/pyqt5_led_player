# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel

from UI.mainwindows import Ui_MainWindow

import sys
import numpy as np
import cv2
import os
import screen_utils
import glob
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, Response

from flask_plugin import *
from global_def import *
from ffmpy_utils import *
#FileFolder = '/home/jason/Videos/Demo_Video/'

os.chdir(FileFolder)
#mp4_extends = '*.mp4'
#SIZE_MB = 1024*1024
file_index = 0

app = Flask(__name__)
from routes import *
title = 'Flask Web App'

"""@app.route("/")
def index():
    print("find index!")
    #maps = find_maps()
    return render_template("index.html", title=title)"""

def find_maps():
    maps = {}
    for fname in glob.glob(mp4_extends):
        if os.path.isfile(fname):
            key = fname  # .decode()
            maps[key] = round(os.path.getsize(fname) / SIZE_MB, 3)

    return maps


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def find_filelists():
    filelists = sorted(glob.glob(mp4_extends))
    return filelists

class Video():
    def __init__(self, filelists, changefiles_cb):
        print("Video Init")
        self.video_index = 0
        self.filelists = filelists
        self.capture = cv2.VideoCapture(self.filelists[self.video_index])
        self.currentFrame = np.array([])
        self.changeplayingfile_cb = changefiles_cb
        self.changeplayingfile_cb(self.filelists[self.video_index])


    def captureFrame(self):
        ret, readFrame = self.capture.read()
        cv2.imshow("video", readFrame)
        return readFrame

    def captureNextFrame(self):
        ret, readFrame = self.capture.read()
        if ret is False:
            self.video_index += 1
            if self.video_index >= len(self.filelists):
                self.video_index = 0
            self.capture = cv2.VideoCapture(self.filelists[self.video_index])
            self.changeplayingfile_cb(self.filelists[self.video_index])
            #self.capture = cv2.VideoCapture("./3a_demo.mp4")
        else:
            readFrame = cv2.resize(readFrame, (80, 100))
            readFrame = cv2.flip(readFrame, 1)
            #readFrame = cv2.imread("./red.jpg")
            #readFrame = cv2.resize(readFrame, (80, 100))
            #if (ret == True):
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(self.currentFrame, width, height, QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None

    def get_playing_filename(self):
        return self.filelists[self.video_index]

    def __del__(self):
        print("del Video")

class SubWindow(QtWidgets.QWidget):
    def __init__(self):
        super(SubWindow, self).__init__()
        self.resize(400, 300)

        # Label
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 80, 100)
        self.label.setText('Sub Window')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        #self.setWindowFlag(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet('font-size:40px')
        self.move(1920, 0)
        self.showFullScreen()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



        self._timer = QTimer(self)
        self._timer.timeout.connect(self.play)
        self.ispause = False
        self.isplaying = False

        self.ui.StartHDMIin.clicked.connect(self.startHDMIin)
        self.ui.closeButton.clicked.connect(self.closewindows)
        self.ui.PauseButton.clicked.connect(self.pause)
        self.ui.PauseButton.setEnabled(False)


        '''Sub window setup'''
        self.sub_window = SubWindow()
        self.sub_window.show()

    def set_video_files(self, filelists):
        self.video_filelists = filelists
        #self.cap = self.video_filelists
        #self.video = Video(self.video_filelists, self.changeplayingfile)

    def changeplayingfile(self, filename):
        #if str(filename).startswith("1"):
        if "ultra_fast" in str(filename):
            self._timer.start(15)
            print("ultra_fast")
        elif "fast" in str(filename):
            self._timer.start(45)
            print("fast")
        else:
            self._timer.start(90)
        self.ui.playingfilelabel.setText("Now playing : " + filename)


    def closewindows(self):
        self.sub_window.close()
        self.close()

    def startHDMIin(self):
        if self.isplaying is False:
            print("startHDMIin")
            #self.video = Video(self.video_filelists)
            self.video = Video(self.video_filelists, self.changeplayingfile)
            self.ui.PauseButton.setEnabled(True)
            self.ui.StartHDMIin.setText("Stop")
            self._timer.start(60)
            self.isplaying = True
        else:
            self.ui.StartHDMIin.setText("Play All Repeat")
            self.ui.PauseButton.setText("Pause")
            self.ui.PauseButton.setEnabled(False)
            self._timer.stop()
            self.video = None
            self.isplaying = False

    def play(self):
        try:
            self.video.captureNextFrame()
            self.ui.videolabel.setPixmap(self.video.convertFrame())
            self.sub_window.label.setPixmap(self.video.convertFrame())
            #self.ui.videolabel.setScaledContents(True)
            #print("play video")
        except TypeError:
            print('No Frame')

    def pause(self):
        print("pause")
        if self.ispause is True:
            self._timer.start(90)
            self.ispause = False
            self.ui.PauseButton.setText("Pause")

            print("re-start")
        else :#if self._timer.isActive():
            self.ispause = True
            self._timer.stop()
            self.ui.PauseButton.setText("Re-Start")

            print("timer stop")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    qtapp = QtWidgets.QApplication([])
    window = MainWindow()
    screen_counts = screen_utils.get_screen_count(qtapp)
    print("screen_counts = ", screen_counts)
    file_lists = find_filelists()
    print("file maps = ", file_lists)

    window.set_video_files(file_lists)
    route_test()
    #app.run(debug=False, host='0.0.0.0', port=9090, threaded=True)
    webapp=ApplicationThread(app)
    webapp.start()
    #subwindow = SubWindow()
    """desktop = app.desktop()

    # 获取显示器分辨率大小
    monitors = desktop.screent()

    print(monitors)
    for i in range(monitors):
        screenRect = desktop.availableGeometry(i)
        height = screenRect.height()
        width = screenRect.width()

        print(height)
        print(width)"""
    get_thumbnail_from_video(FileFolder + file_lists[0])

    window.move(0, 0)
    window.show()

    sys.exit(qtapp.exec_())


