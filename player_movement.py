from ursina import *
import pygame
import random
import time

app = Ursina()
pygame.mixer.init()

window.title = "Procedural Maze Runner"
camera.fov = 90
window.exit_button.visible = False

# Load sounds
move_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\game-music-loop-7-145285.mp3")
win_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\winner-bell-game-show-91932.mp3")
trap_sound = pygame.mixer.Sound(r"c:\Users\pavan\Downloads\beep-329314.mp3")

WALL_COLOR = color.gray
FLOOR_COLOR = color.white
PLAYER_COLOR = color.azure
GOAL_COLOR = color.green
TRAP_COLOR = color.red

tile_size = 1
maze_size = 11  # must be odd
maze = []
walls = []
traps = []
start_time = time.time()

# Directions: up, down, left, right
dir_offsets = [(0, 2), (0, -2), (-2, 0), (2, 0)]

def generate_maze():
    global maze
    maze = [["W" for _ in range(maze_size)] for _ in range(maze_size)]

    def carve(x, y):
        maze[y][x] = "."
        dirs = dir_offsets[:]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 1 <= nx < maze_size - 1 and 1 <= ny < maze_size - 1 and maze[ny][nx] == "W":
                maze[y + dy//2][x + dx//2] = "."
                carve(nx, ny)

    carve(1, 1)
    maze[maze_size - 2][maze_size - 2] = "G"

generate_maze()

# Render maze
for y in range(maze_size):
    for x in range(maze_size):
        pos = Vec3(x, 0, y)
        char = maze[y][x]
        if char == "W":
            walls.append(Entity(model="cube", color=WALL_COLOR, position=pos, scale=(1, 1, 1), collider="box"))
        elif char == ".":
            if random.random() < 0.05 and (x, y) != (1, 1):
                trap = Entity(model="cube", color=TRAP_COLOR, position=pos, scale=(0.8, 0.8, 0.8), collider="box")
                traps.append(trap)
            Entity(model="quad", texture="white_cube", color=FLOOR_COLOR, position=pos + Vec3(0, -0.5, 0),
                   scale=(1, 1, 1), rotation_x=90)
        elif char == "G":
            global goal_pos
            goal_pos = pos
            Entity(model="quad", texture="white_cube", color=GOAL_COLOR, position=pos + Vec3(0, -0.5, 0),
                   scale=(1, 1, 1), rotation_x=90)

# Player
player = Entity(model="cube", color=PLAYER_COLOR, position=Vec3(1, 0, 1), scale=(0.9, 0.9, 0.9), collider="box")
camera.position = (maze_size // 2, 14, -maze_size // 2)
camera.rotation_x = 65

timer_text = Text(text="Time: 0", position=(-0.85, 0.45), scale=1.5, background=True)

def update():
    timer_text.text = f"Time: {int(time.time() - start_time)}"

    direction = Vec3(
        int(held_keys["d"]) - int(held_keys["a"]),
        0,
        int(held_keys["s"]) - int(held_keys["w"]),
    )

    # no diagonal
    if direction.x != 0:
        direction.z = 0

    if direction != Vec3(0, 0, 0):
        move(direction)

    # goal reached
    if distance(player.position, goal_pos) < 0.5:
        win_sound.play()
        Text("🎉 You Win!", scale=2, color=color.yellow, origin=(0, 0), background=True)
        application.pause()

    # trap collision
    for trap in traps:
        if player.position == trap.position:
            trap_sound.play()
            player.position = Vec3(1, 0, 1)

def move(direction):
    next_pos = player.position + direction
    for wall in walls:
        if wall.position == next_pos:
            return
    move_sound.play()
    player.position = next_pos

app.run()
