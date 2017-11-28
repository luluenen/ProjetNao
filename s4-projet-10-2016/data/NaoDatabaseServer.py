#coding: utf8
import subprocess, shlex
import sys
from pymongo import *
from datetime import datetime

DB_NAME = "NaoDatabase"

class NaoDatabaseServer():
    """
        Server for MongoDB.
        Runs the mongoDB server and creates the NaoDatabase.
    """
    proc = None

    def __init__(self, path):
        # Run MongoDB server (mongod)
        command_line = path+'//mongod --dbpath "'+path+'//db" --port 27017'
        args = shlex.split(command_line)
        self.proc = subprocess.Popen(args)

        # Initialize db if does not exist
        client = MongoClient()
        if DB_NAME not in client.database_names():
            try:
                print "Initializing database"
                db = client[DB_NAME]
                self.initNewspapers(db)
                self.initStories(db)
            except Exception:
                client.drop_database(DB_NAME)
                client.close()
        client.close()       

    def stopServer(self):
        self.proc.terminate()
    
    def initNewspapers(self, db):
        """
            Initializes the newspapers in the database
        """
        # Insert Le Monde
        result = db.newspapers.insert_one(
            {
                "name": "le monde",
                "root_link": "http://www.lemonde.fr",
                "end_link": "/rss_full.xml",
                "xml": True,
                "type": "general",
                "sections": [{"name": "actualité", "link": "/m-actu"},
                             {"name": "culture", "link": "/culture"},
                             {"name": "emploi", "link": "/emploi"},
                             {"name": "europe", "link": "/europe"},
                             {"name": "finance", "link": "/finance"},
                             {"name": "international", "link": "/international"},
                             {"name": "sciences", "link": "/sciences"},
                             {"name": "sports", "link": "/sport"},
                             {"name": "économie", "link": "/economie"}]
            }
        )

        # Insert le télégramme
        result = db.newspapers.insert_one(
            {
                "name": "télégramme",
                "root_link": "http://www.letelegramme.fr",
                "end_link": "/rss.xml",
                "xml": True,
                "type": "general",
                "sections": [{"name": "actualité", "link": ""},
                             {"name": "brest", "link": "/finistere/brest"},
                             {"name": "bretagne", "link": "/bretagne"},
                             {"name": "monde", "link": "/monde"},
                             {"name": "france", "link": "/france"},
                             {"name": "voile", "link": "/voile"},
                             {"name": "sports", "link": "/sports"},
                             {"name": "économie", "link": "/economie"}]
            }
        )
        
        # Insert Ouest France
        result = db.newspapers.insert_one(
            {
                "name": "ouest france",
                "root_link": "http://www.ouest-france.fr",
                "end_link": "/rss.xml",
                "xml": True,
                "type": "general",
                "sections": [{"name": "actualité", "link": ""}]
            }
        )

        # Insert Côté Brest
        result = db.newspapers.insert_one(
            {
                "name": "côté brest",
                "root_link": "http://www.cotebrest.fr",
                "end_link": "/feed",
                "xml": True,
                "type": "general",
                "sections": [{"name": "actualité", "link": ""}]
            }
        )

        # Insert la croix
        result = db.newspapers.insert_one(
            {
                "name": "la croix",
                "root_link": "http://www.la-croix.com/RSS",
                "end_link": "",
                "xml": True,
                "type": "general",
                "sections": [{"name": "actualité", "link": "/UNIVERS"},
                             {"name": "france", "link": "/UNIVERS_WFRA"},
                             {"name": "europe", "link": "/WMON-EUR"},
                             {"name": "monde", "link": "/UNIVERS_WMON"},
                             {"name": "économie", "link": "/UNIVERS_WECO"},
                             {"name": "sports", "link": "/UNIVERS_WSPO"},
                             {"name": "culture", "link": "/UNIVERS_WCLT"},
                             {"name": "religion", "link": "/UNIVERS_WREL"}]
            }
        )

        # Insert l'équipe
        result = db.newspapers.insert_one(
            {
                "name": "l'équipe",
                "root_link": "http://www.lequipe.fr/rss",
                "end_link": ".xml",
                "xml": True,
                "type": "sports",
                "sections": [{"name": "actualité", "link": "/actu_rss"},
                             {"name": "football", "link": "/actu_rss_Football"},
                             {"name": "auto-moto", "link": "/actu_rss_Auto-Moto"},
                             {"name": "tennis", "link": "/actu_rss_Tennis"},
                             {"name": "golf", "link": "/actu_rss_Golf"},
                             {"name": "rugby", "link": "/actu_rss_Rugby"},
                             {"name": "basket", "link": "/actu_rss_Basket"},
                             {"name": "hand", "link": "/actu_rss_Hand"},
                             {"name": "cyclisme", "link": "/actu_rss_Cyclisme"}]
            }
        )


    def initStories(self, db):
        """
            Initializes the histories in the database
        """
        # Insert La cigale et la fourmi
        result = db.histories.insert_one(
            {
                "name": "la cigale et la fourmi",
                "file_name": "la_cigale_et_la_fourmi.txt",
                "genre": "enfantin",
                "tags": ["enfantin", "court"]
            }
        )

if "__main__" == __name__:
    server = NaoDatabaseServer(sys.path[0].replace("\\","//"))
