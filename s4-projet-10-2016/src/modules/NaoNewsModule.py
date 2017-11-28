#coding: utf8

from naoqi import ALModule
import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, '//'.join(sys.path[0].split('//')[:-1])+'/search')
from newsProxy import *

CONFIDENCE = 0.45

class NaoNewsModule(ALModule):

    def __init__(self, name, Nao):
        """ Constructor """
        ALModule.__init__(self, name)
        self.Nao = Nao
        self.np = NewsProxy()
        self.ind = -1
        
        # Event Subscription
        self.Nao.memoryProxy.subscribeToEvent("NewsRequest", "NaoNews", "onNewsRequest")

    def exit(self):
        """ Destructor """
        self.Nao.memoryProxy.unsubscribeToEvent("NewsRequest", "NaoNews")
        ALModule.exit(self)

    def onNewsRequest(self, *_args):
        """ Says newspapers options """
        self.Nao.deactivateDialog()
        if "NaoNews" in self.Nao.memoryProxy.getSubscribers("HandLeftBackTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("HandLeftBackTouched", "NaoNews")
        if "NaoNews" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoNews")
        print "inside news"
        self.ind = (self.ind + 1) % len(self.np.getAvailableList())
        self.Nao.say("Si vous voulez " + self.np.getAvailableList()[self.ind] + ". Touchez moi la tête, sinon, touchez moi la main")
        self.Nao.memoryProxy.subscribeToEvent("HandLeftBackTouched", "NaoNews", "onNewsRequest")
        self.Nao.memoryProxy.subscribeToEvent("FrontTactilTouched", "NaoNews", "onFrontTactilTouched")

    def onFrontTactilTouched(self, *_args):
        """ Says the news """
        print "head touched"
        news = False
        if "NaoNews" in self.Nao.memoryProxy.getSubscribers("HandLeftBackTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("HandLeftBackTouched", "NaoNews")
            news = True
        if "NaoNews" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoNews")
            news = True
        if news:
            self.newspaper = self.np.getAvailableList()[self.ind]
            self.Nao.say("Vous avez choisi, "+ self.newspaper)
            entries = self.np.getEntries(self.newspaper)
            
            # When there are no results
            if not len(entries):
                self.Nao.say("Aucune actualité disponible")
            for e in entries:
                self.Nao.say(' '.join((e.title, e.description)))
                time.sleep(1)
            self.Nao.say("Voulez-vous chercher encore des nouvelles ?")
            time.sleep(1)
            self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoNews", "onWordRecognized")
        
    def onWordRecognized(self, key, value, message):
        """ Checks if the user wants more news or not """
        if "NaoNews" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoNews")       
            ok = False
            print "Word Recognized value = " + str(value) # value = [phrase, confidence]
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                if word == "oui":
                    self.Nao.memoryProxy.raiseEvent("NewsRequest", 0)
                elif word == "non":
                    self.Nao.activateDialog()
                    self.Nao.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)
                else:
                    ok = False
                    print "Unknown option"       
            if not ok:
                self.Nao.say("Je n'ai pas compris")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoNews", "onWordRecognized")

            
