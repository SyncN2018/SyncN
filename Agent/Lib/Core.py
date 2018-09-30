try:
    import Setting
    import MQ
    import NoteSql
    import Search
except ImportError:
    from Lib import Setting, MQ, NoteSql, Search, Signal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
import time
import requests


class signalThread(QThread):
    syncSignal = pyqtSignal(bool)
    
    def __init__(self, debug=False):
        super().__init__()
        self.isRun = False
        self.debug = debug
        self.target = Search.PathSearcher().run()
        self.signal = Signal.signal(debug=self.debug)
        # self.signalRunner = self.signal.connect()
        

    def __del__(self):
        if self.debug: print(".... signalThread end.....")
        self.wait()
    
    def stop(self):
        self.isRun = False
        self.signal.disconnect()
        

    def run(self):
        self.signalRunner = self.signal.connect()
        try:
            self.isRun = next(self.signalRunner)
            while self.isRun:
                if self.debug: print("get send signal from sticky note")
                self.syncSignal.emit(True)
                self.signalRunner.send(0)
                time.sleep(1)
        except Exception as e:
            self.stop()
            print("signalThread, check this {0}".format(e))

class mqSendThread(QThread):
    reciveSignal = pyqtSignal(bool)
    def __init__(self, debug=False):
        super().__init__()
        try:
            self.debug = debug
            self.type = ""
            self.DAO = NoteSql.DAO()
            
        except Exception as e:
            print("mqSendThread, check this {0}".format(e))

    def __del__(self):
        if self.debug: print(".... mqSendThread end.....")
        self.wait()
        
    def run(self):
        try: 
            ch = MQ.MQ()
            if self.type == "cmd":
                ch.publishExchange("cmd", ch.queue, 'please exit!', opt={ "type" : "exit" })
                self.type = ""
                if self.debug: print("send exit signal to another Agent")
            else:      
                ch.publishExchange("msg", ch.queue, json.dumps(self.DAO.read()))
                if self.debug: print("push : {0} {1}".format(time.time(), ch.queue))

                # fix msg cnt
                # continue msg get to until msg just 1 rest
                rs = ch.get(ch.config["q"], isAck=False, ch=ch.createChannel())
                if rs["cnt"] > 0: # 1
                    for x in range(0, rs["cnt"]):
                        temp = ch.get(ch.config["q"], ch=ch.createChannel())
                        if self.debug: print("msg cnt fix just 1, in queue cnt {0}".format(temp["cnt"]))
            
        except Exception as e:
            print("mqSendThread, check this {0}".format(e))
    
    def worker(self, ch, method, properties, msg):
        try:
            ch.basic_ack(delivery_tag = method.delivery_tag)
            ch.close()
        except Exception as e:
            print("worker, check this {0}".format(e))

class mqReciveThread(QThread):
    exitSignal = pyqtSignal(bool)
    syncSignal = pyqtSignal(bool)
    killSignal = pyqtSignal(bool)
    execSignal = pyqtSignal(bool)

    def __init__(self, debug=False):
        super().__init__()
        try:
            self.isRun = False
            self.once = False
            self.debug = True
        except Exception as e:
            print("mqReciveThread init, check this {0}".format(e))
            pass

    def __del__(self):
        print(".... mqReciveThread end.....")
        self.wait()
    
    def stop(self):
        self.isRun = False

    def run(self):
        self.isRun = True
        try:
            ch = MQ.MQ(debug=True)

            # if no msg, push now msg!!
            rs = ch.get(ch.config["q"], isAck=False, ch=ch.createChannel())

            if rs["cnt"] >= 0: # 1
                self.killSignal.emit(True)
                
                DAO = NoteSql.DAO()
                if self.once:
                    DAO.sync(json.loads(rs["msg"])["res"])["res"]
                    self.once = False
                    print("sycn when start app")
                else:
                    temp = ch.get(ch.config["q"])
                    DAO.sync(json.loads(temp["msg"])["res"])["res"]
                    print("sycn when change")
                self.execSignal.emit(True)
                print("[+] OK - sync send mail")
            else:
                print("No msg So push this msg")
                self.syncSignal.emit(True)
        except Exception as e:
            print("mqReciveThread run, check this {0}".format(e))        


    def worker(self, ch, method, properties, msg):
        try:
            if properties.type == "cmd":
                if properties.headers.get('host') == Setting.syncn().config["id"]:
                    # if self.debug: print(msg, properties.headers.get('host'), Setting.syncn().config["id"])
                    print("is me!!!!! no exit!!!!")
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                else:
                    print("Another Computer connected!!")
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                    print("is not me!!!!! exit!!!!")
                    self.exitSignal.emit(True)
            else:
                self.killSignal.emit(True)
                DAO = NoteSql.DAO()
                if DAO.sync(json.loads(msg)["res"])["res"]:
                    self.execSignal.emit(True)
                    print("[+] OK - sync send mail")

                if self.once:
                    ch.cancel()
                    ch.close()
                    self.once = False
                    print("end worker no ack so 1 msg in queue")
                    return
                else:
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                    print("ack")
        except Exception as e:
            ch.cancel()
            ch.close()
            print("worker, check this {0}".format(e))

class cmdThread(QThread):
    exitSignal = pyqtSignal(int)

    def __init__(self, debug=False):
        super().__init__()
        self.isRun = False
        self.debug = debug

    def __del__(self):
        if self.debug: print(".... cmdThread end thread.....")
        self.wait()
    
    def run(self):
        self.isRun = True
        try:
            mq = MQ.MQ(debug=True)
            name = "cmd.{0}".format(str(int(time.time())))
            mq.makeQueue(queue=name, auto_delete=True) #auto_delete=True
            mq.makeBind(exchange="cmd", queue=name, routing_key=mq.queue)
            mq.worker(self.listenCMD, name)
            print(name)
        except Exception as e:
            print("cmdThread run, check this {0}".format(e))        

    def listenCMD(self, ch, method, properties, body):
        if properties.type == "exit" : 
            self.exitSignal.emit(2)
            print("get exit signal {0}".format(time.time()))
        ch.basic_ack(delivery_tag = method.delivery_tag)

class authTimer(QThread):
    authTimerSignal = pyqtSignal(str)
    authResetSignal = pyqtSignal(bool)
    authOKSignal = pyqtSignal(bool)

    def __init__(self, debug=False):
        super().__init__()
        self.isRun = False
        self.debug = debug

    def __del__(self):
        if self.debug: print(".... cmdThread end thread.....")
        self.wait()
    
    def stop(self):
        self.isRun = False
        
    def run(self):
        try:
            self.isRun = True
            for x in range(180, 0, -1):
                if not self.isRun: print("stopped!!!!"); return
                self.authTimerSignal.emit("{0}:{1}".format(int(x/60), "{:02d}".format(int(x%60))))
                time.sleep(1)
                
            if self.isRun: self.authTimerSignal.emit("0:00")
            if self.isRun: self.authResetSignal.emit(True)
            if not self.isRun: self.authOKSignal.emit(True)
            if self.debug: print("send reset auth signal")
        except Exception as e:
            print("authTimer run, check this {0}".format(e))

if __name__ == "__main__":
    # here is test area in Qthread class
    th_mail = authTimer()
    th_mail.start()
    while 1:
        time.sleep(1)
        print("is main")