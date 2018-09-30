#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com, suck0818@gmail.com

import requests, time, json, re
try:
    from Lib.Setting import syncn
except ImportError:
    from Setting import syncn
    

class EmailCert():
    def __init__(self, debug=False):
        self.debug = debug
        self.url = ''
        self.email = ''
        self.otpCode = ''
        self.isCreateOTP = False
        self.isBuild = False
        self.sub = {
            "code" : "/code/",
            "account" : "/account/",
            "remove" : "/remove/",
        }

    def build(self, email, url):
        if self.emailChecker(email): return False
        self.url = url if url.find("://") > -1 else "http://"+url
        self.email = email
        self.otpCode = ''
        self.isBuild = True
        return True
    
    def requestAuthClear(self):
        self.otpCode = ''
        # add remove auth info server side
        print("OTP Code Clear, try createOTP")
    
    def buildClear(self):
        self.otpCode = ''
        self.email = ''
        self.url = ''
        print("Reset build, try createOTP")
    
    def emailChecker(self, email):
        regex = re.compile(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if self.debug: print("check : ", email, regex.match(email))
        return regex.match(email) == None
    
    def createOTP(self):
        try:
            otpResult = requests.post(url=self.url + self.sub['code'], data=self.email)
            if otpResult.status_code == 200:
                self.otpCode = otpResult.json()['res']
                self.isCreateOTP = True
                if self.debug:
                    print(otpResult.status_code, " : ", otpResult.json()['res'])
                return True
            else:
                print(otpResult.status_code, " : ", "Server Connection failed, Check your network!")
        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError")
        except Exception as e:
            print("${0} createOTP, check this {1}".format(__file__, e))
        return False
        

    def authOTP(self, email=''):
        try:
            authResult = requests.get(url=self.url + self.sub['account'] + self.otpCode)
            if authResult.status_code == 200:
                config = syncn()
                rs = authResult.json()['res']
                if email: rs["me"] = email
                config.writeSetting(rs)
                if self.debug: print("save setting!! ready to sync")
                if self.debug: print(authResult.text)
                return True
            else:
                print("authResult.status_code, Check your Email and verify auth URL Link")
                if self.debug: print(authResult.json()['e'])
        except Exception as e:
            print("${0} authOTP, check this {1}".format(__file__, e))
            pass
        return False
        

if __name__ == '__main__':

    client = EmailCert()
    client.build(syncn().config["service"],"hdh0926@naver.com")
    client.createOTP()
    time.sleep(60)
    client.authOTP()
