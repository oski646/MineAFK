uv run --group build pyinstaller --clean --onefile --icon=pickaxe.ico main.py
uv run --group build pyinstaller --clean --onefile --icon=pickaxe.ico mouse-position.py
cp config.ini dist/config.ini
