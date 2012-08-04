import subprocess

import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

print(PROJECT_PATH)

process = subprocess.Popen(['d:/System/Programs/MPlayer/NoGUI/mplayer.exe',
                            '-vo', 'null', '-ao', 'null',
                            'http://mr-stream.mediaconnect.hu/4738/mr2.mp3'],
                            shell=False, stdout=subprocess.PIPE)

for line in process.stdout:
    if (line.find("ICY Info: StreamTitle=") != -1):
        if (line.find("Nagyon Zene!") == -1):
            title = line.split("'")[1]
            print(title)
            f = open(PROJECT_PATH + "/nowplaying", "w")
            f.write(title)
            f.close()