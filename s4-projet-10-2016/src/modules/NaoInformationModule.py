#coding: utf8

from naoqi import ALModule
import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, '//'.join(sys.path[0].split('//')[:-1])+'/search')
from informationProxy import *

CONFIDENCE = 0.45

class NaoInformationModule(ALModule):

    def __init__(self, name, Nao):
        """ Constructor """
        ALModule.__init__(self, name)
        self.Nao = Nao
        self.proxy = InformationProxy()

        # Event Subscription        
        self.Nao.memoryProxy.subscribeToEvent("InformationRequest", "NaoInformation", "onInformationRequest")
        self.Nao.memoryProxy.subscribeToEvent("SearchRequest", "NaoInformation", "onSearchRequest")
        self.Nao.memoryProxy.subscribeToEvent("AmbiguosRequest", "NaoInformation", "onAmbiguosRequest")

    def exit(self):
        """ Destructor """
        self.Nao.memoryProxy.unsubscribeToEvent("NaoMusicRequest", "NaoMusic")
        self.Nao.memoryProxy.unsubscribeToEvent("SearchRequest", "NaoInformation")
        self.Nao.memoryProxy.unsubscribeToEvent("AmbiguosRequest", "NaoInformation")
        ALModule.exit(self)

    # When NaoMultimedia rises InformationRequest    
    def onInformationRequest(self, *_args):
        print "inside info"
        self.Nao.deactivateDialog()
        self.Nao.say("Dites-moi ce que vous voulez savoir")
        
        self.text = self.Nao.listen()
        # Nao says what he understood       
        print self.text
        if self.text == None:
            self.Nao.say("Je n'ai pas compris")
            self.Nao.memoryProxy.raiseEvent("InformationRequest", 0)
        else:
            # If he understood, he asks for confirmation
            self.Nao.say("Cherchez-vous "+self.text+" ?")
            self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoInformation", "onOkRequest")

    # Confirm search request
    def onOkRequest(self, key, value, message):
        print "ok request"
        if "NaoInformation" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoInformation")
            ok = False
            print "Word Recognized value = " + str(value) # value = [phrase, confidence]
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                # Nao says the word understood
                if word == "oui":
                    self.Nao.memoryProxy.raiseEvent("SearchRequest", 0)
                elif word == "non":
                    self.Nao.memoryProxy.raiseEvent("InformationRequest", 0)
                else:
                    ok = False
                    print "Unknown option"
                    
            if not ok:
                self.Nao.say("Je n'ai pas compris")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoInformation", "onOkRequest")

    def onSearchRequest(self, *_args):
        # Nao says what he understood       
        print self.text
        if self.text == None:
            self.Nao.say("Je n'ai pas compris")
            self.Nao.memoryProxy.raiseEvent("InformationRequest", 0)
        else:
            self.result = self.proxy.getResult(self.text)
            if self.result == None:
                # No results
                self.Nao.say("Je n'ai aucun résultat. Voulez-vous chercher une autre information ?")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoInformation", "onWordRecognized")
            elif len(self.result) == 1:
                # One result
                t, d = self.proxy.getNextDescription()
                self.Nao.say(t+": "+d)
                self.Nao.say("Voulez-vous chercher une autre information ?")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoInformation", "onWordRecognized")
            elif len(self.result) > 1:
                # Many results
                self.Nao.say("J'ai plusiers résultats")
                self.Nao.memoryProxy.raiseEvent("AmbiguosRequest", 0)

    # Request to stay in informationModule or go to MultimediaModule (menu)           
    def onWordRecognized(self, key, value, message):
        if "NaoInformation" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoInformation")
            ok = False
            print "Word Recognized value = " + str(value)
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                # Nao says the word understood
                if word == "oui":
                    self.Nao.memoryProxy.raiseEvent("InformationRequest", 0)
                elif word == "non":
                    self.Nao.activateDialog()
                    self.Nao.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)
                else:
                    ok = False
                    print "Unknown option"       
            if not ok:
                self.Nao.say("Je n'ai pas compris")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoInformation", "onWordRecognized")

    # Raised when there are more results
    def onAmbiguosRequest(self, *_args):
        print "showing option"
        if "NaoInformation" in self.Nao.memoryProxy.getSubscribers("HandLeftBackTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("HandLeftBackTouched", "NaoInformation")
        if "NaoInformation" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoInformation")
        self.t, self.description = self.proxy.getNextDescription()
        self.Nao.say("Si vous recherchez "+self.t+". Touchez moi la tête, sinon, touchez moi la main")
        self.Nao.memoryProxy.subscribeToEvent("HandLeftBackTouched", "NaoInformation", "onAmbiguosRequest")
        self.Nao.memoryProxy.subscribeToEvent("FrontTactilTouched", "NaoInformation", "onFrontTactilTouched")

    # Confirm from ambiguos
    def onFrontTactilTouched(self, *_args):
        print "head touched"
        touched = False
        if "NaoInformation" in self.Nao.memoryProxy.getSubscribers("HandLeftBackTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("HandLeftBackTouched", "NaoInformation")
            touched = True
        if "NaoInformation" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoInformation")
            touched = True
        if touched:
            self.Nao.say(self.description)
            time.sleep(1)
            self.Nao.say("Voulez-vous chercher une autre information ?")
            self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoInformation", "onWordRecognized")
