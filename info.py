# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

#created by: sidhas roosara mendis (DRAGON) 
#github link:

from PyQt5 import QtCore, QtGui, QtWidgets
commenstyle =("*{border: "+"2px"+" solid "+"red"+";"+
                "color: "+"red"+";"+
                "border-radius: "+"2px"+";}"+
                "*:hover{background: 'blue';}")

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("info")
        Frame.setFixedSize(320, 240)
        self.info = QtWidgets.QLabel(Frame)
        self.info.setGeometry(QtCore.QRect(30, 30, 261, 171))
        self.info.setObjectName("info")
        self.info.setStyleSheet(commenstyle)
        self.checkupdate = QtWidgets.QPushButton(Frame)
        self.checkupdate.setGeometry(QtCore.QRect(30, 210, 75, 23))
        self.checkupdate.setObjectName("checkupdate")
        self.checkupdate.setStyleSheet(commenstyle)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "info"))
        self.info.setText(_translate("Frame", "<html><head/><body><p>created by roosara mendis</p><p><br/></p><p>software version :- Test 1</p><p><br/></p><p>web :- blablabla</p></body></html>"))
        self.checkupdate.setText(_translate("Frame", "check update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())