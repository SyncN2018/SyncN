process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')

let mq = require('lib/channel');
let ready = mq.open()

let consumer = () => {
    ready.then((ch) => {
        console.log("mail service start")
        mq.consume('c.73ff7d371f80571ed86a77726ad25330', (msg) => {
            console.log(msg)
            mq.ack(msg)
        })
    }).catch(e => {
        print(e)
    })
}

// console.log(Math.floor(Math.random() * 10000) + 1)

let amqp = require("amqplib/callback_api")
amqp.connect('amqp://6e8c67f04de5931ebd04c13f28fcdab9:41b643411948c5dbd3636ed0a54302c5@jis5376.iptime.org/syncn', function (err, conn) {
    if(err) { return console.log(err, "error") }
    conn.createChannel(function (err, ch) {
        if(err) { return console.log(err) }
        // ch.publish('msg', '', Buffer.from("test"));
        // console.log(" [x] Sent 'Hello World!'");
        ch.prefetch(1);
        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", "c.73ff7d371f80571ed86a77726ad25330");
        ch.consume("c.73ff7d371f80571ed86a77726ad25330", function(msg) {
        var secs = msg.content.toString().split('.').length - 1;

        console.log(" [x] Received %s", msg.content.toString());
        setTimeout(function() {
            console.log(" [x] Done");
            ch.ack(msg);
        }, secs * 1000);
        }, {noAck: false});
        
    
    });
});


let request = require('request');
let sendPost = () => {
    
    console.log("send post")
    request.post('http://syncn.club:9759/code/', { form : 'hdh0926@naver.com' }, (e, res, body) => {
        
        body = JSON.parse(body);
        console.log(res.statusCode, body)
        let url = 'http://syncn.club:9759/account/' + body.res;
        console.log("url : ", url)
        let auth = () => request.get(url, (e, res, body) => {
            body = JSON.parse(body);
            console.log(res.statusCode, body);
            setTimeout(auth, 3000);
        });
        auth();
    });
}

let checkQueueDebug = () => {
    const forge = require("node-forge")
    let tc1 = "hdh0926@naver.com";
    let tc2 = "wdt0818@naver.com";

    let sha256_email = forge.md.sha256.create().update(tc1).update(tc1.split("@")[0]).digest().toHex();
    console.log(sha256_email)
    let queue_name = `c.${forge.md.md5.create().update(sha256_email).digest().toHex()}`;
    console.log(queue_name)
    console.log("----------------------------------------------------")
    sha256_email = forge.md.sha256.create().update(tc2).update(tc2.split("@")[0]).digest().toHex();
    console.log(sha256_email)
    queue_name = `c.${forge.md.md5.create().update(sha256_email).digest().toHex()}`;
    console.log(queue_name)
}


let sendGet = () => {

    console.log("send get")
    request.get('http://localhost:9759/info/queue/c.73ff7d371f80571ed86a77726ad25330', (e, res, body) => {
        print(res, body)
        // body = JSON.parse(body);
        // console.log(res.statusCode, body)
        // let url = 'http://syncn.club:9759/account/' + body.res;
        // console.log("url : ", url)
        // let auth = () => request.get(url, (e, res, body) => {
        //     body = JSON.parse(body);
        //     console.log(res.statusCode, body);
        //     setTimeout(auth, 3000);
        // });
        // auth();
    });
    // setTimeout(sendGet, 2000)
}
checkQueueDebug()
// sendPost();
// consumer();
// sendGet();


// console.log(JSON.stringify({ to: "hdh0926@naver.com", html: "test" }))