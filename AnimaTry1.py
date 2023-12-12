import pygame
import threading
import speech_recognition as sr
from queue import Queue

# Initialize Pygame
pygame.init()

# Set up sprites
class Sprite(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        super().__init__()
        self.images = images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))  # Center the sprite

    def update(self):
        self.index = (self.index + 1) % len(self.images)
        self.image = self.images[self.index]

# Load sprite images
sprite1_images = [pygame.image.load('SLEEP1.png')]
sprite2_images = [pygame.image.load('Mata1.png'), pygame.image.load('Mata2.png')]

# Create sprite instances
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

center_x = screen_width // 2
center_y = screen_height // 2

sprite1 = Sprite(sprite1_images, center_x, center_y)
sprite2 = Sprite(sprite2_images, center_x, center_y)

# Set up clock
clock = pygame.time.Clock()

# Set up speech recognition
recognizer = sr.Recognizer()

# Global variable to control the main loop
running = True

# Custom event for animation switch
ANIMATION_SWITCH_EVENT = pygame.USEREVENT + 1

# Create Pygame windows in fullscreen
flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
window1 = pygame.display.set_mode((0, 0), flags)
window2 = pygame.display.set_mode((0, 0), flags)

# Create sprite groups for each window
all_sprites1 = pygame.sprite.Group(sprite1)
all_sprites2 = pygame.sprite.Group(sprite2)

# Function to run speech recognition in a separate thread

# Define the wakeword
WAKEWORD = "wakeup"

# Initialize the queue
wakeword_queue = Queue()

# Define a timeout duration (in seconds)
TIMEOUT_DURATION = 5



def detect_wakeword():
    # Listen for the wakeword
    with sr.Microphone() as source:
        print("Listening for the wakeword...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Recognize the wakeword
    try:
        print("Recognizing the wakeword...")
        recognized_text = recognizer.recognize_google(audio)
        if 'kia wake up' in recognized_text:
            print("Wakeword detected!")
            
            wakeword_queue.put(True)
        elif 'goodbye' in recognized_text:
            print("Wakeword not detected.")
            wakeword_queue.put(False)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        wakeword_queue.put(False)
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        wakeword_queue.put(False)

def speech_recognition_thread():
    global running  # Declare 'running' as a global variable
    while running:
        detect_wakeword()

        if not wakeword_queue.empty():
            if wakeword_queue.get():
                pygame.event.post(pygame.event.Event(ANIMATION_SWITCH_EVENT))
               
            else:
                print("Wakeword not detected.")
        else:
            print("No detection in the queue.")
            

# Create and start the speech recognition thread
speech_thread = threading.Thread(target=speech_recognition_thread)
speech_thread.start()

# Game loop
current_window = 1  # Variable to track the currently visible window
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ANIMATION_SWITCH_EVENT:
            # Switch sprite animations
            if current_window == 1:
                current_window = 2
            else:
                current_window = 1

    if current_window == 1:
        window1.fill((255, 255, 255))
        all_sprites1.update()
        all_sprites1.draw(window1)
        pygame.display.flip()
    else:
        window2.fill((255, 255, 255))
        all_sprites2.update()
        all_sprites2.draw(window2)
        pygame.display.flip()

    clock.tick(2)  # Adjust the frame rate as needed (e.g., 30 frames per second)

pygame.quit()


