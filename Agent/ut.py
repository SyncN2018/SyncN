# import sqlite3, pydash as _, uuid
# #windows RS4 under version location is C: \Users\Username\AppData\Roaming\Microsoft\Sticky Notes\StickyNotes.snt 

# class noteSql():
#     def __init__(self, fullPath):
#         self.path = ''
#         self.cursor = None
#         self.conn = None
#         self.build(fullPath)
#         pass

#     def read(self, chk=False):
#         col = "WindowPosition, Theme, Id, ParentId" if chk else "Text, WindowPosition, Theme"
#         rs = self.cursor.execute("SELECT " + col + " FROM Note")
#         rs_array = []
#         for row in rs:
#             rs_array.append(row)
#             if(chk): break
#         return self.convert(rs_array, chk)


#     def build(self, path):
#         self.path = path
#         self.conn = sqlite3.connect(path)
#         self.cursor = self.conn.cursor()
#         pass
        

#     def update(self):
#         # db.execute('update note set  = ? where t1 = ?', (row['i1'], row['t1']))
#         # db.commit()
#         pass

#     def convert(self, items, chk):
#         notes = {}
#         cnt = 1
#         i = None
#         for item in items:
#             if(chk):
#                 i = {str(cnt): { "WindowPosition": item[0], "Theme": item[1], "Id" : item[2], "ParentId" : item[3] }}
#             else:
#                 i = {str(cnt): { "Text": item[0], "WindowPosition": item[1], "Theme": item[2] }}
#             notes.update(i)
#             cnt+=1
#         return notes

#     def check(self):
#         return self.read(chk=True)

# section

# def main():
#     dao = noteSql(
#         "C:\\Users\\hdh09\\AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite")
#     print(dao.read())
    
# if __name__ == '__main__':
#     main()

# import os
# def detailSearch(root_path):
#     for (path, dirname, files) in os.walk(root_path):
#         for f in files:
#             fullPath = path + '/' + f

#             print(fullPath)

# search2(os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+"\AppData\Local\Packages")



# section test mq connection

# import pika
# import json
# from Lib import *

# class MQ():
#     def __init__(self):
#         with open("Setting.syncn", 'r') as configfile:
#             self.ServerData = json.load(configfile)
#         self.QueueName = self.ServerData['q']
#         self.Userid = self.ServerData['id']
#         self.Userpw = self.ServerData['pw']
#         self.RoutingKey = self.QueueName
#         # self.SqlObject = NoteSql.noteSql()
#         # self.SqlData = self.SqlObject.read()
#         self.Message = "WTF"
#         self.exchange = "msg"


#     def SendQueue(self):
#         self.url = 'amqp://' + self.Userid + ":" + self.Userpw + '@jis5376.iptime.org/syncn'
#         # self.url = 'amqp://' + "jis" + ":" + "suck0818" + '@jis5376.iptime.org/syncn'
#         self.SendConnection = pika.BlockingConnection(pika.URLParameters(self.url))
#         self.SendChannel = self.SendConnection.channel()
#         # self.SendChannel.queue_declare(queue=self.QueueName)
#         self.SendChannel.basic_publish(exchange=self.exchange,routing_key=self.RoutingKey,body=json.dumps(self.Message))

#         print(" [x] Sent %r" % self.Message)
#         self.SendConnection.close()



#     def ReceiveQueue(self):
#         self.url = 'amqp://' + self.Userid + ":" + self.Userpw + '@jis5376.iptime.org/syncn'
#         # self.url = 'amqp://' + "jis" + ":" + "suck0818" + '@jis5376.iptime.org/syncn'
#         self.ReceiveConnection = pika.BlockingConnection(pika.URLParameters(self.url))
#         self.ReceiveChannel = self.ReceiveConnection.channel()
#         # self.ReceiveChannel.queue_declare(queue=self.QueueName)


#         self.ReceiveChannel.basic_consume(self.callback, queue=self.QueueName, no_ack=True)

#         print(' [*] Wationg for messages. To exit press CTRL+C')
#         self.ReceiveChannel.start_consuming()

#     def callback(self, ch, method, properties, body):
#         print(" [x] Received %r" % json.loads(body))
#         #example = json.loads(body)['1']['Text']

# if __name__ == '__main__':
#     Connection = MQ()
#     Connection.SendQueue()
#     Connection.ReceiveQueue()


# #  section
# import sys
# from PyQt5.QtCore import QSize
# from PyQt5.QtGui import QImage, QPalette, QBrush
# from PyQt5.QtWidgets import *

# class MainWindow(QWidget):
#     def __init__(self):
#        QWidget.__init__(self)
#        self.setGeometry(100,100,300,200)

#        oImage = QImage("UI\\images\\bg.png")
#        sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
#        palette = QPalette()
#        palette.setBrush(10, QBrush(sImage))                     # 10 = Windowrole
#        self.setPalette(palette)

#        self.label = QLabel('Test', self)                        # test, if it's really backgroundimage
#        self.label.setGeometry(50,50,200,50)

#        self.show()

# if __name__ == "__main__":

#     app = QApplication(sys.argv)
#     oMainwindow = MainWindow()
#     sys.exit(app.exec_())
#########################################################
## customize Title bar
## dotpy.ir
## iraj.jelo@gmail.com
#########################################################
# import sys
# from PyQt5 import QtWidgets, QtGui
# from PyQt5 import QtCore
# from PyQt5.QtCore import Qt

# class TitleBar(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         css = """
#         QWidget{
#             Background: #AA00AA;
#             color:white;
#             font:12px bold;
#             font-weight:bold;
#             border-radius: 1px;
#             height: 11px;
#         }
#         QDialog{
#             Background-image:url('img/titlebar bg.png');
#             font-size:12px;
#             color: black;

#         }
#         QToolButton{
#             Background:#AA00AA;
#             font-size:11px;
#         }
#         QToolButton:hover{
#             Background: #FF00FF;
#             font-size:11px;
#         }
#         """
#         self.setAutoFillBackground(True)
#         self.setBackgroundRole(QtGui.QPalette.Highlight)
#         self.setStyleSheet(css)
#         self.minimize=QtWidgets.QToolButton(self)
#         self.minimize.setIcon(QtGui.QIcon('img/min.png'))
#         self.maximize=QtWidgets.QToolButton(self)
#         self.maximize.setIcon(QtGui.QIcon('img/max.png'))
#         close=QtWidgets.QToolButton(self)
#         close.setIcon(QtGui.QIcon('img/close.png'))
#         self.minimize.setMinimumHeight(10)
#         close.setMinimumHeight(10)
#         self.maximize.setMinimumHeight(10)
#         label=QtWidgets.QLabel(self)
#         label.setText("test")
#         self.setWindowTitle("Window Title")
#         hbox=QtWidgets.QHBoxLayout(self)
#         hbox.addWidget(label)
#         hbox.addWidget(self.minimize)
#         hbox.addWidget(self.maximize)
#         hbox.addWidget(close)
#         hbox.insertStretch(1,500)
#         hbox.setSpacing(0)
#         self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
#         self.maxNormal=False
#         close.clicked.connect(self.close)
#         self.minimize.clicked.connect(self.showSmall)
#         self.maximize.clicked.connect(self.showMaxRestore)

#     def showSmall(self):
#         box.showMinimized()

#     def showMaxRestore(self):
#         if(self.maxNormal):
#             box.showNormal()
#             self.maxNormal= False
#             self.maximize.setIcon(QtGui.QIcon('img/max.png'))
#             print('1')
#         else:
#             box.showMaximized()
#             self.maxNormal=  True
#             print('2')
#             self.maximize.setIcon(QtGui.QIcon('img/max2.png'))

#     def close(self):
#         box.close()

#     def mousePressEvent(self,event):
#         if event.button() == Qt.LeftButton:
#             box.moving = True
#             box.offset = event.pos()

#     def mouseMoveEvent(self,event):
#         if box.moving: box.move(event.globalPos()-box.offset)


# class Frame(QtWidgets.QFrame):
#     def __init__(self, parent=None):
#         QtWidgets.QFrame.__init__(self, parent)
#         self.m_mouse_down= False
#         self.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setMouseTracking(True)
#         self.m_titleBar= TitleBar(self)
#         self.m_content= QtWidgets.QWidget(self)
#         vbox=QtWidgets.QVBoxLayout(self)
#         vbox.addWidget(self.m_titleBar)
#         vbox.setContentsMargins(0, 0, 0, 0)
#         vbox.setSpacing(0)
#         layout=QtWidgets.QVBoxLayout()
#         layout.addWidget(self.m_content)
#         layout.setContentsMargins(5, 5, 5, 5)
#         layout.setSpacing(0)
#         vbox.addLayout(layout)
#         # Allows you to access the content area of the frame
#         # where widgets and layouts can be added

#     def contentWidget(self):
#         return self.m_content

#     def titleBar(self):
#         return self.m_titleBar

#     def mousePressEvent(self,event):
#         self.m_old_pos = event.pos()
#         self.m_mouse_down = event.button()== Qt.LeftButton

#     def mouseMoveEvent(self,event):
        
#         x=event.x()
#         y=event.y()
#         print(x, y)

#     def mouseReleaseEvent(self,event):
#         m_mouse_down=False

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     box = Frame()
#     box.move(60,60)
#     l=QtWidgets.QVBoxLayout(box.contentWidget())
#     l.setContentsMargins(0, 0, 0, 0)
#     edit=QtWidgets.QLabel("""I would've did anything for you to show you how much I adored you
# But it's over now, it's too late to save our loveJust promise me you'll think of me
# Every time you look up in the sky and see a star 'cuz I'm  your star.""")
#     l.addWidget(edit)
#     box.show()
#     app.exec_()
# section
#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
#         QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
#         QMessageBox, QMenu, QPushButton, QSpinBox, QStyle, QSystemTrayIcon,
#         QTextEdit, QVBoxLayout)

# import systray_rc


# class Window(QDialog):
#     def __init__(self):
#         super(Window, self).__init__()

#         self.createIconGroupBox()
#         self.createMessageGroupBox()

#         self.iconLabel.setMinimumWidth(self.durationLabel.sizeHint().width())

#         self.createActions()
#         self.createTrayIcon()

#         self.showMessageButton.clicked.connect(self.showMessage)
#         self.showIconCheckBox.toggled.connect(self.trayIcon.setVisible)
#         self.iconComboBox.currentIndexChanged.connect(self.setIcon)
#         self.trayIcon.messageClicked.connect(self.messageClicked)
#         self.trayIcon.activated.connect(self.iconActivated)

#         mainLayout = QVBoxLayout()
#         mainLayout.addWidget(self.iconGroupBox)
#         mainLayout.addWidget(self.messageGroupBox)
#         self.setLayout(mainLayout)

#         self.iconComboBox.setCurrentIndex(1)
#         self.trayIcon.show()

#         self.setWindowTitle("Systray")
#         self.resize(400, 300)

#     def setVisible(self, visible):
#         self.minimizeAction.setEnabled(visible)
#         self.maximizeAction.setEnabled(not self.isMaximized())
#         self.restoreAction.setEnabled(self.isMaximized() or not visible)
#         super(Window, self).setVisible(visible)

#     def closeEvent(self, event):
#         if self.trayIcon.isVisible():
#             QMessageBox.information(self, "Systray",
#                     "The program will keep running in the system tray. To "
#                     "terminate the program, choose <b>Quit</b> in the "
#                     "context menu of the system tray entry.")
#             self.hide()
#             event.ignore()

#     def setIcon(self, index):
#         icon = self.iconComboBox.itemIcon(index)
#         self.trayIcon.setIcon(icon)
#         self.setWindowIcon(icon)

#         self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

#     def iconActivated(self, reason):
#         if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
#             self.iconComboBox.setCurrentIndex(
#                     (self.iconComboBox.currentIndex() + 1)
#                     % self.iconComboBox.count())
#         elif reason == QSystemTrayIcon.MiddleClick:
#             self.showMessage()

#     def showMessage(self):
#         icon = QSystemTrayIcon.MessageIcon(
#                 self.typeComboBox.itemData(self.typeComboBox.currentIndex()))
#         self.trayIcon.showMessage(self.titleEdit.text(),
#                 self.bodyEdit.toPlainText(), icon,
#                 self.durationSpinBox.value() * 1000)

#     def messageClicked(self):
#         QMessageBox.information(None, "Systray",
#                 "Sorry, I already gave what help I could.\nMaybe you should "
#                 "try asking a human?")

#     def createIconGroupBox(self):
#         self.iconGroupBox = QGroupBox("Tray Icon")

#         self.iconLabel = QLabel("Icon:")

#         self.iconComboBox = QComboBox()
#         self.iconComboBox.addItem(QIcon(':/images/bad.png'), "Bad")
#         self.iconComboBox.addItem(QIcon(':/images/heart.png'), "Heart")
#         self.iconComboBox.addItem(QIcon(':/images/trash.png'), "Trash")

#         self.showIconCheckBox = QCheckBox("Show icon")
#         self.showIconCheckBox.setChecked(True)

#         iconLayout = QHBoxLayout()
#         iconLayout.addWidget(self.iconLabel)
#         iconLayout.addWidget(self.iconComboBox)
#         iconLayout.addStretch()
#         iconLayout.addWidget(self.showIconCheckBox)
#         self.iconGroupBox.setLayout(iconLayout)

#     def createMessageGroupBox(self):
#         self.messageGroupBox = QGroupBox("Balloon Message")

#         typeLabel = QLabel("Type:")

#         self.typeComboBox = QComboBox()
#         self.typeComboBox.addItem("None", QSystemTrayIcon.NoIcon)
#         self.typeComboBox.addItem(self.style().standardIcon(
#                 QStyle.SP_MessageBoxInformation), "Information",
#                 QSystemTrayIcon.Information)
#         self.typeComboBox.addItem(self.style().standardIcon(
#                 QStyle.SP_MessageBoxWarning), "Warning",
#                 QSystemTrayIcon.Warning)
#         self.typeComboBox.addItem(self.style().standardIcon(
#                 QStyle.SP_MessageBoxCritical), "Critical",
#                 QSystemTrayIcon.Critical)
#         self.typeComboBox.setCurrentIndex(1)

#         self.durationLabel = QLabel("Duration:")

#         self.durationSpinBox = QSpinBox()
#         self.durationSpinBox.setRange(5, 60)
#         self.durationSpinBox.setSuffix(" s")
#         self.durationSpinBox.setValue(15)

#         durationWarningLabel = QLabel("(some systems might ignore this hint)")
#         durationWarningLabel.setIndent(10)

#         titleLabel = QLabel("Title:")

#         self.titleEdit = QLineEdit("Cannot connect to network")

#         bodyLabel = QLabel("Body:")

#         self.bodyEdit = QTextEdit()
#         self.bodyEdit.setPlainText("Don't believe me. Honestly, I don't have "
#                 "a clue.\nClick this balloon for details.")

#         self.showMessageButton = QPushButton("Show Message")
#         self.showMessageButton.setDefault(True)

#         messageLayout = QGridLayout()
#         messageLayout.addWidget(typeLabel, 0, 0)
#         messageLayout.addWidget(self.typeComboBox, 0, 1, 1, 2)
#         messageLayout.addWidget(self.durationLabel, 1, 0)
#         messageLayout.addWidget(self.durationSpinBox, 1, 1)
#         messageLayout.addWidget(durationWarningLabel, 1, 2, 1, 3)
#         messageLayout.addWidget(titleLabel, 2, 0)
#         messageLayout.addWidget(self.titleEdit, 2, 1, 1, 4)
#         messageLayout.addWidget(bodyLabel, 3, 0)
#         messageLayout.addWidget(self.bodyEdit, 3, 1, 2, 4)
#         messageLayout.addWidget(self.showMessageButton, 5, 4)
#         messageLayout.setColumnStretch(3, 1)
#         messageLayout.setRowStretch(4, 1)
#         self.messageGroupBox.setLayout(messageLayout)

#     def createActions(self):
#         self.minimizeAction = QAction("Mi&nimize", self, triggered=self.hide)
#         self.maximizeAction = QAction("Ma&ximize", self,
#                 triggered=self.showMaximized)
#         self.restoreAction = QAction("&Restore", self,
#                 triggered=self.showNormal)
#         self.quitAction = QAction("&Quit", self,
#                 triggered=QApplication.instance().quit)

#     def createTrayIcon(self):
#          self.trayIconMenu = QMenu(self)
#          self.trayIconMenu.addAction(self.minimizeAction)
#          self.trayIconMenu.addAction(self.maximizeAction)
#          self.trayIconMenu.addAction(self.restoreAction)
#          self.trayIconMenu.addSeparator()
#          self.trayIconMenu.addAction(self.quitAction)

#          self.trayIcon = QSystemTrayIcon(self)
#          self.trayIcon.setContextMenu(self.trayIconMenu)


# if __name__ == '__main__':

#     import sys
    

#     app = QApplication(sys.argv)

#     if not QSystemTrayIcon.isSystemTrayAvailable():
#         QMessageBox.critical(None, "Systray",
#                 "I couldn't detect any system tray on this system.")
#         sys.exit(1)

#     QApplication.setQuitOnLastWindowClosed(False)

#     window = Window()
#     window.show()
#     sys.exit(app.exec_())


# section

# icon_path="custom.ico"
# from win10toast import ToastNotifier
# import time
# toaster = ToastNotifier()
# toaster.show_toast("Hello World!!!", "Python is 10 seconds awsm!", duration=10)

# toaster.show_toast("Example two", "This notification is in it's own thread!", icon_path=None, duration=5, threaded=True)
# # Wait for threaded notification to finish
# while toaster.notification_active(): time.sleep(0.1)

# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
# code source: https://stackoverflow.com/questions/893984/pyqt-show-menu-in-a-system-tray-application  - add answer PyQt5
#PyQt4 to PyQt5 version: https://stackoverflow.com/questions/20749819/pyqt5-failing-import-of-qtgui
# class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

#     def __init__(self, icon, parent=None):
#         QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
#         menu = QtWidgets.QMenu(parent)
#         syncAction = menu.addAction("Sync")
#         shareAction = menu.addAction("Share")
#         protectAction = menu.addAction("Encryption")
#         uninstallAction = menu.addAction("Uninstall")
#         logoutAction = menu.addAction("Logout")
#         exitAction = menu.addAction("Exit")
#         self.setContextMenu(menu)

# def main(image):
#     app = QtWidgets.QApplication(sys.argv)

#     w = QtWidgets.QWidget()
#     trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)

#     trayIcon.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     on=r'UI\\images\\sync.png'# ADD PATH OF YOUR ICON HERE .png works
#     main(on)



# /section

# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *


# class MyMainGUI(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.qtxt1 = QTextEdit(self)
#         self.btn1 = QPushButton("Start", self)
#         self.btn2 = QPushButton("Stop", self)
#         self.btn3 = QPushButton("add 100", self)
#         self.btn4 = QPushButton("send instance", self)

#         vbox = QVBoxLayout()
#         vbox.addWidget(self.qtxt1)
#         vbox.addWidget(self.btn1)
#         vbox.addWidget(self.btn2)
#         vbox.addWidget(self.btn3)
#         vbox.addWidget(self.btn4)
#         self.setLayout(vbox)

#         self.setGeometry(100, 50, 300, 300)

# class Test:
#     def __init__(self):
#         name = ""


# class MyMain(MyMainGUI):
#     add_sec_signal = pyqtSignal()
#     send_instance_singal = pyqtSignal("PyQt_PyObject")

#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.btn1.clicked.connect(self.time_start)
#         self.btn2.clicked.connect(self.time_stop)
#         self.btn3.clicked.connect(self.add_sec)
#         self.btn4.clicked.connect(self.send_instance)

#         self.th = Worker(parent=self)
#         self.th.sec_changed.connect(self.time_update)  # custom signal from worker thread to main thread

#         self.add_sec_signal.connect(self.th.add_sec)   # custom signal from main thread to worker thread
#         self.send_instance_singal.connect(self.th.recive_instance_singal)
#         self.show()

#     @pyqtSlot()
#     def time_start(self):
#         self.th.start()
#         self.th.working = True

#     @pyqtSlot()
#     def time_stop(self):
#         self.th.working = False

#     @pyqtSlot()
#     def add_sec(self):
#         print(".... add singal emit....")
#         self.add_sec_signal.emit()

#     @pyqtSlot(str)
#     def time_update(self, msg):
#         self.qtxt1.append(msg)

#     @pyqtSlot()
#     def send_instance(self):
#         t1 = Test()
#         t1.name = "SuperPower!!!"
#         self.send_instance_singal.emit(t1)


# class Worker(QThread):
#     sec_changed = pyqtSignal(str)

#     def __init__(self, sec=0, parent=None):
#         super().__init__()
#         self.main = parent
#         self.working = True
#         self.sec = sec

#         # self.main.add_sec_signal.connect(self.add_sec)   # 이것도 작동함. # custom signal from main thread to worker thread

#     def __del__(self):
#         print(".... end thread.....")
#         self.wait()

#     def run(self):
#         while self.working:
#             self.sec_changed.emit('time (secs)：{}'.format(self.sec))
#             self.sleep(1)
#             self.sec += 1

#     @pyqtSlot()
#     def add_sec(self):
#         print("add_sec....")
#         self.sec += 100

#     @pyqtSlot("PyQt_PyObject")    # @pyqtSlot(object) 도 가능..
#     def recive_instance_singal(self, inst):
#         print(inst.name)



# if __name__ == "__main__":
#     import sys

#     app = QApplication(sys.argv)
#     form = MyMain()
#     app.exec_()

# section
# import sys
# import time

# from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
#                           QThreadPool, pyqtSignal)
# class Runnable(QRunnable):
    
#     def run(self):
#         count = 0
#         app = QCoreApplication.instance()
#         while count < 5:
#             print("C Increasing")
#             time.sleep(1)
#             count += 1
#         app.quit()


# def using_q_thread():
#     app = QCoreApplication([])
#     thread = QThread()
#     thread.finished.connect(app.exit)
#     thread.start()
#     sys.exit(app.exec_())

# def using_move_to_thread():
#     app = QCoreApplication([])
#     objThread = QThread()
#     obj = SomeObject()
#     obj.moveToThread(objThread)
#     obj.finished.connect(objThread.quit)
#     objThread.started.connect(obj.long_running)
#     objThread.finished.connect(app.exit)
#     objThread.start()
#     sys.exit(app.exec_())

# def using_q_runnable():
#     app = QCoreApplication([])
#     runnable = Runnable()
#     QThreadPool.globalInstance().start(runnable)
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     using_q_thread()
#     using_move_to_thread()
#     using_q_runnable()

# section
# import sys
# from PyQt5 import QtWidgets, QtGui, QtCore

# class MainWindow(QtWidgets.QWidget):
#     def __init__(self):
#         # call super class constructor
#         super(MainWindow, self).__init__()
#         # build the objects one by one
#         layout = QtWidgets.QVBoxLayout(self)
#         self.pb_load = QtWidgets.QPushButton('Load')
#         self.pb_clear= QtWidgets.QPushButton('Clear')
#         self.edit = QtWidgets.QTextEdit()
#         layout.addWidget(self.edit)
#         layout.addWidget(self.pb_load)
#         layout.addWidget(self.pb_clear)
#         # connect the callbacks to the push-buttons
#         self.pb_load.clicked.connect(self.callback_pb_load)
#         self.pb_clear.clicked.connect(self.callback_pb_clear)

#     def callback_pb_load(self):
#         self.edit.append('hello world')

#     def callback_pb_clear(self):
#         self.edit.clear()
    
# def mythread():
#     print("run?")
#     app = QtWidgets.QApplication(sys.argv)
#     win = MainWindow()
#     win.show()
#     app.exec_()

# def show():
#     import threading
#     t = threading.Thread(target = mythread)
#     t.daemon = True
#     t.start()

# show()
# section

# from Tkinter import *
# import time
# import threading
# import random
# import Queue

# class GuiPart:
#     def __init__(self, master, queue, endCommand):
#         self.queue = queue
#         # Set up the GUI
#         console = Tkinter.Button(master, text='Done', command=endCommand)
#         console.pack()
#         # Add more GUI stuff here depending on your specific needs

#     def processIncoming(self):
#         """Handle all messages currently in the queue, if any."""
#         while self.queue.qsize():
#             try:
#                 msg = self.queue.get(0)
#                 # Check contents of message and do whatever is needed. As a
#                 # simple test, print it (in real life, you would
#                 # suitably update the GUI's display in a richer fashion).
#                 print(msg)
#             except Queue.Empty:
#                 # just on general principles, although we don't
#                 # expect this branch to be taken in this case
#                 pass

# class ThreadedClient:
#     """
#     Launch the main part of the GUI and the worker thread. periodicCall and
#     endApplication could reside in the GUI part, but putting them here
#     means that you have all the thread controls in a single place.
#     """
#     def __init__(self, master):
#         """
#         Start the GUI and the asynchronous threads. We are in the main
#         (original) thread of the application, which will later be used by
#         the GUI as well. We spawn a new thread for the worker (I/O).
#         """
#         self.master = master

#         # Create the queue
#         self.queue = Queue.Queue()

#         # Set up the GUI part
#         self.gui = GuiPart(master, self.queue, self.endApplication)

#         # Set up the thread to do asynchronous I/O
#         # More threads can also be created and used, if necessary
#         self.running = 1
#         self.thread1 = threading.Thread(target=self.workerThread1)
#         self.thread1.start()

#         # Start the periodic call in the GUI to check if the queue contains
#         # anything
#         self.periodicCall()

#     def periodicCall(self):
#         """
#         Check every 200 ms if there is something new in the queue.
#         """
#         self.gui.processIncoming()
#         if not self.running:
#             # This is the brutal stop of the system. You may want to do
#             # some cleanup before actually shutting it down.
#             import sys
#             sys.exit(1)
#         self.master.after(200, self.periodicCall)

#     def workerThread1(self):
#         """
#         This is where we handle the asynchronous I/O. For example, it may be
#         a 'select()'. One important thing to remember is that the thread has
#         to yield control pretty regularly, by select or otherwise.
#         """
#         while self.running:
#             # To simulate asynchronous I/O, we create a random number at
#             # random intervals. Replace the following two lines with the real
#             # thing.
#             time.sleep(rand.random() * 1.5)
#             msg = rand.random()
#             self.queue.put(msg)

#     def endApplication(self):
#         self.running = 0

# rand = random.Random()
# root = Tkinter.Tk()

# client = ThreadedClient(root)
# root.mainloop()
#!/usr/bin/python3

# import sys
# import tempfile
# import subprocess
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import QThread, pyqtSignal, QProcess

# # from mainwindow import Ui_MainWindow


# class process(QProcess):
#     signal = pyqtSignal('PyQt_PyObject')

#     def __init__(self):
#         QThread.__init__(self)
#         self.git_url = ""

#     # run method gets called when we start the thread
#     def run(self):
#         while True:
#             time.sleep(1)
#             print("process")
#             self.signal.emit("123")
#             pass
        


# class app(QtWidgets.QMainWindow):

#     def __init__(self, parent=None):
#         super(app, self).__init__(parent)
#         self.setupUi(self)
#         self.pushButton.setText("Git clone with Thread")
#         self.textEdit = QTextEdit()
#         self.textEdit.setReadOnly(True)
#         self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

#         self.closeButton = QPushButton("&Close")
#         self.closeButton.clicked.connect(self.close)

#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.textEdit)
#         self.layout.addWidget(closeButton)
#         self.setLayout(layout)

#         self.setWindowTitle("Preview")
#         # Here we are telling to call git_clone method when
#         # someone clicks on the pushButton.
#         self.pushButton.clicked.connect(self.git_clone)
#           # This is the thread object
#         # Connect the signal from the thread to the finished method
#         # self.git_thread.signal.connect(self.finished)

#     # def git_clone(self):
#     #     self.git_thread.git_url = self.lineEdit.text()  # Get the git URL
#     #     self.pushButton.setEnabled(False)  # Disables the pushButton
#     #     self.textEdit.setText("Started git clone operation.")  # Updates the UI
#     #     self.git_thread.start()  # Finally starts the thread

#     # def finished(self, result):
#     #     self.textEdit.setText("Cloned at {0}".format(result))  # Show the output to the user
#     #     self.pushButton.setEnabled(True)  # Enable the pushButton


#     def run():
#         app = QtWidgets.QApplication(sys.argv)
#         form = ExampleApp()
#         form.show()
#         app.exec_()
#         print("UI run")

# class Worker(QObject):
#     // 시그널 객체를 하나 생성합니다.
#     sig_numbers = pyqtSignal(int)

#     def __init__(self, parent=None):
#         super(self.__class__, self).__init__(parent)

#     @pyqtSlot()           // 버튼이 클릭시 시그널을 받아들이는 슬롯을 하나 마련합니다. 
#     def startWork(self):
#         _cnt = 0
#         while _cnt < 10:
#             _cnt += 1
#             self.sig_numbers.emit(_cnt) // pyqtSignal 에 숫자데이터를 넣어 보낸다
#             print(_cnt)                 // consol에서 어떻게 진행 되는지 보기 위해서 넣어준다
#             time.sleep(1)

# if __name__ == '__main__':
#     from multiprocessing import Process
#     from PyQt5.QtCore import QThread
#     app()
#     pro = process()
#     th = QThread()
#     th.moveToThread(pro)
#     th.start()



# section
# import gevent
# import random

# def task(pid):
#     """
#     Some non-deterministic task
#     """
#     gevent.sleep(random.randint(0,2))
#     print('Task', pid, 'done')

# def synchronous():
#     for i in range(1,10):
#         task(i)

# def asynchronous():
#     threads = [gevent.spawn(task, i) for i in range(0, 10)]
#     gevent.joinall(threads)

# print('Synchronous:')
# synchronous()

# print('Asynchronous:')
# asynchronous()

# import asyncio
# import random
# from Core import *
# import time



# def print_(msg):
#     print("sync")

# async def main():
#     fts = [asyncio.ensure_future(th_signal.start())]
#     print("async start")
#     while True:
#         time.sleep(1)
#         print("is main")
#         pass

# th_signal = signalThread()
# th_signal.sync.connect(print_)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()


# async def slow_operation(future):
#         await asyncio.sleep(1)
#         print("123")
#         # future.set_result('Future is done!')

# def got_result(future):
#     print(future.result())
#     # loop.stop()

# async def main():
#     loop = asyncio.get_event_loop()
#     future = asyncio.Future()
#     try:
#         loop.run_forever()
#         # while True:
#         #     print("this main")
#         #     tims.sleep(1)
#     except Exception as e:
#         print("stop")
#         loop.close()
#     finally:
#         print("end?")
#     print("2")
#     while True:
#         await asyncio.sleep(1)
#         asyncio.ensure_future(slow_operation(future))
#         pass
    # future.add_done_callback(got_result)
    

# main()
# from PyQt5.QtCore import *
# from PyQt5 import QtCore, QtGui, QtWidgets
# from threading import Thread
# import time
# import sys
# # import SyncN
# import time, os, datetime
# from PyQt5.QtCore import *
# try:
#     from Lib import Search
# except ImportError:
#     import Search

# class PrintA(QThread):
#     def __init__(self):
#         QThread.__init__(self)
#         self.running = True
#         self.isRun = False
#         self.debug = True
#         self.timestamp = 0;
#         self.cnt = 0
#         self.target = Search.PathSearcher().run()

#     def run(self):
#         while self.running:
#             if self.timestamp != os.path.getmtime(self.target):
#                 # change detected
#                 self.cnt = 0;
#                 self.timestamp = os.path.getmtime(self.target)
#                 if self.debug: print("user writting")
#             else:
#                 pass
#                 if self.cnt > 10:
#                     print("sync emit")
#                     self.sync.emit(True)
#                     self.cnt = 0;
#                 else:
#                     if self.debug: print("Wait for Sync : ", 10 - self.cnt, " sec")
#                     self.cnt +=1
#             print('A')
#             time.sleep(1)
#     def stop(self):
#         self.running = False

# class printb(QThread):
#     sync = pyqtSignal(bool)

#     def __init__(self):
#         QThread.__init__(self)
#         self.running = True
#         self.isRun = False
#         self.debug = True
#         self.timestamp = 0;
#         self.cnt = 0
#         self.target = Search.PathSearcher().run()

#     def run(self):
#         while self.running:
#             if self.timestamp != os.path.getmtime(self.target):
#                 # change detected
#                 self.cnt = 0;
#                 self.timestamp = os.path.getmtime(self.target)
#                 if self.debug: print("user writting")
#             else:
#                 pass
#                 if self.cnt > 10:
#                     print("sync emit")
#                     self.sync.emit(True)
#                     self.cnt = 0;
#                 else:
#                     if self.debug: print("Wait for Sync : ", 10 - self.cnt, " sec")
#                     self.cnt +=1
#             print('A')
#             time.sleep(1)
#     def stop(self):
#         self.running = False

    # def __init__(self, sec=0, debug=False):
    #     QThread.__init__(self)
    #     self.isRun = False
    #     self.debug = debug
    #     self.timestamp = 0;
    #     self.cnt = 0
    #     self.target = Search.PathSearcher().run()

    # # def __del__(self):
    # #     print(".... end thread.....")
    # #     self.wait()
    
    # def stop(self):
    #     if not self.isRun:
    #         print("was stopped")
    #         self.cnt = 0
    #         return
    #     else:
    #         print("real stop")
    #         self.isRun = False
    #         self.cnt = 0

    # def start(self):
    #     if self.isRun:
    #         print("already thread")
    #         self.cnt = 0
    #         return
    #     else:
    #         print("real start")
    #         self.cnt = 0
    #         self.isRun = True
    #         self.run()

    # def run(self):
    #     try:
    #         self.isRun = True
    #         while self.isRun:
    #             if self.timestamp != os.path.getmtime(self.target):
    #                 # change detected
    #                 self.cnt = 0;
    #                 self.timestamp = os.path.getmtime(self.target)
    #                 if self.debug: print("user writting")
    #             else:
    #                 if self.cnt > 10:
    #                     print("sync emit")
    #                     self.sync.emit(True)
    #                     self.cnt = 0;
    #                 else:
    #                     if self.debug: print("Wait for Sync : ", 10 - self.cnt, " sec")
    #                     self.cnt +=1
    #             print("while", self.isRun)
    #             time.sleep(2)
    #     except Exception as e:
    #         print(e)
# -------------------------------------------------------------
# a = PrintA()
# b = printb()

# a.start()
# b.start()

# app = QtWidgets.QApplication(sys.argv)
# application = SyncN.UI()
# application.show()
# sys.exit(app.exec_())

# while True:
#     print("non blokcing")
#     time.sleep(1)


# -------------------------------------------------------------
# time.sleep(10)
# a.stop()
# time.sleep(10)
# b.stop()

# section
# ----
# from multiprocessing import Process, Queue
 
# sentinel = -1
 
# def creator(data, q):
#     # // Creates data to be consumed and waits for the consumer
#     # // to finish processing
    
#     print('Creating data and putting it on the queue')
#     for item in data:
#         q.put(item)
 

# def my_consumer(q):
#     # // Consumes some data and works on it
#     # // In this case, all it does is double the input
   
#     while True:
#         data = q.get()
#         print('data found to be processed: {}'.format(data))
#         processed = data * 2
#         print(processed)
 
#         if data is sentinel:
#             break
 
# if __name__ == '__main__':
#     q = Queue()
#     data = [5, 10, 13, -1]
#     process_one = Process(target=creator, args=(data, q))
#     process_two = Process(target=my_consumer, args=(q,))
#     process_one.start()
#     process_two.start()
 
#     q.close()
#     q.join_thread()
 
#     process_one.join()
#     process_two.join()


import pika
from Lib import MQ
# def test(method):
#     print("asdasdas", method)

# channel = MQ.MQ().channel
# channel.queue_declare(test, queue='2222', passive=False, durable=False,
#                       exclusive=False, auto_delete=False, nowait=False,
#                       arguments=None)
# print(channel.makeQueue("123"))

channel = MQ.MQ().channel
#!/usr/bin/python3
import sys, os
frozen = 'not'
if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
print(getattr
print( 'we are',frozen,'frozen')
print( 'bundle dir is', bundle_dir )
print( 'sys.argv[0] is', sys.argv[0] )
print( 'sys.executable is', sys.executable )
print( 'os.getcwd is', os.getcwd() )
# channel.queue_declare(queue='ttt', durable=True, auto_delete=True)
# print(' [*] Waiting for messages. To exit press CTRL+C')

# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     time.sleep(body.count(b'.'))
#     print(" [x] Done")
#     ch.basic_ack(delivery_tag = method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
# channel.basic_consume(callback,
#                       queue='ttt')

# channel.start_consuming()

# import time

# time.sleep(10)
# method_frame, header_frame, body = channel.basic_get('test')
# if method_frame:
#     print(method_frame.message_count)
#     print(method_frame, header_frame, str(body))
#     # channel.basic_ack(method_frame.delivery_tag)
# else:
#     print('No message returned')