from ursina import *

app = Ursina()

# Sound
bounce_sound = Audio(r"c:\Users\pavan\Downloads\game-music-loop-7-145285.mp3", autoplay=False)

window.show_cursor = False  # Hide default OS cursor

# Start with default emoji cursor
cursor_emoji = "🎯"
cursor = Text(text=cursor_emoji, color=color.white, origin=(0,0), scale=3, background=True)

def update():
    # Cursor follows mouse position on screen UI
    cursor.position = Vec2(mouse.x, mouse.y)

def input(key):
    global cursor_emoji
    if key == '1':
        cursor_emoji = "⚔️  Sword "
    elif key == '2':
        cursor_emoji = "🛡️ Shield "
    elif key == '3':
        cursor_emoji = "✨  Magic sparkle "
    cursor.text = cursor_emoji

app.run()
