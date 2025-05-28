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
    Split text into chunks: words, punctuation, whitespace, or newlines.
    """
    pattern = r'\w+|[^\w\s]|\s'
    return re.findall(pattern, text)

# Typing simulation function
def simulate_typing(text, min_delay_ms, max_delay_ms, punctuation_pause_ms, debug=False):
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        typo_chunks = inject_typo(chunk)  # Your inject_typo remains unchanged, returning list
        for part in typo_chunks:
            # Determine type
            if part == chunk:
                part_type = "normal"
            elif set(part) == {"\b"}:
                part_type = f"backspace × {len(part)}"
            elif part.isalpha() and part != chunk:
                part_type = "typo/correction"
            else:
                part_type = "other"

            # Simulate typing
            if part_type == "backspace":
                # todo: split backspace and string into 2 parts(\b *n and string)
                # Brief pause after backspace
                if part != '\b' and part[0] == '\b':
                    base_delay = 1 * len(part)
                    # if random.random() < 0.1:
                    # delay = 15 * 1000
            else:
                pyautogui.write(part, interval=0.01)

            # Determine delay
            base_delay = random.randint(min_delay_ms, max_delay_ms)
            last_char = part[-1] if part else ""
            if last_char in ['.', ';']:
                # base_delay += 2 * punctuation_pause_ms * random.choice([1, 0.9])
                if random.random() < 0.3:
                    base_delay += 2 * punctuation_pause_ms
                else:
                    base_delay = 15 * 1000

            elif last_char in [',', ]:
                base_delay +=  0.5 * punctuation_pause_ms
                if random.random() < 0.1:
                    base_delay = 15 * 1000
            elif last_char == '\n':
                base_delay += 3 * punctuation_pause_ms * 10
            delay = base_delay / 1000

            if debug:
                print(
                    f"[{i:03d}] {part_type:<14} | Out: {repr(part):<18} | "
                    f"Orig: {repr(chunk):<18} | Delay: {delay:>5.2f}s"
                )

            time.sleep(delay)
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