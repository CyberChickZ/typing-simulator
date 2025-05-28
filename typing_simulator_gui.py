import time
import random
import pyautogui
import PySimpleGUI as sg
import re
import string
import random

def inject_typo(chunk, typo_chance=0.07, fix_chance=0.5):
    # Inject typos only in letter/word chunks
    if not chunk.isalpha() or len(chunk) < 3 or random.random() > typo_chance:
        return [chunk]  # Return list for consistent processing later

    # Typo types (implementing one of replace/swap/delete/insert)
    typo_types = ['replace', 'swap', 'delete', 'insert']
    typo_type = random.choice(typo_types)

    chars = list(chunk)
    idx = random.randint(0, len(chars) - 1)

    if typo_type == 'replace':
        wrong = random.choice(string.ascii_letters)
        chars[idx] = wrong
    elif typo_type == 'swap' and len(chars) > 1 and idx < len(chars) - 1:
        chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
    elif typo_type == 'delete' and len(chars) > 1:
        chars.pop(idx)
    elif typo_type == 'insert':
        chars.insert(idx, random.choice(string.ascii_letters))

    typo_word = ''.join(chars)

    # Simulate fixing the typo (backspace + retype)
    if random.random() < fix_chance:
        # Backspace length equals typo_word
        return [typo_word, '\b' * len(typo_word), chunk]
    else:
        return [typo_word]  # No fix, keep the typo
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
        for part in inject_typo(chunk):
            pyautogui.write(part)
            # If it's a backspace character, a very short delay can be added
            if part and part[0] == '\b':
                time.sleep(0.1 * len(part))

        last_char = chunk[-1]
        for part in chunks:
            pyautogui.write(part)
            if debug:
                print(f"Typing: {repr(part)} (original: {repr(chunk)})")
            if part and part[0] == '\b':
                time.sleep(0.03 * len(part))
            else:
                # 计算延迟（按字母数）
                base_delay = random.randint(min_delay_ms, max_delay_ms)
                # 标点和换行特殊停顿
                last_char = part[-1] if part else ""
                if last_char in ['.', ';']:
                    base_delay += punctuation_pause_ms
                elif last_char == '\n':
                    base_delay += 2 * punctuation_pause_ms

                # 延迟与实际长度成比例
                delay = base_delay * max(1, len(part))
                time.sleep(delay / 1000)

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