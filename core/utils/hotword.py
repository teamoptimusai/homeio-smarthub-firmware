import speech_recognition as sr
import os

hostwords = {
    "hey google": "hey google",
}


class HotwordDetector:
    # given a wav file and a hotword, return True if the hotword is detected using snowboy hotword detector
    def __init__(self, hotword):
        self.hotword = hotword
        self.recognizer = sr.Recognizer()

    def detect(self, audio):
        self.recognizer.snowboy_wait_for_hot_word(
            audio, self.hotword, sensitivity=0.5)


if __name__ == "__main__":
    hotword_detector = HotwordDetector('hey google!')
