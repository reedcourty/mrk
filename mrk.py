#!/usr/bin python
# -*- coding: UTF-8 -*-

import os
import ConfigParser

import smtplib
from email.mime.text import MIMEText

from flask import Flask
app = Flask(__name__)

import requests

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_PATH)

config = ConfigParser.ConfigParser()
config.read(PROJECT_PATH + '/mrk.cfg')

RADIO_URL = config.get('radio', 'url')

EMAIL_SUBJECT = config.get('email', 'subject')
EMAIL_FROM = config.get('email', 'from')
EMAIL_TO = config.get('email', 'to')
EMAIL_REPLYTO = config.get('email', 'replyto')
EMAIL_CC = config.get('email', 'cc')
EMAIL_BCC = config.get('email', 'bcc')

def get_title(url):
    title = "Sajnos nem tudom most ezt megmondani neked. :("
    r = requests.get(url, headers={'Icy-MetaData':'1'}, prefetch=False, 
        timeout=0.05)
    interval = r.headers['icy-metaint']
    r.raw.read(int(interval))
    len = ord(r.raw.read(1))*16
    stream_title = r.raw.read(len)
    title = stream_title.split("'")[1]
    return title
    
def send_mail(title):

    m = """
    {0}
    
    https://www.youtube.com/results?search_type=&search_query={1}
    
    """.format(title, title.replace(" ", "%20"))

    print m

    msg = MIMEText(m, _charset="UTF-8")
    
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['Reply-to'] = EMAIL_REPLYTO
    msg['To'] = EMAIL_TO
    msg['Cc'] = EMAIL_CC
    msg['Bcc'] = EMAIL_BCC
    
    s = smtplib.SMTP()
    s.connect("localhost")
    s.sendmail(EMAIL_FROM, [EMAIL_TO, EMAIL_CC, EMAIL_BCC], msg.as_string())
    s.close()
    
@app.route('/')
def index():
    return(u'Most akarsz is valamit, vagy csak kóstolgatsz?')
    
@app.route('/akaromacimet')
def akarom():  
    title = get_title(RADIO_URL)
    print(title)
    
    send_mail(title)
    return "{0}".format(title)
    
@app.route('/neznem')
def neznem():
    title = get_title(RADIO_URL)
    print(title)
    
    return "Jelenleg az MR2-n ez a szám megy: {0}".format(title)
    
@app.errorhandler(404)
def error404(error):
    return "Szerintem eltévedtél..."  

if __name__ == '__main__':
    app.debug = True
    app.run()