process.chdir(__dirname);
require('app-module-path').addPath(__dirname);
require('lib/common')
const moment = require('moment')

const fs = require('fs')
const mq = require('lib/channel');
const mail = require('lib/sendmail');
const forge = require('node-forge')
const rabbit = require('axios').create({
    baseURL: `http://${config.get('mq:host')}:${config.get('mq:api_port')}/api`,
    timeout : 3000,
    auth: { username: config.get('mq:id'), password: config.get('mq:pw') }
})

const regx = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,5}$/i;
let auth = {}
let auth_link = '';
const auth_exfire = 60 * 3; // expire 3 min

fs.readFile('mail_format/auth_link.html', (err, data) => {
    if (err) throw err;
    auth_link = data.toString();

});
// has bug not expired
let auth_cleaner = () => {
    console.log('auth cleaner running, client cnt : ', _.keys(auth).length, _.keys(auth))
    _.forEach(_.keys(auth), key => {
        console.log("check\n"+auth[key].expire+" - "+moment(auth[key].expire).format("YYYY-MM-DD hh:mm:ss")+"\n"+timestamp()+" - "+moment().format("YYYY-MM-DD hh:mm:ss"))
        if (auth[key].expire < timestamp() || auth[key].status ) { auth = _.omit(auth, [key]) }
    })
    setTimeout(() => {
        auth_cleaner()
    }, 3000 );
}

let auth_generator = (email) => {
    let sha256_email = forge.md.sha256.create().update(email).update(email.split("@")[0]).digest().toHex();
    let queue_name = `c.${forge.md.md5.create().update(sha256_email).digest().toHex()}`;
    let id = forge.md.md5.create().update(queue_name+timestamp()).digest().toHex();
    let pw = forge.md.md5.create().update(sha256_email + timestamp()).digest().toHex();
    let otp = forge.md.md5.create().update(email).update(timestamp()).digest().toHex()
    auth[otp] = { status: false, expire: timestamp() + auth_exfire, info: { q: queue_name, id: id, pw: pw }} // expire 5 min
    print("auth gen ok", otp);
    return otp;
}

let post = (req, res) => {
    let data = '';
    
    req.on('data', (raw) => {
        data += raw.toString();
    });

    req.on('socket', (s) => {
        s.setTimeout(3);
        s.on('timeout', () => {
            req.abort();
        });
    })

    req.on('end', () => {
        try {
            let email = data.match(regx)[0];
            if (email == null) { return; }
            
            let otp = auth_generator(email);
            mail.send_auth(email, otp)

            
            res.on('error', (e) => {
                throw e
            });
            
            res.writeHead(200, {'Content-Type': 'application/json'})
            res.end(JSON.stringify(_.assign(_.pick(req, ['headers', 'method', 'url']), { res : 'ok.'+otp })))


        } catch (e) {
            console.log(e)
            res.writeHead(404);
            res.end();
        }
        
    });
}

let get = async (req, res) => {
    try {
        let code = req.url.split("/");
        // using email auth
        if (code[1] == 'code') { // md5
            if (_.has(auth, code[2])) {
                res.writeHead(200); res.write(auth_link.replace(/%script%/, `alert("Auth Successful"); window.close();`));
                auth[code[2]].status = true;
                auth['ok.' + code[2]] = { info: auth[code[2]].info, status: false, expire: timestamp() + auth_exfire } // expire 3 min
                
                console.log(auth['ok.' + code[2]])
            } else {
                res.writeHead(404);
                res.write(auth_link.replace(/%script%/, `alert("Expired this URL, Restart SyncN program and again auth"); window.close();`));
            }
        }
        // using account create
        if (code[1] == 'account') { // ok.md5
            if (_.has(auth, code[2])) {
                const vhost = config.get('mq:vhost');
                let service = `${config.get('service:protocol')}://${config.get('service:host')}:${config.get('service:port')}`
                print(service)
                let info = { version: config.get("c-version"), host: config.get("mq:host"), port: config.get("mq:port"), vhost : vhost, service : service }
                let account = _.assign(auth[code[2]].info, info);
                print("auth!!!!!, " + code[2], JSON.stringify(account))
                
                // 큐 생성 및 exchange, cmd 바인딩
                rabbit.get(`/queues/${vhost}`).then(async rs => {
                    let q_list = _.map(rs.data, r => r.name)
                    if(_.find(q_list, account.q)) { return; }
                    await rabbit.put(`/users/${account.id}`, { password: account.pw, tags : 'None' }).then(() =>{
                        rabbit.put(`/permissions/${vhost}/${account.id}`, {
                            configure: '(cmd.*)',
                            write: `(${account.q}|msg|mail|cmd|amq.default|^cmd.*)`,
                            read: `(${account.q}|msg|mail|cmd|^cmd.*|amq.*)`,
                        }).catch(e => print("UP", e))
                    })
                    .then(() => rabbit.put(`/queues/${vhost}/${account.q}`, { "autoDelete" : false, "durable" : true }).catch(e => print("Q", e)))
                    .then(() => rabbit.post(`/bindings/${vhost}/e/msg/q/${account.q}`, {"routing_key":account.q }).catch(e => print("B1", e)))
                    .catch((e) => { console.log(e); throw new Error('MQ error'); })
                })
                
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.write(JSON.stringify({ res: account }));
                auth[code[2]].status = true;
            } else {
                res.writeHead(404, { 'Content-Type': 'application/json' });
                res.write(JSON.stringify({ e: "Check Email auth URL, Or maybe it was expireded" }));
            }
        }
        // using agent update
        if (code[1] == 'update') { // update
            //get version and compress given new version
            notice = "not ready update link"
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.write(JSON.stringify({ res: notice }));
        }
        res.end();  
    } catch (e) {
        console.log(e)
        res.writeHead(404);
        res.end();
    }
    
    req.on('socket', (s) => {
        s.setTimeout(3);
        s.on('timeout', () => {
            req.abort();
        });
    })
}
// account remove
let remove = async (req, res) => {
    try {
        let code = req.url.split("/");
        if (code[1] == 'account') { // ok.md5
                await rabbit.delete(`/bindings/${config.get('mq:vhost')}/e/msg/q/${info.q}/`) // it maybe will remove code
                await rabbit.delete(`/bindings/${config.get('mq:vhost')}/e/cmd/q/${info.q}/`)
                await rabbit.delete(`/queues/${config.get('mq:vhost')}/${info.q}`) // delete queue
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.write(JSON.stringify({ res: "OK" }));
        } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.write(JSON.stringify({ e: "URL Request failed" }));
        }
        
    } catch (e) {
        console.log(e)
        res.writeHead(404);
        res.write(JSON.stringify({ e : 'MQ error' }));
    }
    res.end();
    req.on('socket', (s) => {
        s.setTimeout(3);
        s.on('timeout', () => {
            req.abort();
        });
    })
}

mq.open().then((ch) => {
    let http = require('http');
    let service = http.createServer('/', (req, res) => {
        switch (req.method) {
            case 'POST':
                post(req, res);
                break;

            case 'GET':
                get(req, res);
                break;

            case 'DELETE':
                remove(req, res);
                break;

            default:
                print("check attacking using http")
                mq.send("mail", '', { type: "notice", headers: { to: config.get('manager') } }) // using cmd
                break;
        }
    });
    service.listen(9759);
    auth_cleaner();
}).catch(e => {
    print(e)
})

// auth from agents