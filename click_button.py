from ursina import *
import random

app = Ursina()

# Sound
bounce_sound = Audio(r"c:\Users\pavan\Downloads\game-music-loop-7-145285.mp3", autoplay=False)

# Player entity (cube) in center of the screen
player = Entity(model='cube', color=color.azure, scale=1.5, y=0)

# Button entity in UI space
button = Button(text='Click Me', scale=(0.3, 0.1), position=(0, 0.4))

# Icon placeholder on the button
icon = None

# Function to get a random color
def get_random_color():
    return color.rgb(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# On button click
def on_button_click():
    global icon

    # Add icon (e.g., a heart or star emoji text) on button once
    if not icon:
        icon = Text(parent=button, text='⭐', scale=2, origin=(0, 0), position=(0.3, 0))

    # Change player color
    player.color = get_random_color()

button.on_click = on_button_click

app.run()
