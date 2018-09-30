#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com, suck0818@gmail.com

import time, os, datetime
from PyQt5.QtCore import *
try:
    from Lib import Search
except ImportError:
    import Search

class signal(object):

    def __init__(self, debug=False):
        object.__init__(self)
        self.isRun = False
        self.debug = debug
        self.target = Search.PathSearcher().run()
        self.timestamp = os.path.getmtime(self.target);
        self.cnt = 0
        self.isSended = True

    def disconnect(self):
        self.isRun = False
        self.cnt = 0

    def connect(self):
        try:
            self.cnt = 0
            self.isRun = True
            while self.isRun:
                time.sleep(1)
                if self.timestamp != os.path.getmtime(self.target): # change detected
                    self.cnt = 0;
                    self.timestamp = os.path.getmtime(self.target)
                    self.isSended = False
                    if self.debug: print("user writting")
                        
                else:
                    if self.cnt > 5: 
                        self.cnt = yield True # send signal coroutine
                        self.isSended = True
                        if self.debug: print("sync emit", self.cnt)
                    else:
                        if self.isSended:
                            # if self.debug: print("continue")
                            continue
                        if self.debug: print("Wait for Sync : ", 5 - self.cnt, " sec")
                        self.cnt +=1
                
        except Exception as e:
            self.stop()
            self.join()
            print("Error, check this {0}".format(e))

if __name__ == "__main__":
    sig = signal(debug=True)
    runner =  sig.connect()
    isRun = next(runner)
    while isRun:
        runner.send(0)
        time.sleep(1)
        print("done!")


        