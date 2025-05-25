````markdown
# Typing Simulator

A simple Python tool that simulates human-like typing into target applications such as Google Docs. Built with [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI), it provides a GUI for customizing typing speed and pause behavior.

## Features

- Multiline input field
- Adjustable typing speed (min/max delay)
- Adjustable punctuation pause
- Debug mode for inspecting typing flow

## Getting Started

### Requirements

- Python 3.13+ with Tkinter
- macOS recommended (tested with `python-tk@3.13` via Homebrew)

### Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### Run

```bash
python typing_simulator_gui.py
```

## Status

Work in progress. Further improvements may be added later when time allows.

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).