#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
APPIMAGETOOL="${APPIMAGETOOL:-}"
BUILD_ROOT="$ROOT/build/appimage"
DIST_ROOT="$ROOT/dist"
APP_DIR="$DIST_ROOT/DeckMate.AppDir"
OUTPUT="$DIST_ROOT/DeckMate-x86_64.AppImage"

if [[ "$(uname -m)" != "x86_64" ]]; then
    printf 'AppImage build requires x86_64; found %s.\n' "$(uname -m)" >&2
    exit 1
fi

if [[ -z "$APPIMAGETOOL" || ! -x "$APPIMAGETOOL" ]]; then
    printf 'Set APPIMAGETOOL to the verified AppImageKit appimagetool executable.\n' >&2
    exit 1
fi

"$PYTHON" -m PyInstaller \
    --noconfirm \
    --clean \
    --distpath "$BUILD_ROOT/dist" \
    --workpath "$BUILD_ROOT/work" \
    "$ROOT/packaging/DeckMate.spec"

mkdir -p "$APP_DIR/usr/bin"
rm -rf "$APP_DIR/usr/bin/DeckMate"
cp -a "$BUILD_ROOT/dist/DeckMate" "$APP_DIR/usr/bin/DeckMate"
install -m 755 "$ROOT/packaging/AppRun" "$APP_DIR/AppRun"
install -m 644 "$ROOT/packaging/deckmate.desktop" "$APP_DIR/deckmate.desktop"
install -m 644 "$ROOT/packaging/deckmate.svg" "$APP_DIR/deckmate.svg"
ln -sfn deckmate.svg "$APP_DIR/.DirIcon"
rm -f "$OUTPUT"

ARCH=x86_64 "$APPIMAGETOOL" --appimage-extract-and-run "$APP_DIR" "$OUTPUT"
chmod 755 "$OUTPUT"
printf 'Built %s (%s bytes)\n' "$OUTPUT" "$(stat -c '%s' "$OUTPUT")"
