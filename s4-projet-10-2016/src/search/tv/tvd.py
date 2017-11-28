# coding: utf8
import feedparser, re, sys

if __name__ == "__main__":
    sys.path.insert(0, '//'.join(sys.path[0].split('//')[:-1]))

from entry import *
from datetime import datetime
import time

class Tv():
    link = ""
    entries = dict()
    rss_feed = None

    def __init__(self):
        today = time.strftime("%Y-%m-%d")
        self.link = 'http://webnext.fr/epg_cache/programme-tv-rss_'+today+'.xml'
        self.rss_feed = feedparser.parse(self.link)

    def getEntries(self):
        for post in self.rss_feed.entries:
            channel, hour, name = post.title.split(' | ')
            entry = Entry(name.encode("utf8", 'ignore'), self.fixDescription(post.description.encode("utf8", 'ignore')), None, hour)
            if channel not in self.entries:
                self.entries[channel] = list()
            self.entries[channel].append(entry)
        return self.entries

    def getChannels(self):
        return self.entries.keys()

    def getChannelProgram(self, channel):
        return self.entries[channel]

    def strToDate(self, date):
        #return parser.parse(date) #work with this for different timezones
        return datetime.strptime(date[:-6], '%a, %d %b %Y %X')

    def fixDescription(self, description, limit=2):
        #Remove incomplete sentences
        desc = re.sub(r'[^.]*\.\.\.$', '', description)
        if desc == '':
            desc = description

        #TODO Remove tags

        #Remove ... between phrases 
        desc = desc.replace("...", ";")

        #Limit the number of phrases
        phrases = re.findall(r'[^.]{2,}\.', desc)
        desc = ' '.join(phrases[:(min(limit,len(phrases)))])
        return desc

if __name__ == '__main__':
    try:
        tv = Tv()
        
        if 'bozo_exception' in tv.rss_feed:
            print tv.rss_feed['bozo_exception']
            raise BozoException()
        
        tv.getEntries()
        channel = "TF1"
        program = tv.getChannelProgram(channel)
        print channel
        print "Program: " + program[0].title + " - Hour: " + "\n" + program[0].description
    except BozoException:
        print "parser error"
