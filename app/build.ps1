$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$IconPath = Join-Path $ProjectRoot "pickaxe.ico"
$EntryPoint = Join-Path $ProjectRoot "main.py"
$SpecPath = Join-Path $ProjectRoot "build"
$ConfigPath = Join-Path $ProjectRoot "config.ini"
$DistConfigPath = Join-Path $ProjectRoot "dist\config.ini"
$DistPath = Join-Path $ProjectRoot "dist"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "uv is not installed or is not on PATH. Install it with: winget install --id astral-sh.uv"
}

function Invoke-Uv {
    uv @args
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Push-Location $ProjectRoot
try {
    New-Item -ItemType Directory -Path $DistPath -Force | Out-Null
    foreach ($Artifact in @("MineAFK.exe", "main.exe", "mouse-position.exe")) {
        $ArtifactPath = Join-Path $DistPath $Artifact
        if (Test-Path $ArtifactPath) {
            Remove-Item -Path $ArtifactPath -Force
        }
    }

    Invoke-Uv run --group build pyinstaller --clean --onefile --windowed --name MineAFK --specpath $SpecPath --icon $IconPath --add-data "${IconPath};." $EntryPoint

    Copy-Item -Path $ConfigPath -Destination $DistConfigPath -Force
}
finally {
    Pop-Location
}
