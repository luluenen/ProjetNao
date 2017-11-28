#coding: utf8

import youtube_dl
import re
import urllib2
import os
import sys

class YoutubeError(Exception):
    pass

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Youtube():
    video_url = ""
    search_results = list()
    index = -1
    url = ""

    def __init__(self, search=''):
        index = 0
        self.url = "https://www.youtube.com/results?search_query="+search.replace(' ', '+')
        
    def __fetch(self, url):
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0')
        
        try:
            result = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            raise YoutubeError(e.code)
        except urllib2.URLError, e:
            raise YoutubeError(e.reason)
        return result

    def getResults(self):
        html_content = self.__fetch(self.url).read()
        results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content)
        self.search_results = list()
        for result in results:
            if result not in self.search_results:
                self.search_results.append(result)
        return self.search_results

    def filtertMusicVideo(self, max_results=5):
        """ Filters search_results to get only music
            restricts the number of results by max_results """
        results = list(self.search_results)
        self.search_results = list()
        
        for result in results:
            video_url = 'https://www.youtube.com/watch?v='+result
            if self.getVideoGenre(video_url).lower() == "music":
                self.search_results.append(video_url)
                
                # Max get results=5 videos #
                if len(self.search_results) == max_results:
                    break
                
        self.video_url = self.search_results[0]
        return self.search_results

    def getNextMusicVideo(self):
        """ To use without using filterMusicVideo,
            Better performance. """
        if len(self.search_results):
            while True:
                self.index = (self.index+1) % len(self.search_results)
                video_url = 'https://www.youtube.com/watch?v='+self.search_results[self.index]
                if self.getVideoGenre(video_url).lower() == "music":
                    self.video_url = video_url
                    break
        return self.video_url
            
    def downloadVideo(self, video_url, path=""):
        if 'https://www.youtube.com/watch?v=' in video_url:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [self.my_hook],
                'outtmpl': path+'\%(id)s.%(ext)s',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

    def destroyVideo(self, f):
        if os.path.isfile(f):
            os.remove(f)

    def getFileName(self):
        if 'https://www.youtube.com/watch?v=' in self.video_url:
            return self.video_url[32:]+".wav"
        return None

    def getVideoTitle(self, url):
        html_content = self.__fetch(url).read()
        name = re.search(r'\<meta itemprop\=\"name\" content\=\"(.+?)\"\>', html_content)
        if not name == None:
            return name.group(1)
        return None

    def getVideoDuration(self, url):
        """ Returns the length of the given youtube video in minutes (ignores seconds) """
        html_content = self.__fetch(url).read()
        duration = re.search(r'\<meta itemprop\=\"duration\" content\=\"(.+?)\"\>', html_content)
        if not duration == None:
            duration = duration.group(1) # Format string PT+minutes+M+seconds+S
            return int(re.search(r'PT([0-9]*)M', duration).group(1))
        return None

    def getVideoGenre(self, url):
        html_content = self.__fetch(url).read()
        genre = re.search(r'\<meta itemprop\=\"genre\" content\=\"(.+?)\"\>', html_content)
        if not genre == None:
            return genre.group(1)
        return None

    def getVideoTags(self, url):
        html_content = self.__fetch(url).read()
        return [ u''+x.decode('utf8') for x in re.findall(r'\<meta property\=\"og:video:tag\" content\=\"(.+?)\"\>', html_content)]

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

if __name__ == '__main__':
##    search = raw_input("Search: ")
    search = "booba"
    yb = Youtube(search)
    results = yb.getResults()
    yb.getNextMusicVideo()
    print yb.video_url    
    yb.downloadVideo(yb.filtertMusicVideo()[0])
    print 'Tags: ',yb.getVideoTags(yb.video_url)
    
##    while raw_input("Is this your song? ") == "no":
##        yb.destroyVideo(yb.getFileName())
##        yb.getNextResult()
##        yb.downloadVideo(yb.video_url)
    
#   yb.destroyVideo(yb.getFileName())
