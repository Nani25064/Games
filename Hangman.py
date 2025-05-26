import pygame
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Load sounds
correct_snd = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\game-start-317318.mp3")
incorrect_snd = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\beep-329314.mp3")
win_snd = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\winner-bell-game-show-91932.mp3")
lose_snd = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\game-over-arcade-6435.mp3")

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 35)
WORD_FONT = pygame.font.SysFont('comicsans', 55)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
BUTTON_FONT = pygame.font.SysFont('comicsans', 40)

# Game variables
hangman_status = 0
words_with_hints = {
    "PIZZA": "A popular Italian food",
    "GUITAR": "A musical instrument",
    "JUNGLE": "A dense forest",
    "PYJAMAS": "Clothes worn to sleep",
    "KANGAROO": "An animal from Australia",
    "ROBOT": "A machine that can act like a human",
    "BUBBLE": "It floats and pops!",
    "OCEAN": "Big body of salt water",
    "PLANET": "A large object that orbits a star",
    "VAMPIRE": "A mythical blood-sucking creature"
}
word, hint = random.choice(list(words_with_hints.items()))
guessed = []
game_over = False
result = ""

# Button variables
RADIUS = 20
GAP = 15
letters = []
A = 65
cols = 9  # 9 letters per row
rows = 3
total_letters = 26
startx = round((WIDTH - ((RADIUS * 2 + GAP) * cols - GAP)) / 2)
starty = HEIGHT - 130

for i in range(total_letters):
    x = startx + ((RADIUS * 2 + GAP) * (i % cols))
    y = starty + ((i // cols) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Draw Hangman
def draw_hangman(stage):
    base_x = 100
    base_y = 400
    pygame.draw.line(win, (0, 0, 0), (base_x, base_y), (base_x + 100, base_y), 5)
    pygame.draw.line(win, (0, 0, 0), (base_x + 50, base_y), (base_x + 50, base_y - 250), 5)
    pygame.draw.line(win, (0, 0, 0), (base_x + 50, base_y - 250), (base_x + 150, base_y - 250), 5)
    pygame.draw.line(win, (0, 0, 0), (base_x + 150, base_y - 250), (base_x + 150, base_y - 200), 5)

    if stage > 0:
        pygame.draw.circle(win, (0, 0, 0), (base_x + 150, base_y - 175), 25, 3)
    if stage > 1:
        pygame.draw.line(win, (0, 0, 0), (base_x + 150, base_y - 150), (base_x + 150, base_y - 80), 3)
    if stage > 2:
        pygame.draw.line(win, (0, 0, 0), (base_x + 150, base_y - 140), (base_x + 120, base_y - 110), 3)
    if stage > 3:
        pygame.draw.line(win, (0, 0, 0), (base_x + 150, base_y - 140), (base_x + 180, base_y - 110), 3)
    if stage > 4:
        pygame.draw.line(win, (0, 0, 0), (base_x + 150, base_y - 80), (base_x + 120, base_y - 50), 3)
    if stage > 5:
        pygame.draw.line(win, (0, 0, 0), (base_x + 150, base_y - 80), (base_x + 180, base_y - 50), 3)

# Draw everything
def draw():
    win.fill((255, 255, 255))

    if game_over:
        result_text = WORD_FONT.render(result, True, (255, 0, 0) if "LOSE" in result else (0, 128, 0))
        win.blit(result_text, (WIDTH / 2 - result_text.get_width() / 2, HEIGHT / 2 - 80))

        restart_btn = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50)
        pygame.draw.rect(win, (0, 0, 0), restart_btn, 2)
        btn_text = BUTTON_FONT.render("Play Again", True, (0, 0, 0))
        win.blit(btn_text, (restart_btn.x + 20, restart_btn.y + 5))

    else:
        title_text = TITLE_FONT.render("HANGMAN", True, (0, 0, 0))
        win.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 20))

        hint_text = LETTER_FONT.render(f"Hint: {hint}", True, (100, 100, 100))
        win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, 100))

        display_word = ""
        for letter in word:
            display_word += letter + " " if letter in guessed else "_ "
        word_text = WORD_FONT.render(display_word.strip(), True, (0, 0, 0))
        win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, 270))

        for letter in letters:
            x, y, ltr, visible = letter
            if visible:
                pygame.draw.circle(win, (0, 0, 0), (x, y), RADIUS, 3)
                text = LETTER_FONT.render(ltr, True, (0, 0, 0))
                win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

        draw_hangman(hangman_status)

    pygame.display.update()

# Restart game
def restart_game():
    global hangman_status, word, guessed, letters, game_over, result, hint
    hangman_status = 0
    word, hint = random.choice(list(words_with_hints.items()))
    guessed = []
    for letter in letters:
        letter[3] = True
    game_over = False
    result = ""

# Main loop
FPS = 60
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if game_over:
                if pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50).collidepoint((m_x, m_y)):
                    restart_game()
            else:
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dist = ((x - m_x) ** 2 + (y - m_y) ** 2) ** 0.5
                        if dist < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
                                incorrect_snd.play()
                            else:
                                correct_snd.play()

    if not game_over:
        if all([ltr in guessed for ltr in word]):
            win_snd.play()
            result = "YOU WON!"
            game_over = True
        elif hangman_status == 6:
            lose_snd.play()
            result = f"YOU LOSE! Word was: {word}"
            game_over = True

pygame.quit()
