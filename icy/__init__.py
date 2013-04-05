#!/usr/bin python
# -*- coding: UTF-8 -*-

import socket
import requests

def get_title(url, timeout):
    title = "Sajnos nem tudom most ezt megmondani neked. :("
    try:
        r = requests.get(url, headers={'Icy-MetaData':'1'}, stream=True, 
            timeout=timeout)
        interval = r.headers['icy-metaint']
        r.raw.read(int(interval))
        lenght = ord(r.raw.read(1))*16
        stream_title = r.raw.read(lenght)

        st_bstring = "StreamTitle='" # Ezt fogjuk levágni a stream_title elejéről
        st_estring = "';" # Ezt fogjuk megkeresni a stream_title végén és onnantól vágunk
        
        b = len(st_bstring)
        e = stream_title.rfind(st_estring)
        
        title = stream_title[b:e]
    except (socket.timeout, requests.exceptions.Timeout):
        pass
    return title

if __name__ == '__main__':

    RADIO_URL = "http://mr-stream.mediaconnect.hu/4738/mr2.mp3"
    RADIO_TIMEOUT = 1

    print(get_title(RADIO_URL, RADIO_TIMEOUT))