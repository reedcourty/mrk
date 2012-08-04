import subprocess

process = subprocess.Popen(['d:/System/Programs/MPlayer/NoGUI/mplayer.exe',
                            '-vo', 'null', '-ao', 'null',
                            'http://mr-stream.mediaconnect.hu/4738/mr2.mp3'],
                            shell=False, stdout=subprocess.PIPE)

for line in process.stdout:
    if (line.find("ICY Info: StreamTitle=") != -1):
        if (line.find("Nagyon Zene!") == -1):
            print(line.split("'")[1])