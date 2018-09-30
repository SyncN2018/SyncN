process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')

let amqplib = require('amqplib/callback_api');



let _con = undefined;
let _ch = undefined;
let _consume = {};
let _close = false;

const ch = {
    close: () => {
        try {
            _ch ? _ch.close() : (_con ? _con.close() : Promise.resolve(0))
            print("[channel.js] disconnected")
            _close = true;
        } catch (error) { print(e); }
        
    },
    open: () => {
        return new Promise((resolve, reject) => {
            if (_ch) {
                return _ch
            }
            let host = config.get("mq:host") || 'localhost';
            let port = config.get("mq:port") || '5672';
            let id = config.get("mq:id") || 'guest';
            let pw = config.get("mq:pw") || 'guest';
            let vhost = config.get("mq:vhost") || '/';
            let set_protocol = `amqp://${id}:${pw}@${host}:${port}/${vhost}`
            print("AMQP : "+set_protocol)
            try {
                amqplib.connect(set_protocol, (err, conn) => {
                    
                    if (err) {
                        print("[channel.js] connection disconnected")
                        _ch = undefined;
                        _con = undefined;
                        reject(0);
                    }
                    print("[channel.js] connection connecting");

                    if (!conn) { return; };
                    print("[channel.js] connection connected");
                    _con = conn;
                    
                    _con.on("close", () => {
                        ch.reopen();
                    })
                    _con.on("error", () => {
                        ch.reopen();
                    })
                    print("[channel.js] channel connecting");

                    conn.createChannel((err, channel) => {
                        if (err) {
                            print("[channel.js] channel disconnected")
                            _ch = undefined;
                            reject(0);
                        }
                        print("[channel.js] channel connectied");
                        _ch = channel;
                        resolve(channel);

                    })
                })
            } catch (e) {
                print("Error", e)
            }
            
        }).catch(e => { console.log(e) })
        
    },
    reopen: () => {
        if (!_close) { return }
        setTimeout(() => {
            ch.open().then(c => {
                _.forEach(_consume, _c => { _ch.consume(_c.queue, _c.func) })
            }).catch(e => { print(e); ch.reopen() })
        }, 1000);
    },
    publish: (target, key, payload) => {
        return _ch.publish(target, key, Buffer.from(payload));
    },
    consume: (queue, func) => {
        if(_ch) { _ch.consume(queue, func) }
    },
    send: (queue, payload, opt) => {
        print("send to " + queue)
        return _ch ? _ch.sendToQueue(queue, Buffer.from(payload), opt) : '';
    },
    ack : (msg) => { return _ch.ack(msg)},
    bind: (queue, ex, target) => { _ch.bindQueue(queue, ex, target) },
    unbind: (queue, ex, target) => { _ch.unbindQueue(queue, ex, target) },    
}

module.exports = ch;
