#coding: utf8

from naoqi import ALModule
import time, sys

CONFIDENCE = 0.4
MAX_TIMES_RECOGNIZED = 3

class NaoRecognitionModule(ALModule):
    '''
        Nao Recognition
        Uses FaceDetection for recognizing and learning faces;
        PeoplePerception for noticing when the person focused has left
        or someone else arrives; and Tracker for tracking the focused person.
    '''
    personId = None

    def __init__(self, name, Nao):
        ALModule.__init__(self, name)
        self.Nao = Nao
        self.times_recognized = 0
        # Subscribe Events
        #self.Nao.memoryProxy.subscribeToEvent("PeoplePerception/JustArrived", "NaoRecognition", "onJustArrived")
        #self.Nao.memoryProxy.subscribeToEvent("PeoplePerception/PeopleDetected", "NaoRecognition", "onJustArrived")
        self.Nao.memoryProxy.subscribeToEvent("NewFaceDetected", "NaoRecognition", "onNewFaceDetected")

    def exit(self):
        if "NaoRecognition" in self.Nao.memoryProxy.getSubscribers("PeoplePerception/PeopleDetected"):
            self.Nao.memoryProxy.unsubscribeToEvent("PeoplePerception/PeopleDetected", "NaoRecognition")
        if "NaoRecognition" in self.Nao.memoryProxy.getSubscribers("PeoplePerception/JustArrived"):
            self.Nao.memoryProxy.unsubscribeToEvent("PeoplePerception/JustArrived", "NaoRecognition")
        if "NaoRecognition" in self.Nao.memoryProxy.getSubscribers("PeoplePerception/JustLeft"):
            self.Nao.memoryProxy.unsubscribeToEvent("PeoplePerception/JustLeft", "NaoRecognition")
        if "NaoRecognition" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoRecognition")
        self.Nao.memoryProxy.unsubscribeToEvent("NewFaceDetected", "NaoRecognition")
        ALModule.exit(self)

    def onJustArrived(self, key, value, message):
        """
            Callback function for PeopleDetected and JustArrived event.
            It only gets treated if the person that was taking into account in the population
            is no longer in front of the robot (no longer part of the population).
            
        """
        print "Just arrived"
        # If there is not a focused person
        if self.personId == None:
            arrived = False
            if "NaoRecognition" in self.Nao.memoryProxy.getSubscribers("PeoplePerception/PeopleDetected"):
                self.Nao.memoryProxy.unsubscribeToEvent("PeoplePerception/PeopleDetected", "NaoRecognition")
                arrived = True
            if "NaoRecognition" in self.Nao.memoryProxy.getSubscribers("PeoplePerception/JustArrived"):
                self.Nao.memoryProxy.unsubscribeToEvent("PeoplePerception/JustArrived", "NaoRecognition")
                arrived = True
            # Set person ID value
            if key == "PeoplePerception/PeopleDetected":
                self.personId = value[1][0][0]
            else:
                self.personId = value
            # Condition so the instructions are only run once
            # in case the event is risen twice at the same time
            if arrived:
                self.Nao.deactivateDialog()
                print "id", self.personId
                self.times_recognized = 0
                # Prepare the body for moving
                self.Nao.motion.wakeUp()
                self.Nao.motion.setIdlePostureEnabled("Body", True)
                # Track the face of the person focused
                self.Nao.tracker.registerTarget("People", self.personId)
                self.Nao.tracker.track("People")
                # Subscribe to JustLeft and FaceRecognition
                self.Nao.memoryProxy.subscribeToEvent("FaceDetected", "NaoRecognition", "onFaceDetected2")
                #self.Nao.memoryProxy.subscribeToEvent("PeoplePerception/JustLeft", "NaoRecognition", "onJustLeft")
        
    def onJustLeft(self, key, value, message):
        """
            Callback function for JustLeft event.
            Deletes the session and subscribes to events for recognizing people.
        """
        print "Just left", value
        # If the person that has left was the one being focused
        if ("NaoRecognition" in self.Nao.memoryProxy.getSubscribers("PeoplePerception/JustLeft")) and (value==self.personId):
            self.Nao.memoryProxy.unsubscribeToEvent("PeoplePerception/JustLeft", "NaoRecognition")
            #TODO Stop behaviors
            self.Nao.say("^start(animations/Stand/Gestures/Hey_1) Bye bye "+self.Nao.session.split('_')[0])
            # Remove the face from tracking
            self.Nao.tracker.stopTracker()
            self.Nao.tracker.unregisterAllTargets()
            # Reset the session values
            self.personId = None
            self.Nao.session = ""
            # Subscribe to JustArrive and PeopleDetected
            self.Nao.memoryProxy.subscribeToEvent("PeoplePerception/JustArrived", "NaoRecognition", "onJustArrived")
            self.Nao.memoryProxy.subscribeToEvent("PeoplePerception/PeopleDetected", "NaoRecognition", "onJustArrived")

    def onFaceDetected2(self, key, value, message):
        """
            Callback function for FaceDetected Event.
            If Nao recognizes the face, greets with name;
            if not, raises event NewFaceDetected.
        """  
        print "Face detected"
        #
        if ("NaoRecognition" in self.Nao.memoryProxy.getSubscribers("FaceDetected")) and (len(value)>0):
            self.Nao.memoryProxy.unsubscribeToEvent("FaceDetected", "NaoRecognition")
            extraInfo = value[1][0][1]
            time_filtered_reco_info = value[1][0]
            faceID = extraInfo[0] # ID number for the face
            scoreReco = extraInfo[1] # confidence of face recognition
            faceLabel = extraInfo[2] # name of recognized face

            print "ScoreReco", scoreReco
            if (not faceLabel) or (scoreReco < CONFIDENCE):
                if MAX_TIMES_RECOGNIZED < self.times_recognized:
                    # If does not recognize after MAX_TIMES_RECOGNIZED times
                    self.Nao.say("^start(animations/Stand/Gestures/BowShort_1) Je suis enchanté de faire votre connaissance. Je suis Nao.")
                    self.Nao.memoryProxy.raiseEvent("NewFaceDetected", 0)
                else:
                    # If does not recognize at first
                    self.times_recognized += 1
                    self.Nao.memoryProxy.subscribeToEvent("FaceDetected", "NaoRecognition", "onFaceDetected2")
            else:
                # Nao recognizes you
                self.Nao.say("^start(animations/Stand/Gestures/Hey_6) Bonjour, "+faceLabel.split('_')[0])
                # Insert into DB if does not exist
                if self.Nao.db_client.findPersonByName(faceLabel) == None:
                    self.Nao.db_client.insertPerson(faceLabel)
                self.Nao.session = faceLabel
                self.Nao.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)
            
    def onNewFaceDetected(self, *_args):
        """
            Callback function for NewFaceDetected Event.
            Asks for the user name and then asks for confirmation subscribing to event WordRecognized.
        """
        print "New face"
        self.Nao.deactivateDialog()
        self.Nao.say("Quel est votre nom ?")
        self.name = self.Nao.listen()
        print self.name
        # If he understands the name
        if self.name:
            self.Nao.say(self.name + ", n'est-ce pas?")
            self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoRecognition", "onWordRecognized")
        else:
            self.Nao.memoryProxy.raiseEvent("NewFaceDetected", 0)

    def onWordRecognized(self, key, value, message):
        """
            Callback function for WordRecognized Event.
            Confirms the name said by the user and then learns the face.
        """
        if "NaoRecognition" in self.Nao.memoryProxy.getSubscribers("WordRecognized"):
            self.Nao.memoryProxy.unsubscribeToEvent("WordRecognized", "NaoRecognition")
            ok = False
            print "Word Recognized value = " + str(value) # value = [phrase, confidence]
            # Confidence check
            if value[1] > CONFIDENCE:
                ok = True
                word = value[0]
                
                if word == "oui":
                    self.Nao.say("Regardez-moi et ne bougez pas s'il vous plaît")
                    # Save the name of the person as name_number
                    i = 1
                    nameOk = self.name+"_"+str(i)
                    while nameOk in self.Nao.fd.getLearnedFacesList():
                        i += 1
                        nameOk = self.name+"_"+str(i)
                    self.Nao.learnFace(nameOk)
                    self.Nao.session = nameOk
                    self.Nao.say("Enchanté, "+self.name)
                    self.Nao.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)
                    
                    # Insert into DB
                    self.Nao.db_client.insertPerson(nameOk)
                elif word == "non":
                    self.Nao.memoryProxy.raiseEvent("NewFaceDetected", 0)
                else:
                    ok = False      
            if not ok:
                self.Nao.say("Je n'ai pas compris")
                self.Nao.memoryProxy.subscribeToEvent("WordRecognized", "NaoRecognition", "onWordRecognized")
