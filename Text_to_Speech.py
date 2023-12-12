import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def display_subtitle(subtitle):
    print("Subtitle:", subtitle)

if __name__ == "__main__":
    text = input("Enter the text to convert to speech: ")
    text_to_speech(text)
