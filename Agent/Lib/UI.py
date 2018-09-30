#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com
# comment format like html

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow
import sys, os


class UI(QMainWindow):
    def __init__(self):
        # app = QtWidgets.QApplication(sys.argv)

        QMainWindow.__init__(self)
        self.debug = True
        self.auth = False
        self.syncn = {
                "icon" : "images/sync.ico",
                "trayicon" : "images/sync.png",
                "config" : "setting.syncn"
        }
        self.setObjectName("MainWindow")
        
        # icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.syncn["icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # tray self.syncn["trayicon"]
        self.tray = syncNTray(icon)

        # window
        self.setWindowIcon(icon)
        self.setEnabled(True)
        self.resize(390, 590)
        self.setMinimumSize(QtCore.QSize(390, 590))
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("SyncN")        
        self.setStyleSheet("background-color:rgb(255, 255, 127);")

        # window - widget
        self.w_main = QtWidgets.QWidget(self)
        self.w_main.setStyleSheet("#btn_close:hover { color:black; }\n#btn_close { color:gray; }\n#btn_tray:hover { color:black; }\n#btn_tray { color:gray; }")
        self.w_main.setObjectName("w_main")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.w_main)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # window - widget - button
        self.btn_tray = QtWidgets.QPushButton(self.w_main)
        self.btn_tray.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_tray.setFont(QtGui.QFont("Corbel", 30, 80))
        self.btn_tray.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_tray.setStyleSheet("background-color:rgb(255, 255, 127);\nborder-style:none;\nfont-family:Corbel;\nfont-size:12px;\nfont-weight:900;")
        self.btn_tray.setObjectName("btn_tray")
        
        self.btn_close = QtWidgets.QPushButton(self.w_main)
        self.btn_close.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_close.setFont(QtGui.QFont("Corbel", 12, 80))
        self.btn_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close.setStyleSheet("background-color:rgb(255, 255, 127);\nborder-style:none;")
        self.btn_close.setObjectName("btn_close")
        
        self.btn_ok = QtWidgets.QPushButton(self.w_main)
        self.btn_ok.setEnabled(False)
        self.btn_ok.setMinimumSize(QtCore.QSize(280, 45))
        self.btn_ok.setFont(QtGui.QFont("Bahnschrift Condensed", 18, 50))
        self.btn_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_ok.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btn_ok.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btn_ok.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_ok.setStyleSheet("background-color:rgb(246, 246, 246);\nborder-style:solid;\nborder-color:#e5d32e;\nborder-width:1px;")
        self.btn_ok.setInputMethodHints(QtCore.Qt.ImhNone)
        self.btn_ok.setObjectName("btn_ok")

        # window - widget - label
        self.l_title = QtWidgets.QLabel(self.w_main)
        self.l_title.setFont(QtGui.QFont("Bahnschrift Condensed", 52, 80))
        self.l_title.setStyleSheet("color:rgb(66, 54, 48)")
        self.l_title.setObjectName("l_title")
        self.l_info = QtWidgets.QLabel(self.w_main)
        self.l_info.setFont(QtGui.QFont("Bahnschrift SemiBold", 16, 80))
        self.l_info.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.l_info.setTextFormat(QtCore.Qt.PlainText)
        self.l_info.setAlignment(QtCore.Qt.AlignCenter)
        self.l_info.setObjectName("l_info")

        # window - widget - input
        self.input_info = QtWidgets.QLineEdit(self.w_main)
        self.input_info.setMinimumSize(QtCore.QSize(280, 45))
        self.input_info.setMaximumSize(QtCore.QSize(280, 45))
        self.input_info.setBaseSize(QtCore.QSize(280, 45))
        self.input_info.setFont(QtGui.QFont("Bahnschrift Condensed", 14))
        self.input_info.setStyleSheet("background-color:rgb(255, 255, 255);\nborder-style:solid;\nborder-color:#e5d32e;\nborder-width:1px;")
        self.input_info.setClearButtonEnabled(True)
        self.input_info.setFocus(True);
        self.input_info.setObjectName("input_info")
        

        # window - widget - spacer
        spacerItem = QtWidgets.QSpacerItem(500, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        spacerItem4 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        #layout - header
        self.la_header = QtWidgets.QHBoxLayout()
        self.la_header.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.la_header.setSpacing(2)
        self.la_header.addItem(spacerItem)
        self.la_header.addWidget(self.btn_tray)
        self.la_header.addWidget(self.btn_close)
        self.la_header.setObjectName("la_header")
        #layout - title
        self.la_body_all = QtWidgets.QHBoxLayout()
        self.la_body_all.addItem(spacerItem1)
        self.la_body_all.addWidget(self.l_title)
        self.la_body_all.addItem(spacerItem2)
        self.la_body_all.setObjectName("la_body_all")
        #layout - content
        self.la_footer_body = QtWidgets.QVBoxLayout()
        self.la_footer_body.addWidget(self.l_info)
        self.la_footer_body.addWidget(self.input_info)
        self.la_footer_body.addWidget(self.btn_ok)
        self.la_footer_body.addItem(spacerItem4)
        self.la_footer_body.setObjectName("la_footer_body")
        #layout - body
        self.la_footer_all = QtWidgets.QHBoxLayout()
        self.la_footer_all.addItem(spacerItem3)
        self.la_footer_all.addLayout(self.la_footer_body)
        self.la_footer_all.addItem(spacerItem5)
        self.la_footer_all.setObjectName("la_footer_all")
        #layout - html
        self.la_content = QtWidgets.QVBoxLayout()
        self.la_content.addLayout(self.la_body_all)
        self.la_content.addLayout(self.la_footer_all)
        self.la_content.setObjectName("la_content")
        
        self.verticalLayout_3.addLayout(self.la_header)
        self.verticalLayout_3.addLayout(self.la_content)
        self.setCentralWidget(self.w_main)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        # check auth
        if self.debug: print("init End")
        

    # function
    def msg(self, title="Notify", msg=""):
        QMessageBox.about(None, title, msg)

    def checkInput(self, to):
        chkBit = True if self.input_info.text() else False
        self.btn_ok.setEnabled(chkBit)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()
        self.mouse_down = event.button()== Qt.LeftButton

    def mouseReleaseEvent(self, e):
        self.mouse_down = False

    def keyPressEvent(self, e):
        if e.key() == 16777216: self.windowTrigger()
        
    def mouseMoveEvent(self, event):
        x=event.x()
        y=event.y()
        self.move(self.pos() + event.globalPos() - self.old_pos)
        self.old_pos = event.globalPos()
        event.accept()
    
    def windowTrigger(self):
        if self.tray.isActive:
            self.show()
            self.tray.hide()
            self.tray.isActive = False
        else:
            self.hide()
            self.tray.show()
            self.tray.isActive = True

    def authStyle(self):
        self.l_info.setStyleSheet("color:green;\n")
        self.l_info.setText("Successful Auth\nStart! SyncN on Tray")
        self.input_info.setAlignment(Qt.AlignCenter)
        self.input_info.setFont(QtGui.QFont("Corbel", 7, 10))
        self.input_info.setText("01234567890123")
        self.input_info.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_info.setEnabled(False)
        self.input_info.setClearButtonEnabled(False)
        self.btn_ok.setText("Run on Tray")
        self.btn_ok.setEnabled(True)
        self.auth = True
    
    def openWindow(self, reason):
        try:
            if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
                self.windowTrigger()
                self.raise_()
        except Exception as e:
            print("{0} openWindow, check this {0}".format(__file__, e))
            pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.w_main.setToolTip(_translate("MainWindow", "Sync your sticky note on Windows 10"))
        self.btn_tray.setToolTip(_translate("MainWindow", "Minimumrize window(Tray)"))
        self.btn_tray.setText(_translate("MainWindow", "_"))
        self.btn_close.setToolTip(_translate("MainWindow", "Close"))
        self.btn_close.setText(_translate("MainWindow", "X"))
        self.l_title.setText(_translate("MainWindow", "SyncN"))
        self.l_info.setText(_translate("MainWindow", "Typing Your E-mail"))
        self.input_info.setToolTip(_translate("MainWindow", "Using only your E-mail"))
        self.input_info.setPlaceholderText(_translate("MainWindow", "exampel@mail.com"))
        self.btn_ok.setToolTip(_translate("MainWindow", "Click when you sure Okay"))
        self.btn_ok.setText(_translate("MainWindow", "OK"))

class syncNTray(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        
        self.isEncrypt = False
        self.isActive = False
        self.syncAction = QtWidgets.QAction("Sync", self, checkable=True)
        self.syncAction.setStatusTip('Default Yes')
        self.syncAction.setChecked(True)
        menu.addAction(self.syncAction)
        self.shareAction = menu.addAction("Share(comming soon)")
        self.shareAction.setToolTip("You Can Send to Firends, only using email")
        self.protectAction = QtWidgets.QAction("Encryption(comming soon)", self, checkable=True)
        self.protectAction.setStatusTip('Default No')
        self.protectAction.setChecked(False)
        menu.addAction(self.protectAction)
        self.accountAction = menu.addAction("Account")
        self.logoutAction = menu.addAction("Logout")
        self.logoutAction.setToolTip("if click this, you can't sync anymore")
        self.exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        self.setToolTip("SyncN[:Sync Note on Windows]!")

if __name__ == "__main__":
    print("Start application")
    app = QtWidgets.QApplication(sys.argv)
    application = UI()
    application.show()
    sys.exit(app.exec_())
    
    
    
    
    

