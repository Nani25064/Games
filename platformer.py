from ursina import *
from random import randint, uniform, choice

app = Ursina()

# Game state
score = 0
timer = 0
game_over = False
game_started = False
velocity_y = 0
gravity = 0.5
jump_force = 0.2
grounded = False
checkpoint_position = Vec3(0, 1, 0)

# Load background music
background_music = Audio(r"c:\Users\pavan\Downloads\game_music.wav", loop=True, autoplay=True)
print("Background music loaded:", background_music)


# Entities
player = Entity(model='cube', color=color.azure, scale_y=1.5, position=checkpoint_position, collider='box')
goal = Entity(model='cube', color=color.yellow, scale=(1, 1, 1), position=(30, 4.5), collider='box')
ground = Entity(model='cube', scale=(50, 1, 1), color=color.green, y=-3, collider='box')

# UI
score_text = Text(text='Time: 0s', position=(-0.85, 0.45), scale=1.5)
instructions = Text("Use A/D to move, Space to jump", origin=(0, 4), scale=1.5, y=0.45)
start_button = Button(text="Play Game", scale=(0.2, 0.1), y=0)
restart_button = Button(text="Play Again", scale=(0.2, 0.1), y=-0.1, enabled=False, visible=False)

# Particles
def spawn_jump_particles():
    for _ in range(5):
        p = Entity(model='sphere', color=color.white, scale=0.1, position=player.position + (0, -0.7, 0))
        p.animate_scale(0, duration=0.4)
        p.animate_position(p.position + Vec3(uniform(-0.5, 0.5), -0.5, 0), duration=0.4)
        destroy(p, delay=0.5)

def spawn_win_particles():
    for _ in range(20):
        p = Entity(model='sphere', color=color.random_color(), scale=0.1, position=goal.position)
        p.animate_scale(0, duration=1)
        p.animate_position(p.position + Vec3(uniform(-2, 2), uniform(-2, 2), 0), duration=1)
        destroy(p, delay=1)

# Platforms, spikes, checkpoints
platforms = []
spikes = []
checkpoints = []

for i in range(10):
    x = i * 3 + 5
    y = randint(-2, 4)
    platform = Entity(model='cube', scale=(3, 1, 1), color=color.orange, position=(x, y), collider='box')
    platforms.append(platform)

    if randint(0, 2) == 0:
        spike = Entity(model='cube', color=color.red, scale=(0.5, 0.5, 1), position=(x + 0.5, y + 0.75), collider='box')
        spikes.append(spike)

    if i in [3, 6]:
        cp = Entity(model='cube', color=color.cyan, scale=(0.3, 1, 1), position=(x, y + 1.5), collider='box')
        checkpoints.append(cp)

# Moving enemies
enemies = []
for i in range(2):
    e = Entity(model='cube', color=color.violet, position=(randint(5, 25), randint(0, 4)), scale=(1, 1, 1), collider='box')
    e.direction = choice([-1, 1])
    enemies.append(e)

# Camera
camera.orthographic = True
camera.fov = 16

# Start game function
def start_game():
    global game_started, game_over, timer, velocity_y, checkpoint_position
    player.position = checkpoint_position
    player.color = color.azure
    velocity_y = 0
    timer = 0
    game_over = False
    game_started = True
    start_button.enabled = False
    start_button.visible = False
    restart_button.enabled = False
    restart_button.visible = False
    background_music.play()
    print("Background music loaded:", background_music)


# Update function
def update():
    global velocity_y, grounded, score, timer, game_over, checkpoint_position

    if not game_started:
        return

    if game_over:
        return

    camera.position = (player.x + 6, 3)
    timer += time.dt
    score_text.text = f"Time: {int(timer)}s"

    # Movement
    speed = 5 * time.dt
    if held_keys['a']:
        player.x -= speed
    if held_keys['d']:
        player.x += speed

    # Gravity
    velocity_y -= gravity * time.dt
    player.y += velocity_y

    # Collision with ground/platform
    grounded = False
    hits = player.intersects()
    if hits.hit and velocity_y < 0:
        player.y = hits.entity.world_y + 0.75
        velocity_y = 0
        grounded = True

    # Jumping
    if grounded and held_keys['space']:
        velocity_y = jump_force
        spawn_jump_particles()

    # Check for falling off map
    if player.y < -10:
        print("🕳️ You fell!")
        die()

    # Spike collision
    for spike in spikes:
        if player.intersects(spike).hit:
            print("💀 You hit a spike!")
            die()

    # Enemy collision
    for enemy in enemies:
        enemy.x += enemy.direction * time.dt * 2
        if enemy.x < 0 or enemy.x > 35:
            enemy.direction *= -1

        if player.intersects(enemy).hit:
            print("😵 Enemy got you!")
            die()

    # Checkpoints
    for cp in checkpoints:
        if player.intersects(cp).hit:
            checkpoint_position = cp.position + Vec3(0, 1, 0)

    # Win condition
    if player.intersects(goal).hit:
        print("🎉 You reached the goal!")
        goal.color = color.lime
        spawn_win_particles()
        game_over = True
        restart_button.enabled = True
        restart_button.visible = True
        background_music.stop()

# Die and show restart
def die():
    global game_over
    player.color = color.red
    game_over = True
    restart_button.enabled = True
    restart_button.visible = True
    background_music.stop()

# Buttons
start_button.on_click = start_game
restart_button.on_click = start_game

app.run() 