# coding: utf8
import feedparser, re, sys
if __name__ == "__main__":
    sys.path.insert(0, '//'.join(sys.path[0].split('//')[:-1]))
from entry import *
from datetime import datetime

class News():
    newspapers = {"le monde": 'http://www.lemonde.fr/m-actu/rss_full.xml',
                 "côté brest": 'http://www.cotebrest.fr/feed',
                 "ouest france": 'http://www.ouest-france.fr/rss.xml',
                 "télégramme": 'http://www.letelegramme.fr/finistere/brest/rss.xml',
                  "la croix": 'http://www.la-croix.com/RSS/UNIVERS',
                  "l'équipe": 'http://www.lequipe.fr/rss/actu_rss.xml'}
    
    channel_lemonde = ['actu', 'culture', 'emploi', 'europe', 'finance', 'idees', 'international', 'mobilite', 'politique', 'sante', 'sciences', 'societe', 'sport', 'technologies', 'economie']
    channel_telegramme = ['finistere/brest', 'bretagne', 'monde', 'france', 'voile', 'sports', 'economie']

    rss_feed = None

    def __init__(self, news):
        self.news = news
        if not (news in self.newspapers):
            print "Newspaper not in the options, using default << Le Monde >>."
            self.news = "le monde"
        self.rss_feed = feedparser.parse(self.newspapers[self.news])

    def addNewspaper(self, name, link):
        """
            To add a newspaper the link has to be direct to a rss feed (.xml extension)
            and the name should not contain special characters
        """
        newspapers[name] = link

    def showTopics(self):
        if self.news == "le monde":
            return self.channel_lemonde
        elif self.news == "télégramme":
            return self.channel_telegramme
        return []

    def changeTopic(self, topic):
        if topic in self.showTopics():
            if self.news == "le monde":
                link = 'http://www.lemonde.fr/{0}/rss_full.xml'.format(topic)
            elif self.news == "télégramme":
                if topic == 'actu':
                    topic = 'm-actu'
                link = 'http://www.letelegramme.fr/{0}/rss.xml'.format(topic)
            self.rss_feed = feedparser.parse(link)

    def getTitle(self):
        return self.rss_feed['feed']['title']

    def getCountEntries(self):
        return len(self.rss_feed['entries'])

    def getEntries(self, max_post=10):
        entries = list()
        if not self.getCountEntries():
            print "No entries."
       
        for i in range(min(self.getCountEntries(), max_post)):
            post = self.rss_feed.entries[i]
            entries.append(Entry(post.title.encode("utf8", 'ignore'), self.fixDescription(post.description.encode("utf8", 'ignore')), self.strToDate(post.published)))
            
        return entries

    def strToDate(self, date):
        #return parser.parse(date) #work with this for different timezones
        return datetime.strptime(date[:-6], '%a, %d %b %Y %X')

    def fixDescription(self, description, limit=2):
        #Remove incomplete sentences
        desc = re.sub(r'[^.]*\.\.\.$', '', description)
        if desc == '':
            desc = description

        #Remove ... between phrases 
        desc = desc.replace("...", ";")
        desc = desc.replace(">", " ")
        desc = desc.replace("<", " ")

        #Limit the number of phrases
        phrases = re.findall(r'[^.]{2,}\.', desc)
        desc = ' '.join(phrases[:(min(limit,len(phrases)))])
        return desc
   
if __name__ == '__main__':
    try:
        news = News("l'équipe")
        if 'bozo_exception' in news.rss_feed:
            print news.rss_feed['bozo_exception']
            raise BozoException()
        print "Title feed:", news.getTitle()
        print news.getCountEntries(), "Entries in topic."
        entries = news.getEntries()
        print "First entry: " + entries[0].title + "\n" + entries[0].description
    except BozoException:
        print "parser error"
