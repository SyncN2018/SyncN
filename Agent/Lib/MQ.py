#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com

import pika, json, os, sys, time
try:
    import Setting
except ImportError:
    from Lib import Setting
class MQ():
    def __init__(self, debug=False):
        try:
            self.ack = False
            self.debug = debug
            self.channel = None
            self.retry = 0
            if self.build():
                while (self.channel == None and self.retry < 10):
                    time.sleep(1)
                    try:
                        if self.debug: print("retry connecting {0}".format(self.retry))
                        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
                        self.channel = self.connection.channel()
                        if self.debug: print("connected")
                    except Exception as e:
                        self.retry+=1
                if self.debug and (self.channel): print('PROTOCOL : '+self.url+' connected')
                if self.channel == None: sys.exit(0)
            else:
                if self.debug: print("Non-Auth")
        except Exception as e:
            print("{0} __init__, check this {0}".format(__file__, e))
        
    def build(self):
        try:
            self.config = Setting.syncn().config
            self.queue = self.config["q"]
            self.id = self.config["id"]
            self.pw = self.config["pw"]
            self.host = self.config["host"]
            self.port = self.config["port"]
            self.vhost = self.config["vhost"]
            self.url = "amqp://{0}:{1}@{2}:{3}/{4}".format(self.id, self.pw, self.host, self.port, self.vhost)
            self.rKey = self.queue
            self.ex_msg = "msg"
            self.ex_cmd = "cmd"
            return True
        except Exception as e:
            print("{0} build, check this {0}".format(__file__, e))
            return False
        
    def makeQueue(self, queue='', durable=True, auto_delete=False):
        self.channel.queue_declare(queue=queue, auto_delete=auto_delete, durable=durable)
        pass
    
    def makeExchange(self, name='', ex_type='', opt={}):
        self.channel.exchange_declare(name, ex_type, opt)
        pass

    def makeBind(self, exchange='', queue='', routing_key=''):
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
        pass

    def makeUser(self):
        # to be make when use it
        pass

    def removeQueue(self):
        # to be make when use it
        pass

    def removeExchange(self):
        # to be make when use it
        pass

    def removeBind(self, exchange='', queue=''):
        # to be make when use it
        # self.channel.queue_unbind(exchange=exchange, queue=queue)
        pass

    def removeUser(self):
        # to be make when use it
        pass
    
    
    def getChannel(self):
        return self.channel
    
    def createChannel(self):
        return self.connection.channel()
    
    def reopenChannel(self):
        self.channel = self.connection.channel()

    def publishExchange(self, exchange='', routing_key='', msg='', opt='', head={}):
        if opt: option = pika.BasicProperties( type = opt["type"], headers=head)
        else: option=''
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg, properties=option)
        if self.debug: print(" [x] publishExchange %r" % msg)
    
    def publishQueue(self, queue='', msg='', opt={}):
        if opt: option = pika.BasicProperties(type=opt["type"])
        else: option=''
        self.channel.basic_publish(routing_key=queue, exchange='', body=msg, properties=option)
        if self.debug: print(" [x] publishQueue %r" % msg)

    def get(self, queue='', isAck=True, ch=None):
        ch = ch if ch else self.connection.createChannel()
        method_frame, header_frame, body = ch.basic_get(queue)
        rs = {}
        if method_frame:
            rs["cnt"] = method_frame.message_count
            rs["msg"] = body
            if self.debug: print("get msg {0} bytes".format(len(body)))
        else:
            rs["cnt"] = -1 # this mean no msg, like nodejs indexof function

        if (isAck): ch.basic_ack(method_frame.delivery_tag)
        ch.close()
        return rs
    def worker(self, func=None, queue=''):
        if self.debug: print(' [*] start working')
        func = func if func else self.callback
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(func, queue=queue, no_ack=False)
        self.channel.start_consuming()

    def callback(serlf, ch, method, properties, msg):
            print(" [x] Received %r" % msg)
            if properties.type == "cmd":
                if properties.headers.get('host') == Setting.syncn().config["id"]:
                    # if self.debug: print(msg, properties.headers.get('host'), Setting.syncn().config["id"])
                    print("exit?")
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                else:
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                    print("Another Computer connected!!")
                    ch.cancel()
                    ch.close()
                    sys.exit(0)
                    print("sync stop")

if __name__ == '__main__':
    
    try:
        mq = MQ()
        # mq.makeQueue('test')
        # mq.makeExchange(name='test', ex_type='fanout')
        # mq.makeBind(exchange='test', queue='test')
        # mq.publishExchange(exchange='test', msg='test')
        
        # mq.publishExchange("msg", "c.6a61bb6e853cefcbb3b7de16259567c1", msg="test", opt={ "type" : "cmd" })
        mq.publishQueue(queue="mail", msg="hdh0926@naver.com", opt={ "type" : "mail" })
        print("send!!")
        # print("start consume")
        # mq.worker(queue='mail')
    except Exception as e:
        print("Error, check this {0}".format(e))
        pass
    

