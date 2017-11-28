# coding: utf8

class BozoException(Exception):
    """ Exception to be thrown in case of exception in feedparser """
    pass

class Entry():

    def __init__(self, title, description, pubDate, hour=None):
        self.title = title
        self.description = description
        self.pubDate = pubDate
        self.hour = hour

    def __str__(self):
        text = self.title + ": " + self.description
        return text
