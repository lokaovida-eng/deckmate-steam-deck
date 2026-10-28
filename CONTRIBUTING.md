# Contributing

Thanks for helping improve DeckMate. The project is experimental, primarily
targets Steam Deck and Linux, and is not yet packaged for Flathub.

## Before making changes

- Check existing issues and describe the problem or proposed change.
- Keep changes focused and explain user-visible behavior changes.
- Do not add credentials, access tokens, private logs, or personal device data.
- Do not claim a platform or repair path is supported unless it has been tested.
- Do not add broad host permissions or bypass Flatpak sandboxing to make a
  potential package appear functional.

## Validation

Use Python 3.10 or newer. Before opening a pull request, run:

```bash
python3 -m py_compile assistente.py ../assistente.py
python3 -m unittest discover -s tests -v
```

The source copies `assistente.py` and `deckmate/assistente.py` must remain
identical. The Qt translucency contract is tested offscreen; visual compositor
behavior and Copilot integration still need testing on a real graphical Linux
system with an account that can access Copilot.

## Pull requests

Include a concise description, the reason for the change, validation performed,
and any known limitations. For changes affecting diagnostics or actions, explain
what host access is required and how user data is protected. Maintainers may ask
for revisions before accepting changes.
