#coding: utf8

from pymongo import *
from datetime import datetime

DB_NAME = "NaoDatabase"

class NaoDatabaseClient():
    """
        Client for MongoDB.
        Manages insertion, updates and search in the database.
    """

    def __init__(self, host='localhost', port=27017):
        self.client = MongoClient([host+':'+str(port)])
        self.db = self.client[DB_NAME]

    def stopClient(self):
        self.client.close()

    """"""""""""""""""""""""
    """  INSERT METHODS  """
    """"""""""""""""""""""""
    
    def insertPerson(self, name):
        """
            Inserts a person in the database.
            To be called when Nao meets someone new.
            name : must be unique
            Returns WriteResult
        """
        result = self.db.persons.insert_one(
            {
                "name": name,
                "newspapers": [],
                "tv": [],
                "music": [],
                "tags": []
            }   
        )
        return result

    def insertNewspaper(self, name, root_link, end_link, is_xml, ntype, sections):
        """
            Insert newspaper in the database
            name : name of the newspaper
            root_link ; start of the link
            end_link : end of the link
            is_xml : boolean if the link is a xml file
            ntype : type of newspaper (general, sports)
            sections : list of dicts. Each dict represents
                a section, with the name and a link that
                is to go between root_link and end_link.
            Returns WriteResult
        """
        result = self.db.newspapers.insert_one(
            {
                "name": name,
                "root_link": root_link,
                "end_link": end_link,
                "xml": is_xml,
                "type": ntype,
                "sections": sections
            }
        )
        return result

    def insertSong(self, title, search, fname, link, tags):
        """
            Insert song in the database
            title : title of the song
            searched_by : the search that got the song
            filename : name of the file in the database
            link : link to download the song
            tags : list of tags of the song (music genre)
            Returns WriteResult
        """
        result = self.findSongByFileName(fname)
        if result == None:
            result = self.db.songs.insert_one(
                {
                    "filename": fname,
                    "title": title,
                    "searched_by": [search],
                    "link": link,
                    "tags": tags
                }
            )
        else:
            result = self.db.songs.update_one(
                {'filename': fname},
                {
                    '$addToSet': {'searched_by': search}
                }
            )
        return result


    """"""""""""""""""""""""
    """  SELECT METHODS  """
    """"""""""""""""""""""""

    def findLink(self, news, section="actualité"):
        """
            Finds the full link for a newspaper feed
            news : name of the newspaper to search
            section : name of the section
            Returns the link in a string
        """
        link = None
        result = self.db.newspapers.find_one({"name": news})
        if result:
            slink = ""
            for s in result["sections"]:
                if s["name"].encode("utf8", 'ignore') == section:
                    slink = s["link"]
                    break
            link = (result["root_link"]+slink+result["end_link"]).encode('utf8', 'ignore')
        return link

    def findPersonByName(self, name):
        """
            Finds a person by its name
            name : name of the person
            Returns the person's information as a dictionary
        """
        return self.db.persons.find_one({'name':name})

    def findNewspaperByName(self, name):
        """
            Finds a newspaper by its name
            name : name of the newspaper
            Returns the newspaper's information as a dictionary
        """
        return self.db.newspapers.find_one({'name':name})

    def findSongByFileName(self, fname):
        """
            Finds a song by its file name
            fname : file name of the song
            Returns the song's information as a dictionary
        """
        return self.db.songs.find_one({'filename':fname})

    def findViewTopic(self, name, topic): 
        """
            Returns a pymongo.results.
        """
        result = self.db.persons.find_one(
            {'name': name, 'topics.name': topic},
            {
                '$inc': {'topics.$.views': 1}
            }
        )
        return result

    """"""""""""""""""""""""
    """  UPDATE METHODS  """
    """"""""""""""""""""""""

    def updateTopicView(self, name, topic):
        """
            Updates the views for a topic
            (news, music, tv, info)
            to be called when a user selects
            a topic from the menu
            name : name of the person
            topic : name of the topic
            Returns a pymong.results.UpdateResult
        """
        result = self.db.persons.update_one(
            {'name': name, 'topics.name': topic},
            {
                '$inc': {'topics.$.views': 1}
            }
        )
        if result.matched_count == 0:
            result = self.db.persons.update_one(
                {'name': name},
                {
                    '$addToSet': {'topics': {'name': topic, 'views': 1}}
                }
            )
        return result

    def updateViewNewspaper(self, name, news):
        """
            Updates the views for a newspaper
            to be called when a user selects a newspaper
            name : name of the person
            news : name of the newspaper
            Returns a pymong.results.UpdateResult
        """
        result = self.db.persons.update_one(
            {'name': name, 'newspapers.name': news},
            {
                '$inc': {'newspapers.$.views': 1}
            }
        )
        if result.matched_count == 0:
            result = self.db.persons.update_one(
                {'name': name},
                {
                    '$addToSet': {'newspapers': {'name': news, 'views': 1}}
                }
            )
        return result

    def updateViewSong(self, name, fname):
        """
            Updates the times a person has listened a song
            to be called when a user selects a song
            name : name of the person
            fname : file name of the song
            Returns a pymong.results.UpdateResult
        """
        result = self.db.persons.update_one(
            {'name': name, 'music.name': fname},
            {
                '$inc': {'music.$.views': 1}
            }
        )
        if result.matched_count == 0:
            result = self.db.persons.update_one(
                {'name': name},
                {
                    '$addToSet': {'music': {'name': fname, 'views': 1}}
                }
            )
        return result
        

    """"""""""""""""""""""""
    """  DELETE METHODS  """
    """"""""""""""""""""""""

    def deletePersonByName(self, name):
        """
            Deletes a person by its name
            name : name of the person
        """
        self.db.persons.remove({'name': name}, 1)

    def deleteSongByFileName(self, fname):
        """
            Deletes a person by its file name
            fname : file name of the song
        """
        self.db.songs.remove({'filename': fname}, 1)

if "__main__" == __name__:
    client = NaoDatabaseClient()
    
