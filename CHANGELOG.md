# Changelog

Notable project changes are recorded here. This changelog does not imply a
stable release or a Flathub listing.

## Unreleased

- Migrate the desktop interface from CustomTkinter to PySide6 Qt Widgets.
- Make only the black window background translucent; keep panels, text, controls,
  and dialogs opaque instead of fading the entire window.
- Request KWin background blur only on KDE Plasma under X11/XWayland, with a
  graceful fallback to the translucent background elsewhere.
- Remove Tk and global window-opacity handling.
- Shorten assistant prompts and provide platform guidance only when relevant.
- Tell the assistant not to hand terminal commands to users for manual execution.
- Initial public prototype and documentation.
- Added Steam Deck and multi-distribution diagnostic guidance.
- Added per-action approval prompts and multilingual interface.
