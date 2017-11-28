#coding: utf8
import sys

if __name__ == "__main__":
    sys.path.insert(0, sys.path[0]+'//tv')
from tvd import *

class TvProxy():
    """
        Proxy for tv:
        if you would rather create your own function, this class must be modified.
    """
    available = list()
    tv1 = None

    def __init__(self):
        try:
            self.tv1 = Tv()
            if 'bozo_exception' in self.tv1.rss_feed:
                raise BozoException()
            self.tv1.getEntries()
            self.available += self.tv1.getChannels()
        except BozoException:
            print "error tv"
        
    def getAvailableList(self):
        return self.available

    def getEntriesChannel(self, channel):
        """
            Receives the name of the desired channel and returns a list of Entry objects
        """
        entries = list()
        if channel in self.tv1.getChannels():
            entries = self.tv1.getChannelProgram(channel)
        return entries

    # TODO create filter by time for entries
    def filterByHour(self, entries, hour_start, hour_end=""):
        filtered_entries = list()
        for e in entries:
            ## if e.hour
            filtered_entries.append(e)
        return filtered_entries
    

if __name__ == '__main__':
    tp = TvProxy()
    print tp.getAvailableList()
    print tp.getEntriesChannel('TF1')

