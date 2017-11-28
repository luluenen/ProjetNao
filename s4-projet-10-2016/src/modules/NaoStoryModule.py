#coding: utf8

from naoqi import ALModule
import time
import sys
from random import choice

if __name__ == "__main__":
    sys.path.insert(0, '//'.join(sys.path[0].split('//')[:-1])+'/search')
    sys.path.insert(0, '//'.join(sys.path[0].split('//')[:-1]))

import PATH
from storyProxy import *

CONFIDENCE = 0.45

class NaoStoryModule(ALModule):

    def __init__(self, name, Nao):
        """ Constructor """
        ALModule.__init__(self, name)
        self.Nao = Nao
        self.proxy = StoryProxy()

        # Event Subscription        
        self.Nao.memoryProxy.subscribeToEvent("StoryRequest", "NaoStory", "onStoryRequest")

    def exit(self):
        """ Destructor """
        self.Nao.memoryProxy.unsubscribeToEvent("StoryRequest", "NaoMusic")
        ALModule.exit(self)

    # When NaoMultimedia rises StoryRequest
    def onStoryRequest(self, *_args):
        print "inside story"
        self.Nao.deactivateDialog()
        self.storyName = choice(self.proxy.stories.keys())
        self.Nao.say("Je vais vous raconter "+self.storyName)
        self.Nao.memoryProxy.subscribeToEvent("FrontTactilTouched", "NaoStory", "onFrontTactilTouched")
        histoire = self.proxy.getStory(self.storyName, PATH.PATH_DB+'/storyfile').split('. ')
        ctr = 0
        self.flag = 1
        while ctr < len(histoire):
            self.Nao.say(histoire[ctr])
            if not self.flag:
                break
            ctr += 1
        self.Nao.say("Aimez-vous cette histoire ?")
        self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoStory", "onWordRecognized")
        
    # Risen when the head is touched, for stopping the story telling    
    def onFrontTactilTouched(self, *_args):
        print "stopped story"
        if "NaoStory" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoStory")
        self.flag = 0

    # Say if the user liked the story and go back to menu
    def onWordRecognized(self, key, value, message):
        reco = False
        if "NaoStory" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoStory")
            reco = True
        if "NaoStory" in self.Nao.memoryProxy.getSubscribers("FrontTactilTouched"):
            self.Nao.memoryProxy.unsubscribeToEvent("FrontTactilTouched", "NaoStory")
            reco = True
        if reco:
            ok = False
            print "Word Recognized value = " + str(value) # value = [phrase, confidence]
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                # Nao says the word understood
                if word == "oui":
                    self.Nao.say("Je vous remercie")
                elif word == "non":
                    self.Nao.say("C'est dômmage")
                else:
                    ok = False
                    print "Unknown option"
                    
            if not ok:
                self.Nao.say("Repetez, s'il vous plaît")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoStory", "onWordRecognized")
            else:
                self.Nao.activateDialog()
                self.Nao.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)
