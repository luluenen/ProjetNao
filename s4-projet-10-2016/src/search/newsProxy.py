#coding: utf8
import sys

if __name__ == "__main__":
    sys.path.insert(0, sys.path[0]+'//news')
from newsd import *

class NewsProxy():
    """
        Proxy for news:
        To add a newspaper you direct to the method addNewspaper in the class News;
        if you would rather create your own function, this class must be modified.
    """
    available = list()

    def __init__(self):
        self.available += News.newspapers.keys()

    def getAvailableList(self):
        return self.available

    def getEntries(self, newspaper, max_entries=3):
        """
            Receives the name of the desired newspaper with no special characters
            and returns a list of Entry objects
        """
        entries = list()
        if newspaper in News.newspapers:
##            try:
            news = News(newspaper)
##                if 'bozo_exception' in news.rss_feed:
##                    raise BozoException()
            entries = news.getEntries(max_entries)
##            except BozoException:
##                print 'error reading newspaper'
##                return []
        return entries

if __name__ == '__main__':
    np = NewsProxy()
    print np.getAvailableList()
    entries = np.getEntries("côté brest")
    print entries
    for e in entries:
        print ' '.join((e.title, e.description))
