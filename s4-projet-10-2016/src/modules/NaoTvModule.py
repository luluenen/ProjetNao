#coding: utf8

from naoqi import ALModule
import time, sys
from datetime import *

if __name__ == "__main__":
    sys.path.insert(0, '//'.join(sys.path[0].split('//')[:-1])+'/search')
from tvProxy import *

CONFIDENCE = 0.45

class NaoTvModule(ALModule):

    def __init__(self, name, Nao):
        """ Constructor """
        ALModule.__init__(self, name)
        self.Nao = Nao
        self.popular_channels = ["TF1", "France 2", "France 3", "M6", "France 4"]
        self.ind = -1

        # Event Subscription
        self.Nao.memoryProxy.subscribeToEvent("TvRequest", "NaoTv", "onTvRequest")
        self.Nao.memoryProxy.subscribeToEvent("SearchProgramRequest", "NaoTv", "onSearchProgramRequest")

    def exit(self):
        """ Destructor """
        self.Nao.memoryProxy.unsubscribeToEvent("TvRequest", "NaoTv")
        ALModule.exit(self)

    def onTvRequest(self, *_args):
        print "inside tv"
        self.Nao.deactivateDialog()
        self.ind = (self.ind + 1) % len(self.popular_channels)
        
        self.Nao.say("^start(animations/Stand/Gestures/Enthusiastic_5) La télé, c'est cool")
        self.Nao.say("De quelle chaine voulez vous le programme ?")

        self.text = self.Nao.listen()
        print self.text

        if self.text not in self.popular_channels:
            self.Nao.say("Je n'ai pas compris")
            self.Nao.memoryProxy.raiseEvent("TvRequest", 0)
        else:
            self.Nao.say("Vous voulez le programme de "+self.text+ "?") 
            self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoTv", "onOkTvRequest")

    def onOkTvRequest(self, key, value, message):
        print "inside onOkTvRequest"
        if "NaoTv" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoTv")
            ok = False
            print "Word Recognized value = " + str(value) # value = [phrase, confidence]
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                if word == "oui":
                    self.Nao.memoryProxy.raiseEvent("SearchProgramRequest", 0)
                elif word == "non":
                    self.Nao.memoryProxy.raiseEvent("TvRequest", 0)
                else:
                    ok = False
                    print "Unknown option"       
            if not ok:
                self.Nao.say("Je n'ai pas compris")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoTv", "onOkTvRequest")

    def onSearchProgramRequest(self, *_args):
        try:
            tp = tvProxy()
            currentHour = datetime.datetime().now().hour
            programs = tp.getEntriesChannel(self.text)
            filteredPrograms = tp.filterByHour(programs, str(currentHour))
            for p in filteredPrograms:
                self.Nao.say("A " + p.hour+" il y a "+ p.title)
            self.Nao.say("Vous voulez cherchez encore des programmes télé?")
            self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoTv", "onWordRecognized")
        except Exception:
            self.Nao.say("Je n'ai pas accès aux programmes télé maintenant")
            self.Nao.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)
        
    def onWordRecognized(self, key, value, message):
        """ Checks if the user wants more news or not """
        if "NaoTv" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoTv")
            ok = False
            print "Word Recognized value = " + str(value) # value = [phrase, confidence]
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                if word == "oui":
                    self.Nao.memoryProxy.raiseEvent("TvRequest", 0)
                elif word == "non":
                    self.Nao.activateDialog()
                    self.Nao.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)
                else:
                    ok = False
                    print "Unknown option"       
            if not ok:
                self.Nao.say("Je n'ai pas compris")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoTv", "onWordRecognized")
    
