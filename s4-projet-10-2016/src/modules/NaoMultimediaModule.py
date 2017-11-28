#coding: utf8

from naoqi import ALModule
import time, sys, pdb

CONFIDENCE = 0.45

class NaoMultimediaModule(ALModule):
    '''
        Nao Multimedia.
        Menu for the program, activates Dialog.
    '''

    def __init__(self, name, Nao):
        ALModule.__init__(self, name)
        self.Nao = Nao

        # Event subscriptions        
        self.Nao.memoryProxy.subscribeToEvent("NaoMultimediaRequest", "NaoMultimedia", "onNaoMultimediaRequest")

    def exit(self):
        """ Destructor """
        self.Nao.memoryProxy.unsubscribeToEvent("NaoMultimediaRequest", "NaoMultimedia", "onNaoMultimediaRequest")
        if "NaoMultimediaModule" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoMultimedia", "onWordRecognized")
        ALModule.exit(self)

    def onNaoMultimediaRequest(self, *_args):
        """
            Callback function for NaoMultimediaRequest event.
            Activates Dialog.
        """
        print "multimedia"
        # Prepare the body for moving
        self.Nao.activateDialog()
        self.Nao.say("Bonjour, Dites-moi ce que vous voulez")
        self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoMultimedia", "onWordRecognized2")

    def onWordRecognized(self, key, value, message):
        """
            Deprecated.
            Dialog is used instead of keywords.
        """
        ok = False
        print "Word Recognized value = " + str(value) # value = [phrase, confidence]
        
        # Confidence check
        if value[1] > CONFIDENCE:
            ok = True
            word = value[0]
            # Nao says the word understood
            self.Nao.say(word)
            
            if word == "musique":
                self.Nao.memoryProxy.raiseEvent("MusicRequest", 0)
            elif word == "journal":
                self.Nao.memoryProxy.raiseEvent("NewsRequest", 0)
            elif word == "info":
                self.Nao.memoryProxy.raiseEvent("InformationRequest", 0)
            elif word == "télé":
                self.Nao.memoryProxy.raiseEvent("TvRequest", 0)
            elif word == "histoire":
                self.Nao.memoryProxy.raiseEvent("StoryRequest", 0)            
            else:
                ok = False
                print "Unknown option"
                
        if not ok:
            self.Nao.say("Je n'ai pas compris")
            time.sleep(1)
            self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoMultimedia", "onWordRecognized")
