from ursina import *

app = Ursina()
window.title = "Brick Breaker Game"
window.color = color.black

# Game state
game_started = False

# Paddle
paddle = Entity(model='cube', color=color.azure, scale=(2, 0.4, 0), position=(0, -4), collider='box', enabled=False)

# Ball
ball = Entity(model='sphere', color=color.white, scale=0.3, position=(0, -3.5), collider='box', enabled=False)
ball.velocity = Vec2(3, 4)



# Score
score = 0
score_text = Text(text=f"Score: {score}", position=(-0.85, 0.45), scale=2, enabled=False)

# Game Over Text
game_over_text = Text(text="Game Over!", origin=(0, 0), scale=3, enabled=False)

# Buttons
def start_game():
    global game_started, score
    game_started = True
    paddle.enabled = True
    ball.enabled = True
    score_text.enabled = True
    game_over_text.enabled = False
    start_button.disable()
    play_again_button.disable()

    ball.position = (0, -3.5)
    ball.velocity = Vec2(3, 4)
    score = 0
    score_text.text = f"Score: {score}"

def play_again():
    start_game()

def close_game():
    quit()

start_button = Button(text='Play', scale=(0.2, 0.1), position=(0, 0.1), on_click=start_game)
play_again_button = Button(text='Play Again', scale=(0.2, 0.1), position=(0, -0.1), on_click=play_again, enabled=False)
close_button = Button(text='Close', scale=(0.2, 0.1), position=(window.top_right - (0.2, 0.1)), origin=(0.5, 0.5), on_click=close_game)
def update():
    global score, game_started

    if not game_started:
        return

    # Paddle movement
    if held_keys['left arrow']:
        paddle.x -= 5 * time.dt
    if held_keys['right arrow']:
        paddle.x += 5 * time.dt

    # Clamp paddle position
    paddle.x = clamp(paddle.x, -6.5, 6.5)

    # Move ball
    ball.x += ball.velocity.x * time.dt
    ball.y += ball.velocity.y * time.dt

    # Wall collisions
    if abs(ball.x) > 7:
        ball.velocity.x *= -1
    if ball.y > 5:
        ball.velocity.y *= -1

    # Bottom collision (Game Over)
    if ball.y < -5:
        ball.disable()
        game_over_text.enabled = True
        play_again_button.enabled = True
        game_started = False

    # Paddle collision
    if ball.intersects(paddle).hit:
        ball.velocity.y *= -1
        ball.y = paddle.y + 0.3  # Avoid sticking


app.run()