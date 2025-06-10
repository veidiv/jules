import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Objects - With Lives!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
# GAMEOVER_BG_COLOR = (50, 50, 50, 200) # Semi-transparent dark for game over overlay - Not used yet

REGULAR_OBJECT_COLORS = [RED, GREEN, BLUE]
PLAYER_FALLBACK_COLOR = WHITE
BACKGROUND_COLOR = BLACK
TEXT_COLOR = WHITE
GAMEOVER_TEXT_COLOR = (255, 50, 50)


# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Fonts
try:
    font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 72) # Larger font for Game Over
    restart_font = pygame.font.Font(None, 48) # Font for restart message
except Exception:
    font = pygame.font.SysFont("arial", 30)
    game_over_font = pygame.font.SysFont("arial", 60)
    restart_font = pygame.font.SysFont("arial", 40)


# --- Sprite & Sound Loading ---
PLAYER_SPRITE_WIDTH = 100
PLAYER_SPRITE_HEIGHT = 40
OBJECT_SPRITE_WIDTH = 30
OBJECT_SPRITE_HEIGHT = 30

def load_image_sprite(filename, dimensions):
    try:
        image_path = filename
        if not os.path.exists(image_path): raise FileNotFoundError(f"Sprite file not found: {image_path}")
        image = pygame.image.load(image_path)
        image = image.convert_alpha() if filename.lower().endswith(".png") else image.convert()
        image = pygame.transform.scale(image, dimensions)
        return image
    except Exception as e: print(f"Error loading sprite '{filename}': {e}")
    return None

player_image = load_image_sprite("player.png", (PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT))
object_images = {
    "REGULAR": load_image_sprite("object_regular.png", (OBJECT_SPRITE_WIDTH, OBJECT_SPRITE_HEIGHT)),
    "BONUS": load_image_sprite("object_bonus.png", (OBJECT_SPRITE_WIDTH, OBJECT_SPRITE_HEIGHT))
}

def load_sound_effect(filename):
    try:
        sound_path = filename
        if not os.path.exists(sound_path): raise FileNotFoundError(f"Sound file not found: {sound_path}")
        sound = pygame.mixer.Sound(sound_path)
        return sound
    except Exception as e: print(f"Error loading sound '{filename}': {e}")
    return None

catch_sound = load_sound_effect("catch.wav")
bonus_catch_sound = load_sound_effect("bonus_catch.wav")
level_up_sound = load_sound_effect("level_up.wav")
miss_sound = load_sound_effect("miss.wav") # Sound for missing an object
game_over_sound = load_sound_effect("game_over.wav") # Sound for game over
# --- End Sprite & Sound Loading ---


# Player properties
player_width = PLAYER_SPRITE_WIDTH if player_image else 100
player_height = PLAYER_SPRITE_HEIGHT if player_image else 20
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10
PLAYER_SPEED = 7

# Game State
score = 0
level = 1
POINTS_PER_LEVEL = 100
lives = 3 # Player starts with 3 lives
game_over = False # Game state flag

ObjectType = {"REGULAR": "regular", "BONUS": "bonus"}

class FallingObject:
    def __init__(self, current_level_arg):
        self.width = OBJECT_SPRITE_WIDTH
        self.height = OBJECT_SPRITE_HEIGHT
        self.level = current_level_arg
        self.image = None
        self.fallback_color = None
        self.determine_type_and_value()
        self.reset_position_and_speed(is_miss=False) # Initial reset is not a miss

    def determine_type_and_value(self):
        if random.random() < 0.15:
            self.obj_type = ObjectType["BONUS"]; self.image = object_images["BONUS"]; self.fallback_color = GOLD; self.points = 25
        else:
            self.obj_type = ObjectType["REGULAR"]; self.image = object_images["REGULAR"]; self.fallback_color = random.choice(REGULAR_OBJECT_COLORS); self.points = 10

    def reset_position_and_speed(self, is_miss=False): # Added is_miss flag
        global lives # Allow modification of global lives
        global game_over

        if is_miss and not game_over: # Only deduct life if it was a miss during active play
            lives -= 1
            if miss_sound: miss_sound.play()
            if lives <= 0:
                lives = 0 # Ensure lives don't go negative on display
                game_over = True
                if game_over_sound: game_over_sound.play()
                print("Game Over!") # Debug

        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(-SCREEN_HEIGHT // 2, 0) - self.height
        base_min_speed = 1 + self.level; base_max_speed = 3 + self.level
        self.speed = random.randint(base_min_speed, base_max_speed)
        if self.speed < 1: self.speed = 1
        if self.speed > 10: self.speed = 10 # Cap max speed

    def reinitialize(self): # Called when caught
        self.determine_type_and_value()
        self.reset_position_and_speed(is_miss=False) # Not a miss when caught

    def update_level(self, new_level): self.level = new_level

    def fall(self):
        if game_over: return # Stop falling if game is over
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.reset_position_and_speed(is_miss=True) # It's a miss

    def draw(self, surface):
        if self.image: surface.blit(self.image, (self.x, self.y))
        else: pygame.draw.rect(surface, self.fallback_color, (self.x, self.y, self.width, self.height))

    def get_rect(self): return pygame.Rect(self.x, self.y, self.width, self.height)

current_max_objects = 3
falling_objects = []
def manage_falling_objects(current_game_level, initial_setup=False):
    global current_max_objects
    current_max_objects = 3 + (current_game_level - 1) // 2
    if current_max_objects > 7: current_max_objects = 7

    if initial_setup: # Only on game start/restart, clear and create all
        falling_objects.clear()

    # Adjust incrementally or populate initially
    while len(falling_objects) > current_max_objects:
        falling_objects.pop()
    while len(falling_objects) < current_max_objects:
        falling_objects.append(FallingObject(current_game_level))

    # Ensure all objects (new or existing) have the correct level, especially after a full reset
    if initial_setup:
        for obj in falling_objects:
            obj.update_level(current_game_level) # Ensure level is set
            obj.reinitialize() # Ensure they get new positions/types for the new game


def reset_game_state():
    global score, level, lives, game_over, player_x
    score = 0
    level = 1
    lives = 3
    game_over = False
    player_x = (SCREEN_WIDTH - player_width) // 2 # Reset player position
    manage_falling_objects(level, initial_setup=True)


manage_falling_objects(level, initial_setup=True) # Initial population

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game_state()
            elif event.key == pygame.K_q:
                 running = False


    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]: player_x += PLAYER_SPEED

        if player_x < 0: player_x = 0
        if player_x > SCREEN_WIDTH - player_width: player_x = SCREEN_WIDTH - player_width

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        for obj in falling_objects:
            obj.fall()
            object_rect = obj.get_rect()
            if player_rect.colliderect(object_rect):
                score += obj.points
                if obj.obj_type == ObjectType["BONUS"] and bonus_catch_sound: bonus_catch_sound.play()
                elif catch_sound: catch_sound.play()
                obj.reinitialize()

                if score >= level * POINTS_PER_LEVEL:
                    level += 1
                    if level_up_sound: level_up_sound.play()
                    manage_falling_objects(level) # Adjust object count for new level
                    for existing_obj in falling_objects: # Ensure all objects know the new level
                        existing_obj.update_level(level)

    # --- Drawing ---
    screen.fill(BACKGROUND_COLOR)
    if not game_over:
        if player_image: screen.blit(player_image, player_rect.topleft)
        else: pygame.draw.rect(screen, PLAYER_FALLBACK_COLOR, player_rect)
        for obj in falling_objects: obj.draw(screen)
    else: # Game Over Screen
        game_over_text_surface = game_over_font.render("GAME OVER", True, GAMEOVER_TEXT_COLOR)
        final_score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
        restart_msg_surface = restart_font.render("Press 'R' to Restart or 'Q' to Quit", True, TEXT_COLOR)

        screen.blit(game_over_text_surface, (SCREEN_WIDTH // 2 - game_over_text_surface.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_msg_surface, (SCREEN_WIDTH // 2 - restart_msg_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    score_text_surface = font.render(f"Score: {score}", True, TEXT_COLOR)
    level_text_surface = font.render(f"Level: {level}", True, TEXT_COLOR)
    lives_text_surface = font.render(f"Lives: {lives}", True, TEXT_COLOR)
    screen.blit(score_text_surface, (10, 10))
    screen.blit(level_text_surface, (10, 40))
    screen.blit(lives_text_surface, (SCREEN_WIDTH - lives_text_surface.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
