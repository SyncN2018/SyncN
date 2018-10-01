


# SyncN!
**Sticy Note**를 사용하면서 icloud의 동기화가 부러웠던 적이 있으세요?? **SyncN**을 써보세요!!

 * 언제 어디서나 기록한 메모를 볼 수 있습니다.
 * 기존에 사용하던 이메일로 로그인 하세요. 따로 회원가입이 필요 없습니다.
 * 더 이상 번거로운 프로그램을 사용하지 마세요. 간편한 “SyncN”으로 Sticky Note를 100% 활용해보세요

## 목차


 >[1. 사용법](https://github.com/Fhwang0926/syncn_v1/blob/master/README.MD#%EC%82%AC%EC%9A%A9%EB%B2%95)  
 >
 >[2. 설치](https://github.com/Fhwang0926/syncn_v1#%EC%84%A4%EC%B9%98)
 >
>[3. 장점](https://github.com/Fhwang0926/syncn_v1#%EC%9E%A5%EC%A0%90)
>
>[4. 발전가능성](https://github.com/Fhwang0926/syncn_v1#%EB%B0%9C%EC%A0%84-%EA%B0%80%EB%8A%A5%EC%84%B1)
>
>[5. 개발 환경]( https://github.com/Fhwang0926/syncn_v1#%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD)
>
 >[6 데모](https://github.com/Fhwang0926/syncn_v1#%EB%8D%B0%EB%AA%A8)
 


## 사용법

### 1. 설치
----
**SyncN**은 별도 웹페이지에 설치 파일을 제공하고 있습니다.

>* 아래 첨부된 파일을 다운받으세요 & 아래 링크를 클릭하세요
>
>* 프로그램을 다운 받아주세요 (기본 설치 경로는 ProgramFile 입니다)

url입력칸 & exe파일 첨부 칸



### 2. 인증
----
**SyncN**은 여러분이 가지고 있는 이메일을 통해 인증이 가능합니다. 입력창에 이메일을 입력하면 인증 URL이 메일로 발송됩니다. 그리고 그 링크를 클릭하기만 하면 인증이 완료됩니다. 인증이 끝나면 서버와 연결할 수 있는 설정파일(Setting.syncn)이 생겨요!

>* 설치된 **Syncn**을 실행합니다.
>
>* 입력창에 여러분의 Email을 입력해주세요 ex) abc@gmail.com
>* 입력한 이메일의 수신함을 확인해주세요.
>* 받은 메일안의 URL을 클릭해주세요.(※이메일을 입력 후 3분안에 클릭해야 합니다.)
>* "Auth Successfully"라는 팝업창이 뜹니다. 확인을 눌러주세요
>* **Syncn**프로그램으로 돌아가 "OK"버튼을 눌러주세요.

<img src="https://github.com/Fhwang0926/syncn_v1/blob/master/Image/EmailWrite.gif" width="30%"></img> 
<img src="https://github.com/Fhwang0926/syncn_v1/blob/master/Image/EmailAuth.gif" width="60%" height="400"></img>


### 3. 동기화
----
[인증](https://github.com/Fhwang0926/syncn_v1#2-인증) 절차가 끝났다면 여러분은 평상시처럼 **Sticy Note**를 이용하면 됩니다. **SyncN**은 백그라운드에서 자동으로 실행됩니다. 만약 동기화를 멈추고 싶다면 트레이 아이콘에서 설정할 수 있어요.

>* 동기화를 원하는 컴퓨터에도 **SyncN** 프로그램이 [설치](http://www.test.com)해 주세요. 
>
>*  **SyncN**을 처음 설치하는 컴퓨터일 경우 Email[인증](https://github.com/Fhwang0926/syncn_v1#2-인증) 절차를 진행해 주셔야 합니다.
>* **SyncN**이 설치되어 있고 Email[인증](https://github.com/Fhwang0926/syncn_v1#2-인증)이 끝난 PC라면 이전과 같이 **Sticy Note**를 사용하시면 됩니다~

트레이 아이콘 동기화 옵션 gif파일 첨부 칸

## 설치

Server Side

1. Rabbit MQ 설치
```bash
# we need to install erlang for dependencies
$ sudo apt-get install -y erlang logrotate
$ sudo apt-get -f install

# Download latest version of rabbitmq-server.deb
$ wget https://github.com/rabbitmq/rabbitmq-$ server/releases/download/rabbitmq_v3_6_10/rabbitmq-server_3.6.10-1_all.deb
$ sudo dpkg -i rabbitmq-server_3.6.10-1_all.deb
$ sudo apt install rabbitmq-server
```

2. Rabbit MQ 설정
```bash
# Plugin enable
$ sudo rabbitmq-plugins enable rabbitmq_management
# Make user
$ sudo rabbitmqctl add_user [newuser] [password]
# Grant authority
$ sudo rabbitmqctl set_user_tags [newuser] administrator
$ sudo rabbitmqctl set_permissions -p / [newuser] ".*" ".*" ".*"
```

3. Rabbit MQ 접속
```url
# Web default port is 15672
# Data default port is 5672

http://localhost:15672
```
<img src="https://github.com/Fhwang0926/syncn_v1/blob/master/Image/RabbitMq%20Enter.gif" width="60%"></img> 

만약 설치에 어려움이 있다면 운영체제에 맞게 공식 웹사이트 설치 가이드를 따라하시면 좋을 것 같습니다
http://www.rabbitmq.com/#getstarted


## 장점
>* DB가 필요없습니다!
>
>* 사용법이 간단합니다!
>
>* 기존에 쓰던 프로그램을 사용합니다!


## 발전 가능성
글로벌 시대가 도래하면서, 최근 2대 이상의 PC로 작업을 하는 사용자들이 상당히 많아졌습니다. 그에 따라 효율적인 생산성을 위해 클라우드 서비스를 이용하는 사람 또한 급증하고 있습니다.  저희는 간편한 동기화에 초점을 맞춰 프로그램을 개발중입니다.
>* ### 범용성
>> **SyncN**은 Sticy Note라는 윈도우 내장 프로그램에 초점을 맞춰 개발한 소프트웨어지만 동기화가 필요한 다른 프로그램에도 언제든지 가져다 쓸 수 있도록 미들웨어 개념의 소프트웨어로 개발할 것입니다.
>
>* ### 확장성
>> 다수의 유저가 동시에 작업을 할 때, 병목현상을 고려하여 MQ(MessageQueue)를 사용해 서버를 구성했습니다. 지금은 1대 1 동기화에 초점을 맞췄지만, 추후 n대n 동기화가 가능하도록 업데이트 할 것입니다.
>
>* ### 다양성
>> 윈도우 뿐만 아니라 리눅스, MacOS 등 다양한 운영체제에서도 호환이 가능하도록 개발 할 것입니다.


## 개발환경
>* [Python 3.6.6](https://www.python.org/downloads/release/python-366)
>* [RabbitMQ 3.6.10](https://www.rabbitmq.com/)
>
>* [Erlang 19.2.1](https://www.erlang.org/)
>* [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
>* [PyCharm Community 2018](https://www.jetbrains.com/pycharm/download/#section=windows)
>* [PyQt5 Designer](https://www.jetbrains.com/pycharm/download/#section=windows) 

## 데모
*[Demo Link](https://www.youtube.com/watch?v=6jfhkHdDLSg&feature=youtu.be)


[![demo](https://i.ytimg.com/vi/6jfhkHdDLSg/maxresdefault.jpg)](https://www.youtube.com/watch?v=6jfhkHdDLSg&feature=youtu.be)

