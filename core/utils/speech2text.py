import speech_recognition as sr


class Speech2Text:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    def recognize(self, audio):
        with sr.AudioFile(audio) as source:
            audio = self.recognizer.record(source)
        try:
            return self.recognizer.recognize_sphinx(audio)
        except:
            return Exception("Could not understand audio")