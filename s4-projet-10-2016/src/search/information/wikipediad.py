# coding: utf8

import wikipedia

class Wikipedia():
    lang = ''
    results = list()
    summary = ''
    ind = -1

    def __init__(self, lang='fr'):
        self.lang = lang
        wikipedia.set_lang("fr")

    def setLang(self, lang):
        self.lang = lang
        wikipedia.set_lang("fr")

    def getResults(self, search, results=5):
        self.results = wikipedia.search(search, results=results)
        for i in range(len(self.results)):
            self.results[i] = self.results[i].encode('utf8','ignore')
        self.results = self.results[1:]
        return self.results

    def multipleResultsToChoice(self, results):
        """
            If there is ambiguation returns dictionary
            containing options for the user to pick
        """
        if len(results) == 1:
            return None
        opt = dict()
        for i in range(1, len(results)):
            opt[i] = results[i]
        return opt

    def isAmbiguosOrEmpty(self, search):
        try:
            wikipedia.summary(search, 1)
            return 1
        except wikipedia.exceptions.DisambiguationError:
            # More than one result #
            return 0
        except wikipedia.exceptions.PageError:
            # No results #
            return -1

    def getSummary(self, search, sentences=3):
        """
            Gets the summary of a search,
            if there is an ambiguation it takes the first result
        """    
        try:
            self.summary = wikipedia.summary(search, sentences=sentences).encode('utf8','ignore')
        except wikipedia.exceptions.DisambiguationError:
            # More than one result #
            self.getSummary(self.getResults(search)[1], sentences=sentences)
        except wikipedia.exceptions.PageError:
            print "No results"
        return self.summary

    def getNextResult(self):
        """ Returns the next result, none if something is not set """
        result = None
        if len(self.results):
            self.ind = (self.ind+1) % len(self.results)
            result = self.results[self.ind]
        print "wikipedia getNextResult", type(result)
        return result

    def getSections(self):
        pass

    def readSection(self, section):
        pass

if __name__ == "__main__":
    w = Wikipedia()
    search = raw_input("Search: ")
    aa = w.isAmbiguosOrEmpty(search)
    if aa == -1:
        print "No results"
    elif aa == 1:
        print "Direct:"
        print w.getSummary(search)
    
    else:
        print "Probable Ambiguation:"
        opt = dict()
        while opt != None:
            results = w.getResults(search)
            opt = w.multipleResultsToChoice(results)
            print "Multiple results:\n", opt
            oo = "-1"
            while oo not in opt:
                oo = int(raw_input("Choose: "))
            search = opt[oo]
            if w.isAmbiguosOrEmpty(search) == 1:
                break
        print w.getSummary(search)
