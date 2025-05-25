import pygame
import random

pygame.init()
pygame.mixer.init()

# Screen
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Color Catch Game")
clock = pygame.time.Clock()

# Load background music
pygame.mixer.music.load(r"c:\Users\pavan\Downloads\game-music-loop-7-145285.mp3")
pygame.mixer.music.play(-1)  # Loop forever

# Colors
COLORS = {
    "RED": (255, 0, 0),
    "GREEN": (0, 200, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0)
}
COLOR_NAMES = list(COLORS.keys())
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 36)

class Bucket:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.rect = pygame.Rect(250, 450, self.width, self.height)
        self.color_name = random.choice(COLOR_NAMES)

    def draw(self):
        pygame.draw.rect(screen, COLORS[self.color_name], self.rect)
        label = font.render(self.color_name, True, BLACK)
        screen.blit(label, (self.rect.x + 10, self.rect.y - 25))

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(self.rect.x, 600 - self.width))

    def change_color(self):
        self.color_name = random.choice(COLOR_NAMES)

class Block:
    def __init__(self, speed):
        self.is_power = False
        self.color_name = random.choice(COLOR_NAMES)
        self.color = COLORS[self.color_name]
        self.rect = pygame.Rect(random.randint(0, 570), 0, 30, 30)
        self.speed = speed
        if random.random() < 0.1:  # 10% chance to spawn power-up
            self.is_power = True
            self.color_name = "POWER"
            self.color = (0, 255, 255)  # Cyan

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.is_power:
            p = font.render("P", True, BLACK)
            screen.blit(p, (self.rect.x + 5, self.rect.y + 2))

def draw_text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, BLACK)
    rect = render.get_rect(center=(x, y))
    screen.blit(render, rect)

def run_game():
    bucket = Bucket()
    blocks = []
    score = 0
    lives = 5
    block_timer = 0
    fall_speed = 4
    slow_timer = 0

    running = True
    while running:
        screen.fill(WHITE)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            bucket.move(-6)
        if keys[pygame.K_RIGHT]:
            bucket.move(6)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Gradually increase fall speed
        fall_speed = 4 + score // 5
        if slow_timer > 0:
            slow_timer -= 1
            fall_speed = max(2, fall_speed - 3)

        # Spawn blocks
        block_timer += 1
        if block_timer > 40:
            blocks.append(Block(fall_speed))
            block_timer = 0

        # Move and draw blocks
        for block in blocks[:]:
            block.move()
            block.draw()

            if block.rect.colliderect(bucket.rect):
                if block.is_power:
                    power = random.choice(["CLEAR", "SLOW"])
                    if power == "CLEAR":
                        blocks = [b for b in blocks if b is block]
                    elif power == "SLOW":
                        slow_timer = 180  # ~3 seconds at 60 FPS
                elif block.color_name == bucket.color_name:
                    score += 1
                    bucket.change_color()
                else:
                    lives -= 1
                blocks.remove(block)

            elif block.rect.y > 500:
                if not block.is_power and block.color_name == bucket.color_name:
                    lives -= 1
                    bucket.change_color()
                blocks.remove(block)

        bucket.draw()

        draw_text(f"Score: {score}", 30, 80, 30)
        draw_text(f"Lives: {lives}", 30, 520, 30)
        if slow_timer > 0:
            draw_text("SLOW!", 40, 300, 50)

        if lives <= 0:
            draw_text("Game Over!", 50, 300, 200)
            draw_text("Press any key to exit", 30, 300, 250)
            pygame.display.flip()
            pygame.time.wait(500)
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                        wait = False
            break

        pygame.display.flip()
        clock.tick(60)

run_game()
pygame.quit()
