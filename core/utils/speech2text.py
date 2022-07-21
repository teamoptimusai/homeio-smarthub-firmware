import speech_recognition as sr


class Speech2Text:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize(self, audio):
        with sr.AudioFile(audio) as source:
            audio = self.recognizer.record(source)
        try:
            return self.recognizer.recognize_sphinx(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that"

class Wav2Vec:
    def __init__(self):
        pass

    def recognize(self, audio):
        pass




if __name__ == "__main__":
    speech2text = Speech2Text()
    sentence = speech2text.recognize('test.wav')
    print(sentence)
