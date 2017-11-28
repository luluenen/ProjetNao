#coding: utf8
import sys

if __name__ == "__main__":
    sys.path.insert(0, sys.path[0]+'//information')
from wikipediad import *

class InformationProxy():
    """
        Proxy for information:
        if you would rather create your own function, this class must be modified.
    """
    available = list()
    searcher = None
    result = None
    ind = -1

    def __init__(self):
        self.available.append('wikipedia')

    def getResult(self, search, tool="wikipedia"):
        """
            Returns list of results
            None for no results.
        """
        if tool.lower() == "wikipedia":
            self.searcher = Wikipedia()
            x = self.searcher.isAmbiguosOrEmpty(search)
            if x == 1:
                self.result = [search]
            elif x == 0:
                self.result = self.searcher.getResults(search)
        return self.result

    def getNextDescription(self, tool="wikipedia"):
        """
            Returns a tuple of (title, text) of the search made;
            if something is not set, returns None.
        """
        result = None
        if self.searcher == None:
            return result
        if tool.lower() == "wikipedia":
            self.ind = (self.ind+1) % len(self.result)
            result = (self.result[self.ind], self.searcher.getSummary(self.result[self.ind]))
        print "proxy getNextDescription", type(result)
        return result

if __name__ == '__main__':
    ip = InformationProxy()
    print ip.getResult("Nadal")
    print ip.getNextDescription()
