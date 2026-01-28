Add-Type -AssemblyName System.Windows.Forms

$pathBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$pathBrowser.Description = "Select path to plugin installation"
$pathBrowser.SelectedPath  = "C:\"
if ($pathBrowser.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $rootPath = $pathBrowser.SelectedPath

    Write-Host "Selected path: $rootPath" -ForegroundColor Yellow

    if ([string]::IsNullOrWhiteSpace($rootPath)) {
        Write-Host "Error: No folder selected" -ForegroundColor Red
        exit 1
    }

    $folderName = Split-Path $rootPath -Leaf
    if ($rootPath -notmatch "Plugins\\python") {
        Write-Host "Error: Selected folder have to be in '<Atom>\Plugin\python'" -ForegroundColor Red
        Write-Host "Current folder name: '$folderName'" -ForegroundColor Yellow
        exit 1
    }

} else {
    Write-Host "Operation cancelled" -ForegroundColor Red
    exit 1
}

$pluginPath = "$rootPath\plugin-peak-shape"


# Extracting a source code
Write-Host "Extracting plugin's source code..." -ForegroundColor Yellow

New-Item -ItemType Directory -Path "$pluginPath" -Force

Expand-Archive -Path "$PSScriptRoot\plugin.zip" -DestinationPath "$rootPath\temp" -Force
$extractedFolder = Get-ChildItem -Path "$rootPath\temp" -Directory | Select-Object -First 1
Move-Item -Path "$($extractedFolder.FullName)\*" -Destination "$pluginPath" -Force
Remove-Item -Path "$rootPath\temp" -Recurse -Force


# Installing a plugin
Write-Host "Extracting plugin's source code..." -ForegroundColor Yellow
Set-Location "$pluginPath"

Write-Host "Creating virtual environments..." -ForegroundColor Yellow
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --no-index --find-links "$PSScriptRoot\packages" -r "$PSScriptRoot\packages\requirements.txt"

Write-Host "Plugin installed successfully" -ForegroundColor Yellow


#
Set-Location "$PSScriptRoot"
