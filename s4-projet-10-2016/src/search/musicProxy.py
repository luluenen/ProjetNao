#coding: utf8
import sys
import os

PATH_PROXY = sys.path[0]
if __name__ == "__main__":
    sys.path.insert(0, sys.path[0]+'//music')
from youtubed import *

MAX_DURATION = 15 # Max duration in minutes to download a music file

class MusicProxy():
    """
        Proxy for music:
        if you would rather create your own function, this class must be modified.
    """
    available = list()
    yb = None

    def __init__(self):
        self.available.append('youtube')

    def getAvailableList(self):
        return self.available

    def getSongInfo(self):
        """
            Returns a dict of the information available of the song
            It must at least contain fname, link, title and tags
        """
        if self.yb != None:
            url = self.yb.video_url
            return {'filename': self.yb.getFileName(),
                    'title': self.yb.getVideoTitle(url),
                    'link': url,
                    'tags': self.yb.getVideoTags(url)}

    def getSong(self, search, path=sys.path[0], tool="youtube"):
        """
            Receives a string with the searched song,
            the path for the file must be downloaded
            returns the name of the downloaded file;
            None if there are no results.
        """
        fname = None
        if tool.lower() == "youtube":
            self.yb = Youtube(search)
            self.yb.getResults()
            video_url = self.yb.getNextMusicVideo()
            fname = self.yb.getFileName()
            # Check if the file already exists
            if fname not in os.listdir(path):
                if self.yb.getVideoDuration(video_url) > MAX_DURATION:
                    print "too long"
                    return self.getNextSong(path, tool)
                else:
                    self.yb.downloadVideo(video_url, path)
        return fname

    def getNextSong(self, path=sys.path[0], tool="youtube"):
        """
            Returns the name of the downloaded file;
            None if there are no results or there has not been a search before.
        """
        fname = None
        if self.yb == None:
            print "No searcher initialized"
            return fname
        elif tool.lower() == "youtube":
            video_url = self.yb.getNextMusicVideo()
            fname = self.yb.getFileName()
            # Check if the file already exists            
            if fname not in os.listdir(path):
                if self.yb.getVideoDuration(video_url) > MAX_DURATION:
                    print "too long2"
                    return self.getNextSong(path, tool)
                else:
                    self.yb.downloadVideo(video_url, path)
        return fname


if __name__ == '__main__':
    mp = MusicProxy()
    print mp.getSong("crazy")
    print mp.getNextSong()
    
