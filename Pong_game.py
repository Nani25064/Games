import pygame

import random

# Init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Pong with Sound, AI, and Game Over")
clock = pygame.time.Clock()

# Colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 50)

# Sounds
try:
    hit_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\90s-game-ui-6-185099.mp3")
    score_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\winner-bell-game-show-91932.mp3")
except:
    hit_sound = score_sound = None

# Game mode
ai_mode = True  # Change to False for Player vs Player

# Game variables
paddle_width, paddle_height = 10, 100
ball_size = 20

player1 = pygame.Rect(50, 200, paddle_width, paddle_height)
player2 = pygame.Rect(740, 200, paddle_width, paddle_height)

ball = pygame.Rect(390, 240, ball_size, ball_size)
ball_speed_x = 5 * random.choice((-1, 1))
ball_speed_y = 5 * random.choice((-1, 1))

score1 = 0
score2 = 0
MAX_SCORE = 10

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (400, 250)
    ball_speed_x *= -1
    ball_speed_y *= random.choice([-1, 1])

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (400, 0), (400, 500))

    score_text1 = font.render(f"{score1}", True, WHITE)
    score_text2 = font.render(f"{score2}", True, WHITE)
    screen.blit(score_text1, (300, 20))
    screen.blit(score_text2, (470, 20))
    pygame.display.flip()

def game_over(winner):
    screen.fill(BLACK)
    draw_text(f"{winner} Wins!", 60, 300, 200)
    draw_text("Press any key to exit", 40, 250, 280)
    pygame.display.flip()
    pygame.time.wait(1000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
          

def draw_text(text, size, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
          

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= 6
    if keys[pygame.K_s] and player1.bottom < 500:
        player1.y += 6

    if not ai_mode:
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= 6
        if keys[pygame.K_DOWN] and player2.bottom < 500:
            player2.y += 6
    else:
        # AI Movement
        if player2.centery < ball.centery and player2.bottom < 500:
            player2.y += 5
        elif player2.centery > ball.centery and player2.top > 0:
            player2.y -= 5

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Wall collision
    if ball.top <= 0 or ball.bottom >= 500:
        ball_speed_y *= -1
        if hit_sound: hit_sound.play()

    # Paddle collision
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
        if hit_sound: hit_sound.play()

    # Scoring
    if ball.left <= 0:
        score2 += 1
        if score_sound: score_sound.play()
        reset_ball()
    if ball.right >= 800:
        score1 += 1
        if score_sound: score_sound.play()
        reset_ball()

    if score1 >= MAX_SCORE:
        game_over("Player 1")
    if score2 >= MAX_SCORE:
        game_over("Player 2" if not ai_mode else "AI")

    draw()
    clock.tick(60)