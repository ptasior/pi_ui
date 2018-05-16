import psutil
import subprocess
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read
import shared_data

class Player(object):
    def __init__(self):
        # self.state = 'STOP'
        self.state = 'NEXT'
        shared_data.data['playlist'] = []
        shared_data.addThread('player', self.loop)
        print("player initialised")


    def loop(self):
        if self.state != 'NEXT':
            return

        if not len(shared_data.data['playlist']):
            return

        if 'url' not in shared_data.data['playlist'][0]:
            return

        track = shared_data.data['playlist'].pop()

        self.playUrl(track['url'])


    def playUrl(self, url):
        print('Player: Playing '+url)
        cmd = ['mplayer', '-quiet', '-cache' , '400', url]
        # self.proc_raw = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        self.proc_raw = subprocess.Popen(cmd)

        # flags = fcntl(self.proc_raw.stdout, F_GETFL)
        # fcntl(self.proc_raw.stdout, F_SETFL, flags | O_NONBLOCK)

        self.proc = psutil.Process(pid=self.proc_raw.pid)
        self.status = 'PLAY'



    def resume(self):
        try:
            for c in self.proc.children(recursive=True):
                c.resume()
        except: pass
        try: self.proc.resume()
        except: pass
        self.status = 'PLAY'


    def pause(self):
        try:
            for c in self.proc.children(recursive=True):
                c.suspend()
        except: pass

        try: self.proc.suspend()
        except: pass
        self.status = 'PAUSE'


    def stop(self):
        try:
            for c in self.proc.children(recursive=True):
                c.terminate()
        except: pass
        try: self.proc.terminate()
        except: pass
        self.status = 'STOP'


    def next(self):
        self.stop()
        self.status = 'NEXT'

