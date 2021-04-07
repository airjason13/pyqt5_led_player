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

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

FileFolder = '/home/jason/Videos/Demo_Video/'

os.chdir(FileFolder)
mp4_extends = '*.mp4'
SIZE_MB = 1024*1024
file_index = 0

def find_filelists():
    """filelists = []
    for fname in glob.glob(mp4_extends):
        print(fname)
        filelists.extend(fname)"""
    filelists = glob.glob(mp4_extends)

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
        #self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture("./3a_demo.mp4")
        #self.cap = cv2.VideoCapture("./logos.mp4")
        #self.cap = cv2.VideoCapture(file_maps[0])
        #self.video = Video(self.cap)
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
            self._timer.start(90)
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

    app = QtWidgets.QApplication([])
    window = MainWindow()
    screen_counts = screen_utils.get_screen_count(app)
    print("screen_counts = ", screen_counts)
    file_lists = find_filelists()
    print("file maps = ", file_lists[0])
    #for k in file_lists:
    #    print("file : ", k)
    window.set_video_files(file_lists)
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


    window.move(0, 0)
    window.show()

    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
