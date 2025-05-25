import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Click the Circle")
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

# Load background music
pygame.mixer.music.load(r"c:\Users\pavan\Downloads\game-music-loop-7-145285.mp3")
pygame.mixer.music.play(-1)  # Loop forever

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

circle_radius = 30

def draw_text(text, size, x, y, center=True):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, BLACK)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(render, rect)
    return rect

def wait_for_click(rects):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
               
            if event.type == pygame.MOUSEBUTTONDOWN:
                for label, rect in rects.items():
                    if rect.collidepoint(event.pos):
                        return label
        pygame.display.flip()
        clock.tick(60)

def start_screen():
    screen.fill(WHITE)
    draw_text("Click the Circle", 50, 300, 100)
    start_btn = draw_text("Start Game", 40, 300, 200)
    pygame.display.flip()
    return wait_for_click({"start": start_btn}) == "start"

def game_over_screen(score):
    screen.fill(WHITE)
    draw_text("Game Over", 50, 300, 100)
    draw_text(f"Your Score: {score}", 40, 300, 160)
    play_btn = draw_text("Play Again", 35, 300, 230)
    quit_btn = draw_text("Quit", 35, 300, 280)
    pygame.display.flip()
    choice = wait_for_click({"play": play_btn, "quit": quit_btn})
    return choice == "play"

def run_game():
    score = 0
    misses = 0
    circle_pos = [random.randint(50, 550), random.randint(50, 350)]
    running = True

    # NEW: timing variables
    base_time_limit = 2000  # in milliseconds
    circle_spawn_time = pygame.time.get_ticks()

    while running:
        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, circle_pos, circle_radius)
        draw_text(f"Score: {score}", 30, 10, 10, center=False)
        draw_text(f"Misses: {misses}/5", 30, 10, 40, center=False)

        current_time = pygame.time.get_ticks()  # NEW: current time

        # NEW: calculate dynamic time limit (min 500ms)
        time_limit = max(500, base_time_limit - score * 100)

        if current_time - circle_spawn_time > time_limit:
            misses += 1
            if misses >= 5:
                break
            circle_pos = [random.randint(50, 550), random.randint(50, 350)]
            circle_spawn_time = pygame.time.get_ticks()  # reset timer

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                distance = ((mouse_pos[0] - circle_pos[0]) ** 2 + (mouse_pos[1] - circle_pos[1]) ** 2) ** 0.5
                if distance < circle_radius:
                    score += 1
                    circle_pos = [random.randint(50, 550), random.randint(50, 350)]
                    circle_spawn_time = pygame.time.get_ticks()  # NEW: reset timer on hit
                else:
                    misses += 1
                    if misses >= 5:
                        running = False

        pygame.display.flip()
        clock.tick(60)

    return score

# --- Game Loop ---
while True:
    if not start_screen():
        break
    score = run_game()
    if not game_over_screen(score):
        break

pygame.quit()
