import os
import re
import pafy
import urllib.request
import urllib.parse
from threading import Thread

import shared_data



class YoutubeLinker(object):
    def __init__(self):
        self.processing = False


    def runThread(self):
        self.processing = True
        self.thread = Thread(target = self.loop)
        self.thread.setDaemon(True)
        self.thread.start()


    def loop(self):
        pos = 0
        while pos < len(shared_data.data['playlist']):
            it = shared_data.data['playlist'][pos]
            if 'url' not in it:
                it['url'] = self.findUrl(it['title'])
                pos = 0
                # time.sleep(0.1)
            else:
                pos = pos + 1
        self.processing = False


    def findUrl(self, title):
        query_string = urllib.parse.urlencode({"search_query" : title})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

        if not len(search_results): return ''

        url = "http://www.youtube.com/watch?v=" + search_results[0]

        video = pafy.new(url)
        # print("--", video.title.encode('utf-8'), "--")
        # print(url)

        w = min(video.audiostreams, key=lambda x: x.get_filesize())
        return w.url

