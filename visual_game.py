import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OBJECT_COLORS = [RED, GREEN, BLUE] # List of possible object colors
PLAYER_COLOR = WHITE
BACKGROUND_COLOR = BLACK
TEXT_COLOR = WHITE

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Font for score
try:
    score_font = pygame.font.Font(None, 36)
except Exception:
    score_font = pygame.font.SysFont("arial", 30)

# Player properties
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 20
player_x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
PLAYER_SPEED = 7

# Score
score = 0

# Falling Object Class
class FallingObject:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(-SCREEN_HEIGHT, 0) - self.height # Start at various heights above screen
        self.speed = random.randint(2, 6)
        self.color = random.choice(OBJECT_COLORS) # Assign a random color

    def fall(self):
        self.y += self.speed
        # If object goes off screen (missed)
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Game settings for multiple objects
MAX_OBJECTS = 5  # Maximum number of objects on screen
falling_objects = [] # List to hold falling object instances

# Function to add new objects if below MAX_OBJECTS
# This function is good for future use if we want to dynamically add objects
# For now, we initialize them all at the start and reset them.
# def add_new_object():
#     if len(falling_objects) < MAX_OBJECTS:
#         falling_objects.append(FallingObject())

# Initialize objects
for _ in range(MAX_OBJECTS):
    # add_new_object() # Using direct append for initial population
    falling_objects.append(FallingObject())


# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED

    # Keep player within screen boundaries
    if player_x < 0:
        player_x = 0
    if player_x > SCREEN_WIDTH - PLAYER_WIDTH:
        player_x = SCREEN_WIDTH - PLAYER_WIDTH

    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Update and process falling objects
    for obj in falling_objects: # Iterate directly, as we are resetting, not removing
        obj.fall()

        # Collision detection
        object_rect = obj.get_rect()
        if player_rect.colliderect(object_rect):
            score += 10
            obj.reset() # Reset the object after being caught


    # Drawing code
    screen.fill(BACKGROUND_COLOR)

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Draw all falling objects
    for obj in falling_objects:
        obj.draw(screen)

    # Draw score
    score_text_surface = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text_surface, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
