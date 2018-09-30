// SyncN Project
// auth : Fhwang in SyncN

const nodemailer = require('nodemailer');
const smtpPool = require('nodemailer-smtp-pool');
const fs = require('fs');
const auth_url = 'http://syncn.club:9759/code/'
let auth_html = '';
// smtpPool는 smtp서버를 사용하기 위한 모듈로
// transporter객체를 만드는 nodemailer의 createTransport메소드의 인자로 사용된다.
// config 정보로 바뀌어야 함
const config = {
    mailer: {
        service: 'syncn_mail',
        host: 'smtp.gmail.com',
        port: '587',
        user: 'syncn2018@gmail.com',
        password: '8102@syncn',
    },
};

const transporter = nodemailer.createTransport(smtpPool({
    service: config.mailer.service,
    host: config.mailer.host,
    port: config.mailer.port,
    auth: {
        user: config.mailer.user,
        pass: config.mailer.password,
    },
    tls: {
        rejectUnauthorize: false,
    },
    maxConnections: 10,
    maxMessages: 20,
}));

fs.readFile('mail_format/common.html', (err, data) => {
    if (err) throw err;
    common = data.toString();
});

let mail = {
    send_auth: (to, code) => {
        let tag = `<a href="${auth_url + code}" target="_blank" style="text-decoration: none; font-weight: 900; ">Click here to Verify</a>`
        const mailOptions = {
            from : 'syncn2018 < syncn2018@gmail.com >',
            to,
            subject : 'SyncN Notify auth URL(this url remove after 3 min)',
            html: common.replace(/%type%/g, "SyncN Auth Notify").replace(/%title%/g, "Need to Auth for your sync").replace(/%code1%/g, tag).replace(/%code2%/g, `then Click "Auth OK ?" on Program`),
            //text
        };

        return mail.send(mailOptions)
    },
    send : (info) => {
        if (!_.has(info, "from")) { info.from = 'syncn2018 < syncn2018@gmail.com >' }
        if (!_.has(info, "subject")) { info.subject = 'SyncN Notify' }
        if (!_.has(info, "html")) {
            info.html = common.replace(/%type%/g, "SyncN Notify").replace(/%title%/g, "Hello, Dear").replace(/%code1%/g, info.text).replace(/%code2%/g, '')
            _.omit(info, "text")
        }
            
        return new Promise((resolve, reject) => {
            transporter.sendMail(info, (err, res) => {
                if (err) {
                    console.log('failed... => ', err);
                } else {
                    print(JSON.stringify(res))
                    // need replace logger or using pm2
                }
    
                err ? resolve(false) : resolve(res);
            });
        })
        
    }
}
module.exports  = mail;
