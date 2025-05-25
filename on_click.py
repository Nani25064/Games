from ursina import *
import random

app = Ursina()


# Sound
bounce_sound = Audio(r"c:\Users\pavan\Downloads\game-music-loop-7-145285.mp3", autoplay=False)
bounce_sound.volume = 0.5

# Define some colors and their names
colors = {
    "Red": color.red,
    "Green": color.green,
    "Blue": color.blue,
    "Yellow": color.yellow,
    
    "Orange": color.orange,
    "White": color.white,
}

color_names = list(colors.keys())

current_color_index = 0

# Create a cube entity in center
cube = Entity(model='cube', color=colors[color_names[current_color_index]], scale=2)

# UI to show current color name
color_name_text = Text(text=f"Current Color: {color_names[current_color_index]}",
                      origin=(0,0), position=(-0.7, 0.4), scale=2)

# UI color preview block
color_preview = Entity(parent=camera.ui, model='quad', color=colors[color_names[current_color_index]],
                       scale=(0.1, 0.1), position=(-0.85, 0.4))

def input(key):
    global current_color_index
    # When any key is pressed, change the current color to the next one
    if key != 'left mouse down':
        current_color_index = (current_color_index + 1) % len(color_names)
        color_name_text.text = f"Current Color: {color_names[current_color_index]}"
        color_preview.color = colors[color_names[current_color_index]]

def on_click():
    # Change cube color to the selected color on click
    cube.color = colors[color_names[current_color_index]]

def update():
    # Check for left mouse click on the cube
    if mouse.left:
        # Cast a ray to see if we hit the cube
        hit_info = raycast(camera.world_position, camera.forward, distance=100)
        if hit_info.entity == cube:
            on_click()

app.run()
