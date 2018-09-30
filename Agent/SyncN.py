from Lib import Core, UI, Setting, Auth, NoteSql, Search
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import os
import requests
import json
import subprocess
import os, sys
from win32com.client import GetObject as scanProcess
 
class SyncN(object):
    def __init__(self):
        super().__init__()
        # init
        self.debug = True
        self.checkProcessMe()
        self.app = QtWidgets.QApplication(sys.argv)
        # init UI
        self.UI = UI.UI()
        if os.path.exists(Setting.syncn().path):
            self.UI.authStyle()
        #init auth
        self.OTP = Auth.EmailCert(debug=True)
        # init signal
        self.th_signal = Core.signalThread(debug=True)
        # init MQ
        self.th_mqSender = Core.mqSendThread(debug=True)
        # init MQ
        self.th_mqReciver = Core.mqReciveThread(debug=True)
        # init CMD
        self.th_cmd = Core.cmdThread(debug=True)
        # init mail
        # self.th_mail = Core.mailThread(debug=True)
        # init authTimer
        self.th_authTimer = Core.authTimer(debug=True)
        # init target
        target = Search.PathSearcher()
        target.run()
        target = target.findPath.split("\\")
        self.target = target[len(target)-2].split("_")[1]
        
        # init func
        self.connectInterface()
        
    
    def connectInterface(self):
        #define UI
        self.UI.tray.accountAction.triggered.connect(self.UI.windowTrigger)
        self.UI.tray.activated.connect(self.UI.openWindow)
        self.UI.tray.exitAction.triggered.connect(self.proExit)
        self.UI.tray.syncAction.triggered.connect(self.sycnTrigger)
        self.UI.input_info.textChanged.connect(self.UI.checkInput)
        self.UI.btn_close.clicked.connect(self.proExit)
        self.UI.btn_tray.clicked.connect(self.UI.windowTrigger)

        #define here
        self.UI.input_info.returnPressed.connect(self.proAuth)
        self.UI.btn_ok.clicked.connect(self.proAuth)
        self.UI.tray.logoutAction.triggered.connect(self.proLogout)
        if self.debug: print("[+] Registration Interface")

    def setThreadChannel(self):
        self.th_signal.syncSignal.connect(self.th_mqSender.start)
        self.th_mqReciver.exitSignal.connect(self.proExit)
        self.th_mqReciver.syncSignal.connect(self.th_mqSender.start)
        self.th_mqReciver.execSignal.connect(self.openNote)
        self.th_mqReciver.killSignal.connect(self.closeNote)
        self.th_cmd.exitSignal.connect(lambda n:self.proExit(code=n))
        self.th_authTimer.authResetSignal.connect(self.authReset)
        self.th_authTimer.authTimerSignal.connect(lambda strTime:self.UI.l_info.setText("We Sended Auth mail\n{0}".format(strTime)))
        self.th_authTimer.authOKSignal.connect(self.UI.authStyle)
    
    def authReset(self):
        self.OTP.buildClear()
        self.UI.l_info.setText("Typing Your E-mail")
        self.UI.l_info.setStyleSheet("color:black;\n")
        self.UI.btn_ok.setText("OK")
        self.OTP.isCreateOTP = False

    def sycnTrigger(self):
        if self.th_signal.isRun:
            self.th_signal.stop()
            print("sycn stop")
        else:
            self.th_signal.start()
            print("sycn start")
    
    def proExit(self, code=0):
        if code == 2:
            self.sycnTrigger()
            self.UI.windowTrigger()
            self.UI.msg(msg="Sync Stop!!\n\nAnother PC login")
        else:
            if self.th_signal.isRunning(): self.th_cmd.terminate()
            if self.th_cmd.isRunning(): self.th_cmd.terminate()
            if self.th_mqSender.isRunning(): self.th_cmd.terminate()
            if self.th_mqReciver.isRunning(): self.th_cmd.terminate()
        self.UI.close()
        sys.exit(code)

    def run(self):
        self.closeNote()
        self.setThreadChannel()
        if self.UI.auth:
            self.disconnectCMD()
            self.th_mqReciver.once = True
            self.th_mqReciver.start()
            self.th_signal.start()
        self.UI.show()
        if self.UI.auth:
            self.UI.windowTrigger()
        self.proExit(self.app.exec_())
    
    def proAuth(self):
        if self.UI.auth: return self.UI.windowTrigger()
        if not self.OTP.isCreateOTP:
            # need create OTP
            if not self.OTP.build(self.UI.input_info.text(), "syncn.club:9759"):
                self.UI.l_info.setText("Check Email Address\n%")
                self.UI.l_info.setStyleSheet("color:red;\n")
                return
            else:
                if self.OTP.createOTP():
                    self.UI.l_info.setStyleSheet("color:green;\n")
                    self.UI.l_info.setText("We Sended Auth mail")
                    self.UI.btn_ok.setText("Auth OK ?")
                    self.th_authTimer.start()
                else:
                    self.UI.l_info.setStyleSheet("color:red;")
                    self.UI.l_info.setText("Failed send Auth email")
        else:
            # need auth OTP
            if self.OTP.authOTP(self.UI.input_info.text()):
                self.th_authTimer.stop()
                self.th_authTimer.wait()
                self.UI.authStyle()
                self.disconnectCMD()
                self.th_mqReciver.once = True
                self.th_mqReciver.start()
                self.th_signal.start()
            else:
                self.UI.l_info.setStyleSheet("color:red;\n")
                self.UI.l_info.setText("Auth Failed, see email")
    
    def openNote(self):
        subprocess.call("explorer.exe shell:appsFolder\Microsoft.MicrosoftStickyNotes_{0}!App".format(self.target), creationflags=0x08000000)
    
    def closeNote(self):
        subprocess.call('taskkill /f /im Microsoft.Notes.exe', creationflags=0x08000000)
        subprocess.call('taskkill /f /im Microsoft.StickyNotes.exe', creationflags=0x08000000)

    def proLogout(self):
        try:
            os.remove(self.UI.syncn["config"])
        except Exception as e:
            print("{0} proLogout, check this {0}".format(__file__, e))
        finally:
            sys.exit(0)

    # excute others agent disconnect all then only connect me
    def disconnectCMD(self):
        try:
            self.th_mqSender.type = "cmd"
            self.th_mqSender.start()
            self.th_cmd.start()
        except Exception as e:
            print("{0} disconnectCMD, check this {1}".format(__file__, e))
            pass
    
    def checkProcessMe(self):
        psAll = scanProcess('winmgmts:').InstancesOf('Win32_Process')
        me = os.path.basename(__file__)
        
        for ps in psAll:
            if self.debug: print(me, ps.Properties_('Name').Value)
            if me == ps.Properties_('Name').Value:
                if self.debug: print("Same Process is running, me is exit!")
                sys.exit(0)
        else:
            print("No process, me is run!")
        

if __name__ == '__main__':
    main = SyncN()
    main.run()
    # main.checkProcessMe()