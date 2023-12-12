import speech_recognition as sr

def recognize_speech(prompt="Listening..."):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10)  # Increase the timeout to 10 seconds

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

'''
if __name__ == "__main__":
    recognize_speech()  # Test the function without arguments
'''
