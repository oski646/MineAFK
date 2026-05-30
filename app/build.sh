#!/usr/bin/env sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PROJECT_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"
mkdir -p "$PROJECT_ROOT/dist"
rm -f "$PROJECT_ROOT/dist/MineAFK.exe" "$PROJECT_ROOT/dist/main.exe" "$PROJECT_ROOT/dist/mouse-position.exe"
case "$(uname -s 2>/dev/null || echo unknown)" in
    MINGW*|MSYS*|CYGWIN*) DATA_SEPARATOR=";" ;;
    *) DATA_SEPARATOR=":" ;;
esac
uv run --group build pyinstaller --clean --onefile --windowed --name MineAFK --specpath "$PROJECT_ROOT/build" --icon "$PROJECT_ROOT/pickaxe.ico" --add-data "$PROJECT_ROOT/pickaxe.ico${DATA_SEPARATOR}." "$PROJECT_ROOT/main.py"
cp "$PROJECT_ROOT/config.ini" "$PROJECT_ROOT/dist/config.ini"
