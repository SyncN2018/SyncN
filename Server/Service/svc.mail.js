process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
let mq = require('lib/channel');
let mail = require('lib/sendmail');

mq.open().then((ch) => {
    console.log("Mail service start")
    ch.consume('mail', async msg => {
        if (msg.properties.type == "mail") {
            print(msg.content.toString())
            rs = await mail.send(JSON.parse(msg.content.toString()))
        } else {
            // rs = await mail.send(msg.properties.headers.to, msg.properties.headers.title)
            print("not support this type, this option prepare soon")
        }
        mq.ack(msg)
    })
}).catch(e => {
    print(e)
})