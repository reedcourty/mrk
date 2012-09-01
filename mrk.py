#!/usr/bin python
# -*- coding: UTF-8 -*-

import os
import ConfigParser

import smtplib
from email.mime.text import MIMEText

import socket

from flask import Flask, render_template, request, url_for
app = Flask(__name__)

import requests

from icy import get_title

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_PATH)

config = ConfigParser.ConfigParser()
config.read(PROJECT_PATH + '/mrk.cfg')

RADIO_URL = config.get('radio', 'url')

RADIO_TIMEOUT = config.getfloat('radio', 'timeout')

EMAIL_SUBJECT = config.get('email', 'subject')
EMAIL_FROM = config.get('email', 'from')
EMAIL_TO = config.get('email', 'to')
EMAIL_REPLYTO = config.get('email', 'replyto')
EMAIL_CC = config.get('email', 'cc')
EMAIL_BCC = config.get('email', 'bcc')
   
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
    
@app.route('/akaromacimet', methods=['POST', 'GET'])
def akarom():  
    title = get_title(RADIO_URL, RADIO_TIMEOUT)
    link = "https://www.youtube.com/results?search_type=&search_query={0}".format(title.replace(" ", "%20"))
    if request.method == 'POST':
        send_mail(title)
        return render_template('akaromacimet.html', title=title, link=link,
            mail=u"Elvileg elment a levél.")
    return render_template('akaromacimet.html', title=title, link=link, mail=None)    
    
@app.errorhandler(404)
def error404(error):
    return "Szerintem eltévedtél..."  

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")