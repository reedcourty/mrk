#!/usr/bin python
# -*- coding: UTF-8 -*-

import subprocess
import os
import ConfigParser

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

print(PROJECT_PATH)

config = ConfigParser.ConfigParser()
config.read(PROJECT_PATH + '/mrk.cfg')

MPLAYER = config.get('path', 'mplayer')
RADIO_URL = config.get('radio', 'url')

while True:
    process = subprocess.Popen([MPLAYER, '-vo', 'null', '-ao', 'null',
                                RADIO_URL],
                                shell=False, stdout=subprocess.PIPE)

    for line in process.stdout:
        if (line.find("ICY Info: StreamTitle=") != -1):
            if (line.find("Nagyon Zene!") == -1):
                title = line.split("'")[1]
                print(title)
                f = open(PROJECT_PATH + "/nowplaying", "w")
                f.write(title)
                f.close()
        if (line.find("Audio output truncated at end.") != -1):
            break
