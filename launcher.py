import subprocess
from pynput import keyboard

# NOTE: before running this file, find absolute path to the parent project folder ('MinesweeperBot')
# and replace PROJECT_PATH with this path

PROJECT_PATH = '/Users/jakeduffy/PycharmProjects/MinesweeperBot'

process = subprocess.Popen(
    ['python3', 'main.py'],
    cwd=PROJECT_PATH,
    )

# OTHER NOTE: if you're on a Windows machine, you may need to replace 'python3' with 'python'
# in the first argument list of subprocess.Popoen (as seen in the lines of code above)

def on_press(key):
    global process, keyboard_listener
    if key == keyboard.Key.esc:
        process.kill()
        keyboard_listener.stop()


with keyboard.Listener(on_press=on_press) as keyboard_listener:
    keyboard_listener.join()
