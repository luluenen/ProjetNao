#coding: utf8

from naoqi import ALBroker, ALModule, ALProxy
from utils import *
from filetransfer import *
from msvcrt import getch
import time
import sys
import pdb
import PATH

PATH.addPaths()

from NaoDatabaseServer import *
from NaoDatabaseClient import *

# Import Nao Modules
from NaoGUI import *
from NaoMultimediaModule import *
from NaoRecognitionModule import *
from NaoMusicModule import *
from NaoInformationModule import *
from NaoNewsModule import *
from NaoTvModule import *
from NaoStoryModule import *

# Global variable to store module instances
CONFIDENCE = 0.45
NaoRecognition = None
NaoMultimedia = None
NaoMusic = None
NaoNews = None
NaoInformation = None
NaoTv = None

class NaoBasic():
    """
        Nao main class.
        Called for making any centrilized action.
    """
    session = ""
    
    def __init__(self, port, pip="127.0.0.1", login="nao", pswrd="nao"):
        self.pip = pip
        self.port = port

        # Connect to NaoDatabase
        # For the moment we run server and client in this part,
        # but for the future plan is to have a centralized db
        # so this object should also receive the server ip
        self.db_server = NaoDatabaseServer(PATH.PATH_DB)
        self.db_client = NaoDatabaseClient('localhost', 27017)

        # Establish FTP connection
        self.ftp = FileTransfer(self.pip)
        self.ftp.login(login, pswrd)

        # Create Proxies
        self.memoryProxy = ALProxy("ALMemory", self.pip, self.port)
        self.motion = ALProxy('ALMotion', self.pip, self.port)
        self.rp = ALProxy("ALRobotPosture", self.pip, self.port)
        self.tts2 = ALProxy('ALTextToSpeech', self.pip, self.port)
        self.tts = ALProxy('ALAnimatedSpeech', self.pip, self.port)
        self.dialog = ALProxy('ALDialog', self.pip, self.port)
        self.ar = ALProxy("ALAudioRecorder", self.pip, self.port)
        self.ap = ALProxy("ALAudioPlayer", self.pip, self.port)
        self.sr = ALProxy("ALSpeechRecognition", self.pip, self.port)
        self.fd = ALProxy("ALFaceDetection", self.pip, self.port)
        self.pp = ALProxy("ALPeoplePerception", self.pip, self.port)
        self.tracker = ALProxy("ALTracker", self.pip, self.port)
                
        # Event Declarations
        self.memoryProxy.declareEvent("NewFaceDetected")
        self.memoryProxy.declareEvent("NaoMultimediaRequest")
        self.memoryProxy.declareEvent("MusicRequest")
        self.memoryProxy.declareEvent("NewsRequest")
        self.memoryProxy.declareEvent("InformationRequest")
        self.memoryProxy.declareEvent("TvRequest")
        self.memoryProxy.declareEvent("StoryRequest")
        self.memoryProxy.declareEvent("AmbiguosRequest") # InformationModule
        self.memoryProxy.declareEvent("SearchRequest") # InformationModule
        self.memoryProxy.declareEvent("SearchProgramRequest") # TvModule
        self.memoryProxy.declareEvent("MusicFinished") # MusicModule
        self.memoryProxy.declareEvent("PlayMusicRequest") #MusicModule

        self.stopAll()

        # Voice settings
        self.tts2.setLanguage("French")
        self.tts2.setParameter("speed", 0.5)
        
        # Definition of keywords
        self.sr.pause(True)
        self.sr.setLanguage("French")
        self.sr.setVocabulary(["oui", "non"], False) #"musique", "journal", "info", "télé", "histoire", 
        self.sr.pause(False)

        # * WIP * instead of using keywords to launch the different
        # functionalities, we are implementing a dialog
        # Dialog loading topics
        self.deactivateDialog()
        if 'MenuMultimedia' in self.dialog.getActivatedTopics():
            self.dialog.deactivateTopic('MenuMultimedia')
            self.dialog.unloadTopic('MenuMultimedia')
        self.ftp.uploadFile('dialog\MenuMultimedia.top')
        self.dialog.setLanguage("French")
        self.dialog.setASRConfidenceThreshold(0.45)
        self.topic = self.dialog.loadTopic('/home/nao/dialog\MenuMultimedia.top')
        self.dialog.activateTopic(self.topic)

        # Body settings
        self.motion.setSmartStiffnessEnabled(True)
        self.fd.setTrackingEnabled(True)
        # Prepare the body for moving
        self.motion.wakeUp()
        self.motion.setIdlePostureEnabled("Body", True)

        # People perception settings
        self.pp.setMaximumDetectionRange(1.5) # in meters
        #self.pp.setMovementDetectionEnabled(True)
        self.pp.setTimeBeforeVisiblePersonDisappears(10.0)
        self.pp.setTimeBeforePersonDisappears(10.0)
        
        # Create Broker for mudules 
        self.myBroker = ALBroker("myBroker",
           "0.0.0.0",   # listen to anyone
           0,           # find a free port and use it
           pip,         # parent broker IP
           port)        # parent broker port

        # Creating Nao Modules
        global NaoMultimedia, NaoRecognition, NaoMusic, NaoInformation, NaoNews, NaoTv, NaoStory
        NaoMultimedia = NaoMultimediaModule("NaoMultimedia", self)
        NaoRecognition = NaoRecognitionModule("NaoRecognition", self)
        NaoMusic = NaoMusicModule("NaoMusic", self)
        NaoInformation = NaoInformationModule("NaoInformation", self)
        NaoNews = NaoNewsModule("NaoNews", self)
        NaoTv = NaoTvModule("NaoTv", self)
        NaoStory = NaoStoryModule("NaoStory", self)

        self.memoryProxy.raiseEvent("NaoMultimediaRequest", 0)

    def learnFace(self, name):
        # For not duplicated names
        new_name = name+'_1'
        ind = 2
        while new_name in self.fd.getLearnedFacesList():
            new_name = name+'_'+str(ind)
            ind += 1
        name = new_name

        # run Learn face until succesful
        while True:
            result = self.fd.learnFace(name)
            if result:
                print "learned face", name
                break

    def move(self, (x,y,z)):
        self.motion.moveTo(x,y,z)

    def say(self, text, lang="French"):
        for subs in self.memoryProxy.getSubscribers("WordRecognized"):
            if subs not in ["ALAnimatedSpeech", "ALChoregraph"]:
                self.memoryProxy.unsubscribeToEvent("WordRecognized", subs)
        self.tts.say(text)

    def record(self, fname="recordout.wav", seg=4):
        # Records voice
        print "started recording"
        self.ap.post.playFile("/usr/share/naoqi/wav/begin_reco.wav")
        self.ar.stopMicrophonesRecording()
        self.ar.startMicrophonesRecording('/home/nao/recordout.wav', "wav", 48000, (0, 1, 0, 0))
        time.sleep(seg)
        self.ar.stopMicrophonesRecording()
        print "stopped recording"

    def listen(self, fname="recordout.wav", seg=4):
        """
            Records and recognizes voice.
            returns text understood; none if didn't get anything
        """
        # Records
        self.record(fname, seg)
        # Downloads recorded file from Nao
        self.ftp.downloadFile(fname)
        # Pass recorded file to SpeechRecognition
        try:
            text = speechRecognition(fname)
            self.ftp.deleteFile(fname)
            return text
        except Exception:
            return None

    def play(self, fname):
        fileId = self.ap.post.playFile(fname)
        while True:
            if not self.ap.isRunning(fileId):
                print "finished playing"
                self.memoryProxy.raiseEvent("MusicFinished", 0)
                break

    def stopAll(self):
        self.ap.stopAll()

    def activateDialog(self):
        try:
            self.dialog.subscribe("NaoMultimediaModule")
        except Exception:
            pass

    def deactivateDialog(self):
        try:
            self.dialog.unsubscribe("NaoMultimediaModule")
        except Exception:
            pass

    def quit(self):
        #TODO Stop behaviors
        self.stopAll()
        self.motion.rest()

        # Dialog closing
        self.dialog.deactivateTopic(self.topic)
        self.dialog.unloadTopic(self.topic)
        self.deactivateDialog()
        
        self.myBroker.shutdown()
        self.db_client.stopClient()
        self.db_server.stopServer()
        self.ftp.close()
        
        if os.path.isfile("recordout.wav"):
            os.remove("recordout.wav")
 
if __name__ == "__main__":

    gui = NaoGUI()

    Nao = None
    if gui.values:
        Nao = NaoBasic(gui.values["port"], gui.values["ip"], gui.values["login"], gui.values["password"])
        
    try:
        while True:
            key = ord(getch())
            if key == 27: #ESC
                raise KeyboardInterrupt()
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        if Nao:
            Nao.quit()        
        sys.exit(0)
