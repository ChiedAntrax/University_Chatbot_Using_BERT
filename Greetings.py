import pyttsx3
import datetime

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def greetings():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        text_to_speech("good morning!")
    elif hour>12 and hour <=18:
        text_to_speech("good afternoon!")
    else:
        text_to_speech("good evening!")

    text_to_speech("please tell me, how can I help you") 
