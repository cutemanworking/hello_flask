# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_script import Manager, Shell
from flask_mail import Mail, Message
from threading import Thread
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)
#app.config.from_object('envcfg.raw')
#app.config['MAIL_DEBUG'] = os.environ.get('MAIL_DEBUG')
#app.config['MAIL_SUPPRESS_SEND'] = os.environ.get('MAIL_SUPPRESS_SEND')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
manager = Manager(app)
mail = Mail(app)



@app.route('/')
def index():
    msg = Message('Testing')
#    msg.sender='gandalfwong@qq.com'
    msg.recipients = ['joey_huang@aisino-wincor.com']
    msg.body = 'sended by flask-email'
    msg.html = '<b>测试Flask发送邮件<b>'
    msg.subject = 'Testing from Flask Email Program'
    with app.app_context():
         mail.send(msg)
    return '<h1>邮件发送成功</h1>'

if __name__ == '__main__':
    app.run(debug=True)