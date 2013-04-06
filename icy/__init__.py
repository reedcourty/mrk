#!/usr/bin python
# -*- coding: UTF-8 -*-

import socket
import logging
import requests

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)

def get_title(url, timeout):
    title = "Sajnos nem tudom most ezt megmondani neked. :("
    try:
        r = requests.get(url, headers={'Icy-MetaData':'1'}, stream=True, 
            timeout=timeout)
        logger.debug('r = {0}'.format(r))
        interval = r.headers['icy-metaint']
        logger.debug('interval = {0}'.format(interval))
        r.raw.read(int(interval))
        lenght = ord(r.raw.read(1))*16
        logger.debug('lenght = {0}'.format(lenght))
        stream_title = r.raw.read(lenght)
        logger.debug('stream_title = {0}'.format(stream_title))

        st_bstring = "StreamTitle='" # Ezt fogjuk levágni a stream_title elejéről
        st_estring = "';" # Ezt fogjuk megkeresni a stream_title végén és onnantól vágunk
        
        b = len(st_bstring)
        logger.debug('b = {0}'.format(b))
        e = stream_title.rfind(st_estring)
        logger.debug('e = {0}'.format(e))
        
        title = stream_title[b:e]
        logger.debug('title = {0}'.format(title))
    except (socket.timeout, requests.exceptions.Timeout):
        pass
    return title

if __name__ == '__main__':

    RADIO_URL = "http://mr-stream.mediaconnect.hu/4738/mr2.mp3"
    RADIO_TIMEOUT = 1

    print(get_title(RADIO_URL, RADIO_TIMEOUT))