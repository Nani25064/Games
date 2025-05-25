import pygame
import random

pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Load sound effects
success_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\winner-bell-game-show-91932.mp3")
fail_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\beep-329314.mp3")

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Keyboard Reaction Game")
font = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

directions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
key_map = {
    'LEFT': pygame.K_LEFT,
    'RIGHT': pygame.K_RIGHT,
    'UP': pygame.K_UP,
    'DOWN': pygame.K_DOWN
}

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

def run_game():
    score = 0
    misses = 0
    running = True

    prompt = random.choice(directions)
    prompt_time = pygame.time.get_ticks()
    reaction_times = []

    base_time_limit = 2000  # ms

    while running:
        screen.fill(WHITE)

        draw_text(f"Press: {prompt}", 60, 300, 120)
        draw_text(f"Score: {score}", 30, 10, 10, center=False)
        draw_text(f"Misses: {misses}/5", 30, 10, 40, center=False)

        current_time = pygame.time.get_ticks()

        # Dynamic time limit: harder as score increases
        time_limit = max(800, base_time_limit - score * 100)

        # Timeout
        if current_time - prompt_time > time_limit:
            fail_sound.play()
            misses += 1
            prompt = random.choice(directions)
            prompt_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                reaction = current_time - prompt_time
                if event.key == key_map[prompt]:
                    success_sound.play()
                    score += 1
                    reaction_times.append(reaction)
                else:
                    fail_sound.play()
                    misses += 1
                prompt = random.choice(directions)
                prompt_time = pygame.time.get_ticks()

        if misses >= 5:
            running = False

        pygame.display.flip()
        clock.tick(60)

    # Game Over Screen
    screen.fill(WHITE)
    draw_text("Game Over", 60, 300, 100)
    draw_text(f"Score: {score}", 40, 300, 160)
    if reaction_times:
        avg = sum(reaction_times) / len(reaction_times)
        draw_text(f"Avg Reaction: {avg:.0f} ms", 35, 300, 210)
    else:
        draw_text("No correct inputs!", 35, 300, 210)
    draw_text("Press any key to exit", 30, 300, 300)
    pygame.display.flip()

    # Wait for key press to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

# Run game
run_game()
pygame.quit()
