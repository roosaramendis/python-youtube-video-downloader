#created by: sidhas roosara mendis (DRAGON) 
#github link:

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
import sys
import py_youtubedownloader_UI, py_settings,info

class info(QtWidgets.QMainWindow, info.Ui_Frame):
    def __init__(self, parent=None):
        super(info, self).__init__(parent)
        self.setupUi(self)

class settings_window(QtWidgets.QMainWindow, py_settings.Ui_Frame):
    def __init__(self, parent=None):
        super (settings_window, self).__init__(parent)
        self.setupUi(self)
        self.credits.clicked.connect(self.credits_clk1)
        self.dialog1 = info(self)
    def credits_clk1(self):
        self.dialog1.show()    
class downloader_window(QtWidgets.QMainWindow, py_youtubedownloader_UI.Ui_Form):
    def __init__(self, parent=None):
        super(downloader_window, self).__init__(parent)
        self.setupUi(self)
        
        self.pb_settings.clicked.connect(self.on_pushButton_clicked)
        self.dialog = settings_window(self)

    def on_pushButton_clicked(self):
        self.dialog.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    stylef = QFile("style1.css") 
    stylef.open(QFile.ReadOnly | QFile.Text)
    stylesheet = QTextStream(stylef)
    stylesheetstr =stylesheet.readAll()
    print(stylesheetstr)
    app.setStyleSheet(stylesheetstr)
    main = downloader_window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 