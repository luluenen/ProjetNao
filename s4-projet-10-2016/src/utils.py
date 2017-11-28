import speech_recognition as sr
import wave
import sys
import socket
from os import path

# Recognize speech from a wav file using Google Speech Recognition
def speechRecognition(fname, lang='fr-FR'):
    """
        Recognizes speech from a wav file
        using Google Speech Recognition.
        fname : name of the file
        lang : language of the recording
        Returns the speech as a text;
        null if it does not recognizes it
        or if error.
    """
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), fname)
    r = sr.Recognizer()

    # Read the audio file
    try:
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)
    except IOError:
        print "File error"
        return None

    # Use Google Speech Recognition
    try:
        text = r.recognize_google(audio, language=lang)
        return text.encode("utf8")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return None

def isConnected(host="8.8.8.8", port=53, timeout=3):
    """
        Checks internet connection
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        Returns true if there is internet connection;
        false otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        pass
    return False
