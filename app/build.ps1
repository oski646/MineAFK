$ErrorActionPreference = "Stop"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "uv is not installed or is not on PATH. Install it with: winget install --id astral-sh.uv"
}

function Invoke-Uv {
    uv @args
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Invoke-Uv run --group build pyinstaller --clean --onefile --icon=pickaxe.ico main.py
Invoke-Uv run --group build pyinstaller --clean --onefile --icon=pickaxe.ico mouse-position.py

Copy-Item -Path config.ini -Destination dist\config.ini -Force
