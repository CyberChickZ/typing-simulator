import pyautogui
import time
import random

def simulate_typing(text, min_delay=0.05, max_delay=0.15):
    """
    Simulate human-like typing by sending keystrokes one character at a time,
    with a small random delay between each character.
    """
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(min_delay, max_delay))

if __name__ == "__main__":
    print("You have 5 seconds to place your cursor in Google Docs...")
    time.sleep(5)

    # Example text to type
    message = (
        "This is a typing simulation demo.\n"
        "It mimics human keystrokes for use in Google Docs or any text field.\n"
        "Customize the message in typing_simulator.py to your needs.\n"
    )

    simulate_typing(message)
