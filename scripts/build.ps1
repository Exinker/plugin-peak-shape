param(
    [string]$pluginVersion = $null
)

if (-not $pluginVersion) {
    $pluginVersion = (& uv run python -c "import plugin; print(plugin.__version__)").Trim()
}
Write-Host "Plugin Version: $pluginVersion" -ForegroundColor Yellow


#
$rootPath = Split-Path -Path $PSScriptRoot -Parent
$pluginPath = "$rootPath\build\$pluginVersion"

$pythonURL = "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"
$pluginURL = "https://github.com/Exinker/plugin-peak-shape/archive/refs/tags/$pluginVersion.zip"

Write-Host "Creating distribution..." -ForegroundColor Yellow


# Downloading requirements
Write-Host "Plugin Path: $pluginPath" -ForegroundColor Yellow
New-Item -ItemType Directory -Path "$pluginPath" -Force

Write-Host "Downloading python..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "$pythonURL" -OutFile "$pluginPath\python.exe"

Write-Host "Downloading plugin from github..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "$pluginURL" -OutFile "$pluginPath\plugin.zip"


# Exporting requirements
$packagesPath = "$pluginPath\packages"
New-Item -ItemType Directory -Path "$packagesPath" -Force

Write-Host "Exporting requirements.txt..." -ForegroundColor Yellow
$requirementsPath = "$packagesPath\requirements.txt"
uv export `
    --no-editable `
    --no-group dev `
    --no-hashes `
    --output-file "$requirementsPath" `
    --python 3.12

Write-Host "Exporting base requirements..." -ForegroundColor Yellow
uv run pip download `
    setuptools>=61.0 `
    wheel `
    pip `
    -d "$packagesPath"


Write-Host "Exporting plugin requirements..." -ForegroundColor Yellow
uv run pip download `
    -r "$requirementsPath" `
    -d "$packagesPath"

# Copy deploy script
Copy-Item -Path "$PSScriptRoot\deploy.ps1" -Destination "$pluginPath\deploy.ps1" -Force
