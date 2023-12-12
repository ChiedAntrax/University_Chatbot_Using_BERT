import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Sprite Animation")

# Set the title of the window
pygame.display.set_caption("Sprite Animation")

# Load sprites
sprites = [
    pygame.image.load("SLEEP1.png"),
    pygame.image.load("SLEEP2.png")
]
sprites = [pygame.transform.scale(sprite, (width, height)) for sprite in sprites]

# Set up variables for animation
fps = 2
clock = pygame.time.Clock()
frame = 0
sprite_speed = 1  # Adjust the speed of the animation

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Update animation frame
    frame += sprite_speed
    if frame >= len(sprites):
        frame = 0

    # Draw the current frame
    screen.fill((255, 255, 255))  # Fill the screen with a white background
    screen.blit(sprites[int(frame)], (0, 0))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
