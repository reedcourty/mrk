#!/usr/bin python
# -*- coding: UTF-8 -*-

import os
import ConfigParser

import smtplib
from email.mime.text import MIMEText

from bottle import route, error, default_app, debug

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_PATH)

config = ConfigParser.ConfigParser()
config.read(PROJECT_PATH + '/mrk.cfg')

EMAIL_FROM = config.get('email', 'from')
EMAIL_TO = config.get('email', 'to')

debug(True)
    
def send_mail(title):

    m = """
    {0}
    
    https://www.youtube.com/results?search_type=&search_query={1}
    
    """.format(title, title.replace(" ", "%20"))

    print m

    msg = MIMEText(m, _charset="UTF-8")
    
    me = EMAIL_FROM
    
    msg['Subject'] = "MRK"
    msg['From'] = me
    msg['Reply-to'] = me
    msg['To'] = EMAIL_TO
    msg['Cc'] = me
    
    s = smtplib.SMTP()
    s.connect("localhost")
    s.sendmail(me, EMAIL_TO + ", " + me, msg.as_string())
    s.close()
    
@route('/')
def index():
    return(u'Most akarsz is valamit, vagy csak kóstolgatsz?')
    
@route('/akaromacimet')
def akarom():
    
    f = open(PROJECT_PATH + "/nowplaying", "r")
    title = f.readline()
    print(title)
    f.close()
    
    send_mail(title)
    return "{0}".format(title)
    
@error(404)
def error404(error):
    return "Szerintem eltévedtél..."  

application = default_app()