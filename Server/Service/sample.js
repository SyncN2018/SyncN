// Copyright(c) 2018. F1Security.co.kr
// by Yourim Yi <yi@f1security.co.kr>
// Date : 2018-03-29

'use strict';

const amqp = require('amqplib');
const uuid = require('uuid');

let _con = undefined; // connection
let _ch = undefined; // channel
let _temp_ch = undefined; // channel
let _close = false;
let _reopen = 0;
let userId = '';

let _consume = {};
// const add_consume = (tag, queue, func, opt) => {
// 	_consume[tag] = {
// 		tag: tag,
// 		queue: queue,
// 		func: func,
// 		opt: opt
// 	};
// 	return tag;
// }
// const remove_consume = (tag) => delete _consume[tag];

let _listen = {};
const add_listen = (target, tag, func) => _listen[`${target}:${tag}`] = { target: target, tag: tag, func: func};

// Connect to AMQP Server
const channel = {
	close : () => {
		_close = true;
		if(_.isEmpty(_ch)) { return Promise.resolve(true); }
		console.log('[channel.js] mq server disconnecting.');
		return _ch.close().then(() => {
			if(_.isEmpty(_con)) { return Promise.resolve(true); }
			return _con.close().then(() => {
				console.log('[channel.js] mq server disconnected.');
				_con = undefined;
			}, console.warn);
			_ch = undefined;
		}, console.warn);
	},
	reopen: () => {
		if(!_close) {
			setTimeout(() => {
				_reopen++;
				console.log(`[channel.js] mq server disconnected. reconnect(${_reopen}).`);
				channel.open().then(c => {
					_.forEach(_consume, v => channel.consume(v.queue, v.func, v.opt));
					_.forEach(_listen, v => channel.listen(v.target, v.tag, v.func));
				}).catch(e => channel.reopen());
			}, 1000);
		}
	},
	open : () => {
		let user = userId = _config_.get('mq:user');
		let pass = _config_.get('mq:pass');
		if(!_.isEmpty(_ch)) { return Promise.resolve(channel); }
		console.log('[channel.js] mq server connecting.');
		let host = _config_.get('mq:host'), vhost = _config_.get('mq:vhost');
		let amqp_connection_string = `amqp://${user}:${pass}@${host}/${vhost}`;
		return amqp.connect(amqp_connection_string)
			.then((conn) => {
				conn.on('close', (e) => {
					console.log('[channel.js] mq server disconnected.');
					_ch = null; _con = null; _temp_ch = null;
					channel.reopen();
				});

				_con = conn;
				conn.on('error', handle => {
					console.log('[channel.js] mq server error.');
					// channel.reopen();
				});
				console.log('[channel.js] mq server connected.');
				channel.openTempChannel(); // sacrifice channel...
				return conn.createChannel().then((ch) => {
					ch.prefetch(1);
					_ch = ch;
					return channel;
				});
			})
			.catch((err) => {
				console.error('[channel.js] mq server connect fail.', _reopen++);
				try { if(_ch) { _ch.close(); _ch = undefined; } } catch(e) {}
				try { if(_con) { _con.close(); } _con = undefined; } catch(e) {}
				return new Promise((resolve, reject) => {
					setTimeout(() => channel.open().then(resolve), 100);
				});
			})
		;
	},
	// getChannel : () => { return _ch; },
	// openTempChannel : () => {
	// 	if(_temp_ch != null) { return Promise.resolve(_temp_ch); }
	// 	return _con.createChannel().then(ch => {
	// 		ch.on('error', e => { console.log('x'); _temp_ch = undefined; channel.openTempChannel(); });
	// 		return _temp_ch = ch;
	// 	});
	// },
	// ack : (msg) => _ch ? _ch.ack(msg) : Promise.reject(0),
	// send : (q, payload, opt) => _ch ? Promise.resolve(_ch.sendToQueue(q, Buffer.from(payload), _.assign({ persistent: true, userId: userId }, opt))) : Promise.reject(0),
	// publish : (target, key, payload, opt) => _ch ? Promise.resolve(_ch.publish(target, key, Buffer.from(payload), _.assign({ persistent: true, userId: userId }, opt))) : Promise.reject(0),

  // RPC
  // prepare : (func, ack = false) => {
  //   return _ch ? channel.createQueue('', { exclusive : true }).then((rq) => {
  //     return channel.consume(rq.queue, func, { noAck : ack }).then((cq) => { return rq.queue; });
  //   }) : Promise.reject(0);
  // },
  // dismiss : (rq) => _ch.deleteQueue(rq),
  // rpc : (q, rq, corr, payload, opt, ttl = 15000) => channel.send(q, payload, _.assign({ correlationId : corr, replyTo : rq }, opt)),

  // RPC reply
  // reply : (msg, payload, opt) => channel.send(msg.properties.replyTo, payload, _.assign(_.omit(msg.properties, 'userId'), opt)),

  // Instant RPC
  // ask : (q, payload, opt, ttl = 15000) => {
  //   let uid = uuid();
  //   if(!_ch) { return Promise.reject(0); }
  //   return new Promise((resolve, reject) => {
  //     if(!_ch) { return reject(0); }
  //     channel.createQueue('', { exclusive : true })
  //       .then((rq) => {
  //         if(!_ch) { return reject(0); }
  //         let func = () => { reject('timeout'); if(_ch) { _ch.deleteQueue(rq.queue); } }
  //         let func_timer = setTimeout(func, ttl || 60000); // MAX
  //         let corr = uuid();
  //         channel.consume(rq.queue, (msg) => {
  //           if(msg && msg.properties.correlationId == corr) {
  //           	func = () => {};
  //           	clearTimeout(func_timer);
  //             resolve(msg);
  //             if(_ch) { _ch.deleteQueue(rq.queue); } // will cause unconsume
  //           }
  //         }, {noAck : true})
  //         .then(() => {
  //           return channel.send(q, payload, _.assign({ correlationId : corr, replyTo : rq.queue, expiration : ttl || 60000 }, opt));
  //         })
  //         .catch(reject);
  //       });
  //   });
  // },
	// checkExchange : (queue) => _ch ? channel.openTempChannel().then(ch => ch.checkExchange(queue)) : Promise.reject(0),
	// createExchange : (ex, type, opt) => _ch ? channel.openTempChannel().then(ch => ch.assertExchange(ex, type, opt)) : Promise.reject(0),
	// deleteExchange : (ex) => _ch ? channel.openTempChannel().then(ch => ch.deleteExchange(ex)) : Promise.reject(0),

	// checkQueue : (queue) => _ch ? channel.openTempChannel().then(ch => ch.checkQueue(queue)) : Promise.reject(0),
	// createQueue : (queue, opt) => _ch ? channel.openTempChannel().then(ch => ch.assertQueue(queue, opt)) : Promise.reject(0),
	// deleteQueue : (queue) => _ch ? channel.openTempChannel().then(ch => ch.deleteQueue(queue)) : Promise.reject(0),

  // bind : (queue, ex, target) => _ch ? _ch.bindQueue(queue, ex, target) : Promise.reject(0),
  // unbind : (queue, ex, target) => _ch ? _ch.unbindQueue(queue, ex, target) : Promise.reject(0),

	// consume : (queue, func, opt) => _ch ? _ch.consume(queue, func, opt).then(q => add_consume(q.consumerTag, queue, func, opt)) : Promise.reject(0),
  // cancel : (tag) => _ch ? _ch.cancel(tag).then(tag => remove_consume(tag)) : Promise.reject(0),

	// channel
	// listen : (target, tag, func) => {
	// 	if(!_ch) { return Promise.reject(0); }
	// 	return new Promise((resolve, reject) => {
  //     if(!_ch) { return reject(0); }
	// 		channel.createQueue('', { exclusive : true })
	// 			.then((q) => {
  //         if(!_ch) { return reject(0); }
	// 				_ch.bindQueue(q.queue, target, tag);
	// 				_ch.consume(q.queue, func, { noAck : true });
	// 				add_listen(target, tag, func);
  //         return q.queue;
	// 			})
	// 			.then(resolve);
	// 		;
	// 	})
	// },
};

module.exports = channel;