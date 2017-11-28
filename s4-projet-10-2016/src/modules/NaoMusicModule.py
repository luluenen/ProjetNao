#coding: utf8

from naoqi import ALModule
import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, '/'.join(sys.path[0].split('//')[:-1])+'/search')
    sys.path.insert(0, '/'.join(sys.path[0].split('//')[:-1]))

import PATH
from musicProxy import *

CONFIDENCE = 0.45

class NaoMusicModule(ALModule):

    def __init__(self, name, Nao):
        """ Constructor """
        ALModule.__init__(self, name)
        self.Nao = Nao
        self.proxy = MusicProxy()

        # Event Subscription        
        self.Nao.memoryProxy.subscribeToEvent("MusicRequest", "NaoMusic", "onMusicRequest")
        self.Nao.memoryProxy.subscribeToEvent("PlayMusicRequest", "NaoMusic", "onPlayMusicRequest")

    def exit(self):
        """ Destructor """
        self.Nao.memoryProxy.unsubscribeToEvent("MusicRequest")
        self.Nao.memoryProxy.unsubscribeToEvent("PlayMusicRequest")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoMusic")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("MusicFinished"):
            self.Nao.memoryProxy.unsubscribeToEvent("MusicFinished", "NaoMusic")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("HandLeftBackTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("HandLeftBackTouched", "NaoMusic")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoMusic")
        ALModule.exit(self)

    def onMusicRequest(self, *_args):
        """
            Callback function for MusicRequest event risen by Dialog.
            Asks for the song searched and then asks for confirmation.
        """
        print "inside music"
        self.Nao.deactivateDialog()
        self.Nao.say("Dites-moi quel morceaux vous voulez")
        self.text = self.Nao.listen()

        # Nao says what he understood       
        print self.text
        if self.text == None:
            self.Nao.say("Je n'ai pas compris")
            self.Nao.memoryProxy.raiseEvent("MusicRequest", 0)
        else:
            # If he understood, he asks for confirmation
            self.Nao.say("Cherchez-vous "+self.text+" ?")
            self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoMusic", "onOkRequest")
   
    def onOkRequest(self, key, value, message):
        """
            Callback function for OkRequest event risen by onMusicRequest.
            If the user confirms the search, it searches the song and downloads it;
            rises MusicRequest otherwise.
        """
        print "ok request"
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoMusic")
            ok = False
            print "Word Recognized value = " + str(value) # value = [phrase, confidence]
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                # Nao says the word understood
                if word == "oui":
                    self.Nao.say("Je recherche "+self.text)
            
                    # Download music from youtube
                    print "start downloading"
                    self.fname = PATH.PATH_DB + "/musicfile/" + self.proxy.getSong(self.text, PATH.PATH_DB+"/musicfile")
                    print self.fname, "downloaded"
                    # Insert song into database and update profile
                    info = self.proxy.getSongInfo()
                    self.Nao.db_client.insertSong(info['title'], self.text, info['filename'], info['link'], info['tags'])
                    self.Nao.db_client.updateViewSong(self.Nao.session, info['filename'])
                    
                    self.Nao.memoryProxy.raiseEvent("PlayMusicRequest", 0)
                elif word == "non":
                    self.Nao.memoryProxy.raiseEvent("MusicRequest", 0)
                else:
                    ok = False
                    print "Unknown option"   
            if not ok:
                self.Nao.say("Je n'ai pas compris")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoMusic", "onOkRequest")

    # Uploads song to Nao and plays it    
    def onPlayMusicRequest(self, *_args):
        """
            Callback function for PlayMusicRequest event risen by onOkRequest and onHandLeftBackTouched.
            Uploads the downloaded song to NAO and plays it.
        """
        # Upload music file to Nao
        self.Nao.ftp.uploadFile(self.fname.replace("/","\\"))
        print "finished uploading", self.fname

        self.Nao.say("Je vais jouer la musique "+self.text+". Pour arrêter la musique touchez-moi la tête, ou touchez-moi la main pour obtenir un autre résultat.")

        # Subscribe to event to stop music and finished music       
        self.Nao.memoryProxy.subscribeToEvent("FrontTactilTouched", "NaoMusic", "onFrontTactilTouched")
        self.Nao.memoryProxy.subscribeToEvent("HandLeftBackTouched", "NaoMusic", "onHandLeftBackTouched")
        self.Nao.memoryProxy.subscribeToEvent("MusicFinished", "NaoMusic", "onMusicFinished")

        # Play Music    
        self.Nao.play("/home/nao/"+self.fname.replace("/","\\"))

    def onHandLeftBackTouched(self, *_args):
        """
            Callback function for HandLeftBackTouched event.
            Stops the current playing song and downloads the next result of the search.
        """
        print "choose other result"
        stopped = False
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("MusicFinished"):
            self.Nao.memoryProxy.unsubscribeToEvent("MusicFinished", "NaoMusic")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("HandLeftBackTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("HandLeftBackTouched", "NaoMusic")
            stopped = True
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoMusic")
            stopped = True
        if stopped:
            self.Nao.stopAll()
            self.fname = PATH.PATH_DB + "/musicfile/" + self.proxy.getNextSong(PATH.PATH_DB+"/musicfile")
            # Insert song into database and update profile
            info = self.proxy.getSongInfo()
            self.Nao.db_client.insertSong(info['title'], self.text, info['filename'], info['link'], info['tags'])
            self.Nao.db_client.updateViewSong(self.Nao.session, info['filename'])

            self.Nao.memoryProxy.raiseEvent("PlayMusicRequest", 0)

    def onMusicFinished(self, *_args):
        """
            Callback function for MusicFinished event risen when the songs ends.
            Asks the user if he wants another song.
        """
        print "finished playing music"
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("MusicFinished"):
            self.Nao.memoryProxy.unsubscribeToEvent("MusicFinished", "NaoMusic")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("HandLeftBackTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("HandLeftBackTouched", "NaoMusic")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoMusic")
        self.Nao.say("Voulez-vous un autre morceaux?")
        self.Nao.ftp.deleteFile(self.fname.replace("/","\\"))
        self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoMusic", "onWordRecognized")
           
    def onFrontTactilTouched(self, *_args):
        """
            Callback function for FrontTactilTouched event.
            Stops the current playing song and asks the user if he wants another one.
        """
        print "stopped music"
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoMusic")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("HandLeftBackTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("HandLeftBackTouched", "NaoMusic")
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("MusicFinished"):
            self.Nao.memoryProxy.unsubscribeToEvent("MusicFinished", "NaoMusic")
        self.Nao.stopAll()
        self.Nao.say("Voulez-vous un autre morceaux?")
        self.Nao.ftp.deleteFile(self.fname.replace("/","\\"))
        self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoMusic", "onWordRecognized")

    # Choose between staying in MusicModule or MultimediaModule (menu) 
    def onWordRecognized(self, key, value, message):
        """
            Callback function for WordRecognized event.
            Answer to the question if another search is intended,
            if yes it rises MusicRequest; rises MultimediaRequest otherwise.
        """
        if "NaoMusic" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoMusic")
            ok = False
            print "Word Recognized value = " + str(value) # value = [phrase, confidence]
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                # Nao says the word understood
                if word == "oui":
                    self.Nao.memoryProxy.raiseEvent("MusicRequest", 0)
                elif word == "non":
                    self.Nao.activateDialog()
                    self.Nao.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)
                else:
                    ok = False
                    print "Unknown option"
                    
            if not ok:
                self.Nao.say("Je n'ai pas compris")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoMusic", "onWordRecognized")
