import pygame
import random


# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Dodge the Falling Objects")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DANGER = (200, 0, 0)
PLAYER = (0, 100, 255)
INVINCIBLE_COLOR = (255, 215, 0)
SLOW_COLOR = (100, 100, 255)

# Fonts
font = pygame.font.SysFont(None, 36)

# Load sounds
try:
    dodge_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\game-over-arcade-6435.mp3")
    hit_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\90s-game-ui-6-185099.mp3")
    powerup_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\winner-bell-game-show-91932.mp3")
except:
    dodge_sound = hit_sound = powerup_sound = None

# Power-up types
POWER_TYPES = ["INVINCIBLE", "SLOW"]

# Player
player = pygame.Rect(275, 450, 50, 20)

# Obstacle class
class Obstacle:
    def __init__(self, speed):
        self.rect = pygame.Rect(random.randint(0, 570), -30, 30, 30)
        self.speed = speed
        self.is_power = False
        self.type = None

        if random.random() < 0.1:  # 10% chance to be a power-up
            self.is_power = True
            self.type = random.choice(POWER_TYPES)
            self.color = INVINCIBLE_COLOR if self.type == "INVINCIBLE" else SLOW_COLOR
        else:
            self.color = DANGER

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def draw_text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, BLACK)
    screen.blit(render, (x, y))

def run_game():
    running = True
    lives = 3
    score = 0
    spawn_timer = 0
    obstacles = []

    invincible = 0
    slow_fall = 0

    while running:
        screen.fill(WHITE)
        speed = 4 + score // 5
        fall_speed = speed - 2 if slow_fall > 0 else speed

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
              

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 6
        if keys[pygame.K_RIGHT]:
            player.x += 6
        player.x = max(0, min(player.x, 600 - player.width))

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 30:
            obstacles.append(Obstacle(fall_speed))
            spawn_timer = 0

        # Update and draw obstacles
        for obs in obstacles[:]:
            obs.move()
            obs.draw()

            if obs.rect.colliderect(player):
                if obs.is_power:
                    if powerup_sound: powerup_sound.play()
                    if obs.type == "INVINCIBLE":
                        invincible = 180
                    elif obs.type == "SLOW":
                        slow_fall = 180
                elif invincible > 0:
                    if dodge_sound: dodge_sound.play()
                else:
                    if hit_sound: hit_sound.play()
                    lives -= 1
                    if lives <= 0:
                        running = False
                obstacles.remove(obs)
            elif obs.rect.top > 500:
                if not obs.is_power:
                    score += 1
                obstacles.remove(obs)

        # Decrement timers
        if invincible > 0:
            invincible -= 1
        if slow_fall > 0:
            slow_fall -= 1

        # Draw player
        color = INVINCIBLE_COLOR if invincible > 0 else PLAYER
        pygame.draw.rect(screen, color, player)

        # Draw HUD
        draw_text(f"Score: {score}", 30, 10, 10)
        draw_text(f"Lives: {lives}", 30, 500, 10)
        if invincible > 0:
            draw_text("INVINCIBLE!", 25, 230, 10)
        if slow_fall > 0:
            draw_text("SLOW MODE", 25, 230, 40)

        pygame.display.flip()
        clock.tick(60)

    # Game Over screen
    screen.fill(WHITE)
    draw_text("GAME OVER", 50, 180, 200)
    draw_text(f"Final Score: {score}", 40, 180, 260)
    draw_text("Press any key to quit", 30, 170, 320)
    pygame.display.flip()
    pygame.time.wait(1000)

    # Wait for key
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                pygame.quit()
                return

# Run the game
run_game()
