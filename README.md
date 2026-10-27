# DeckMate

**A system-support assistant focused on Steam Deck and Linux.**

DeckMate is an early-stage desktop application built with Python and
CustomTkinter. It connects to the official GitHub Copilot SDK to answer
questions, inspect available system information, and guide troubleshooting.
The app is not affiliated with Valve, KDE, or GitHub.

## Current status

This project is a prototype and is not yet published on Flathub or the KDE
Discover store. System access and available diagnostics depend on the host,
installed tools, Copilot account, and SDK permissions. DeckMate cannot guarantee
that it can diagnose or repair every issue.

The Steam Deck guidance distinguishes SteamOS from general Linux distributions.
The assistant should prefer read-only checks, protect user data, and ask before
actions that change the system. Review every proposed action before approving it.

## Requirements

- Python 3.10 or newer
- A graphical Linux desktop with Tk support
- A GitHub account with access to GitHub Copilot
- Network access for the Copilot service

The app is primarily designed for SteamOS and Linux. Other systems have not been
validated and may not provide the required desktop or host diagnostics.

## Run from source

On Steam Deck, switch to Desktop Mode and open Konsole. Create a virtual
environment and install the Python dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m copilot download-runtime
.venv/bin/copilot login
.venv/bin/python assistente.py
```

If the Copilot CLI login command is not available in your installed SDK version,
use the app's **Connect** button and follow the official sign-in flow.

## Project files

- `assistente.py` — application source
- `requirements.txt` — Python dependencies

## Privacy and permissions

System information and prompts may be sent to GitHub Copilot when you use the
assistant. Do not share secrets or sensitive logs in chat. Tool actions can
affect the computer; inspect the requested action and only approve changes you
understand. A permission prompt is not a guarantee that an action is safe.

## License

DeckMate is distributed under the GNU General Public License, version 3 or later.
See `LICENSE`.

## Credits

Created by **Flavinho PQD 85207**.  
Instagram: <https://www.instagram.com/eagle_85207/>
