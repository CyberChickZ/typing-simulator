import time
import random
import pyautogui
import PySimpleGUI as sg
import re

def chunk_text(text):
    """
    Split text into chunks: word, punctuation, or newline.
    E.g. "Hello, world!\nHow are you?" -> ['Hello', ',', ' ', 'world', '!', '\n', 'How', ' ', 'are', ' ', 'you', '?']
    """
    pattern = r'\w+|[^\w\s]|\s'
    return re.findall(pattern, text)

# Typing simulation function
def simulate_typing(text, min_delay_ms, max_delay_ms, punctuation_pause_ms, debug=False):
    chunks = chunk_text(text)
    for chunk in chunks:
        pyautogui.write(chunk)

        last_char = chunk[-1]
        delay = random.randint(min_delay_ms, max_delay_ms)
        if last_char in ['.', ';']:
            delay += punctuation_pause_ms
        elif last_char == '\n':
            delay += 2 * punctuation_pause_ms

        if debug:
            print(f"Typing chunk: {repr(chunk)} | delay: {delay / 1000:.2f}s")

        time.sleep(delay / 1000)

# GUI layout
sg.theme("SystemDefault")
layout = [
    [sg.Text("Enter text to simulate typing:")],
    [sg.Multiline(size=(60, 6), key="-INPUT-")],

    [sg.Text("Min Delay (ms):"), sg.Slider(range=(0, 500), default_value=0, orientation='h',
                                           resolution=1, key='-MIN-', enable_events=True)],
    [sg.Text("Max Delay (ms):"), sg.Slider(range=(1, 501), default_value=22, orientation='h',
                                           resolution=1, key='-MAX-', enable_events=True)],
    [sg.Text("Punctuation Pause (ms):"), sg.Slider(range=(0, 1000), default_value=300, orientation='h',
                                                   resolution=50, key='-PAUSE-', enable_events=True)],

    [sg.Button("Start Typing"), sg.Button("Exit")]
]

window = sg.Window("Typing Simulator", layout)

# Event loop
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break

    elif event == "Start Typing":
        text = values["-INPUT-"].strip()
        if not text:
            sg.popup("Please enter some text to type.")
            continue

        min_delay = int(values["-MIN-"])
        max_delay = int(values["-MAX-"])
        punctuation_pause = int(values["-PAUSE-"])

        if min_delay > max_delay:
            sg.popup_error("Min delay must not exceed max delay.")
            continue

        sg.popup("Switch to Google Docs now. Typing will start in 5 seconds...")
        time.sleep(5)

        simulate_typing(text, min_delay, max_delay, punctuation_pause, debug=True)
        sg.popup("Typing complete.")

window.close()

# End