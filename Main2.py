import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import pandas as pd
from Text_to_Speech import text_to_speech
from Speech_recognition import recognize_speech
import speech_recognition as sr
from queue import Queue
from Greetings import greetings
import tkinter as tk
from tkinter import messagebox
import requests
import io
import sys
import subprocess
from subprocess import Popen, PIPE
import time

last_query_timestamp = time.time()

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def start_gui_process():
    global the_other_process
    the_other_process = subprocess.Popen(['python', 'AnimOld.py'])
    
def stop_gui_process():
    global the_other_process
    if the_other_process:
        the_other_process.terminate()
        the_other_process = None
        
def start_gui_process1():
    global the_other_process1
    the_other_process1 = subprocess.Popen(['python', 'OldAnim.py'])
    
def stop_gui_process1():
    global the_other_process1
    if the_other_process1:
        the_other_process1.terminate()
        the_other_process1 = None
        
start_gui_process()

recognizer = sr.Recognizer()

# Define the wakeword
WAKEWORD = "kia wake up"

# Initialize the queue
wakeword_queue = Queue()

# Define a timeout duration (in seconds)
TIMEOUT_DURATION = 5

def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        response.raise_for_status()
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False


def show_no_internet_dialog():
    messagebox.showinfo("No Internet Connection", "Please check your internet connection.")

def detect_wakeword():
    # Check internet connection
    if not check_internet_connection():
        print("No internet connection.")
        show_no_internet_dialog()
        return

    # Rest of your existing code remains unchanged
    with sr.Microphone() as source:
        print("Listening for the wakeword...")
        audio = recognizer.listen(source)

    # Recognize the wakeword
    try:
        print("Recognizing the wakeword...")
        recognized_text = recognizer.recognize_google(audio)
        if recognized_text.lower() == WAKEWORD:
            print("Wakeword detected!")

            wakeword_queue.put(True)
        else:
            print("Wakeword not detected.")
            wakeword_queue.put(False)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        wakeword_queue.put(False)
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        wakeword_queue.put(False)

def initialize_model_and_tokenizer(model_name):
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def answer_question(question, context, model, tokenizer):
    input_text = question + " " + context
    inputs = tokenizer(input_text, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    
    # Get the most likely answer
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1  # Add 1 to include the end token
    
    # Decode the answer using the tokenizer
    answer_tokens = inputs["input_ids"][0][start_index:end_index]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)
    
    # Combine with the original context
    answer = context.replace("[MASK]", answer)
    
    return answer

# Load the dataset
data = pd.read_csv("processed_university_chatbot_dataset.csv")

# Initialize model and tokenizer
model_name = "fine_tuned_qa_model"
chatbot_model, chatbot_tokenizer = initialize_model_and_tokenizer(model_name)

def main_process():
    
    global last_query_timestamp

    try:
        # user_question = input("Ask me a question (or type 'exit' to end): ")
        user_question = recognize_speech("Listening...")

        if user_question.lower() == 'goodbye':
            
            text_to_speech("Thank you have a nice day!")
            stop_gui_process1()
            start_gui_process()
            
            return main_loop()

        
        relevant_rows = data[data['question'].str.contains(user_question, case=False)]

        if not relevant_rows.empty:
            
            relevant_row = relevant_rows.iloc[0]
            context = relevant_row['text']

            answer = answer_question(user_question, context, chatbot_model, chatbot_tokenizer)

            print("Answer:", answer)
            text_to_speech(answer)
            

            last_query_timestamp = time.time()

        else:
            print("No relevant passage found for the question.")
            
            text_to_speech("I'm sorry, I couldn't find a relevant answer.")

    except Exception as e:
        print(f"Error during main process: {e}")
        
        text_to_speech("I encountered an error while processing your request.")




should_keep_running = True

def main_loop():
    global should_keep_running, last_query_timestamp

    while should_keep_running:
        detect_wakeword()

        if not wakeword_queue.empty():
            if wakeword_queue.get():

                stop_gui_process()
                start_gui_process1()

                greetings()
                
                
                while True:
                    main_process()

                    if time.time() - last_query_timestamp > 180:
                        print("No queries for 3 minutes. Returning to main loop.")
                        stop_gui_process1()
                        start_gui_process()
                        return main_loop()
               
            else:
                print("Wakeword not detected.")
        else:
            print("No detection in the queue.")

# Start the main loop
main_loop()


if __name__ == "__main__":
    detect_wakeword()
    
    the_other_process = subprocess.Popen(['python', 'AnimOld.py'])

    if check_internet_connection():
        greetings()
        while True:
            main_process()

            if time.time() - last_query_timestamp > 180:
                print("No queries for 3 minutes. Exiting the program.")
                break
    else:
        show_no_internet_dialog()