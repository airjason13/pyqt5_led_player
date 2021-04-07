from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel

def get_pri_geometry(app):
    #app = QtWidgets.QApplication([])
    desktop = app.desktop()
    monitors = desktop.screenCount()

    screenRect = desktop.availableGeometry(0)
    height = screenRect.height()
    width = screenRect.width()

    print(height)
    print(width)
    return width, height

def get_sec_geometry(app):
    #app = QtWidgets.QApplication([])
    desktop = app.desktop()
    monitors = desktop.screenCount()
    if monitors is 1:
        return 0, 0
    screenRect = desktop.availableGeometry(1)
    height = screenRect.height()
    width = screenRect.width()

    print(height)
    print(width)
    return width, height

def get_screen_count(app):
    #app = QtWidgets.QApplication([])
    desktop = app.desktop()
    monitors = desktop.screenCount()
    print("screen count is ", monitors)
    return monitors