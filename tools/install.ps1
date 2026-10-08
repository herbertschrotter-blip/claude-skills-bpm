# Einrichtung des Marketplace workbench auf Windows (PowerShell 5.1 oder 7).
# Prüft git, Python 3 (Befehl python3, den die Hooks aufrufen) und Claude Code, installiert Fehlendes nach Rückfrage mit
# winget bzw. dem offiziellen Installer, legt den Marketplace an bzw. aktualisiert ihn und übergibt dann an
# tools/einrichten.py (Plugins, Optionen, autoUpdate, skillOverrides, Probe der Hooks).
#
#   powershell -ExecutionPolicy Bypass -File tools\install.ps1 [-Modus terminal|desktop] [-RechnerName NAME] [-Ja]
#   irm https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.ps1 | iex
param(
    [ValidateSet('terminal', 'desktop')][string]$Modus,
    [string]$RechnerName,
    [switch]$Ja,
    [switch]$OhneOverrides
)
$ErrorActionPreference = 'Stop'
$Repo = 'herbertschrotter-blip/claude-workbench'
$Marketplace = 'workbench'

function Has([string]$Name) { [bool](Get-Command $Name -ErrorAction SilentlyContinue) }

function Frage([string]$Text) {
    if ($Ja) { return $true }
    $antwort = Read-Host "$Text [J/n]"
    return -not ($antwort -match '^(n|nein)$')
}

function Neu-Pfad {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}

function Python3-Ok {
    if (-not (Has 'python3')) { return $false }
    & python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>$null
    return $LASTEXITCODE -eq 0
}

Write-Host '== Voraussetzungen'
if (Has 'git') { Write-Host "git: $(git --version)" }
elseif ((Has 'winget') -and (Frage 'git fehlt. Mit winget installieren?')) {
    winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements; Neu-Pfad
} else { throw 'Ohne git geht es nicht (der Marketplace ist ein Git-Repo).' }

if (Python3-Ok) { Write-Host "Python: $(python3 --version)" }
elseif ((Has 'winget') -and (Frage 'python3 fehlt (die Hooks rufen python3 auf). Python aus dem Microsoft Store mit winget installieren?')) {
    winget install -e --id 9NCVDN91XZQP --source msstore --accept-source-agreements --accept-package-agreements; Neu-Pfad
    if (-not (Python3-Ok)) { throw 'python3 noch nicht verfügbar – neues Fenster öffnen und das Skript erneut starten.' }
} else { throw 'Ohne python3 laufen Skill-Log und Skill-Wächter nicht.' }

if (Has 'claude') { Write-Host "Claude Code: $(claude --version)" }
elseif (Frage 'Claude Code fehlt. Mit dem offiziellen Installer installieren (irm https://claude.ai/install.ps1 | iex)?') {
    Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression; Neu-Pfad
    $env:Path += ";$env:USERPROFILE\.local\bin"
    if (-not (Has 'claude')) { throw 'claude noch nicht im PATH – neues Fenster öffnen und das Skript erneut starten.' }
    Write-Host 'Anmelden: claude starten und /login ausführen, danach dieses Skript erneut starten.'
} else { throw 'Ohne Claude Code geht es nicht.' }

Write-Host "== Marketplace $Marketplace"
$markets = claude plugin marketplace list --json | ConvertFrom-Json
if ($markets | Where-Object { $_.name -eq $Marketplace }) { claude plugin marketplace update $Marketplace }
else { claude plugin marketplace add $Repo }
$ort = (claude plugin marketplace list --json | ConvertFrom-Json | Where-Object { $_.name -eq $Marketplace }).installLocation

Write-Host '== Plugins und Einstellungen'
$weiter = @()
if ($Modus) { $weiter += @('--modus', $Modus) }
if ($RechnerName) { $weiter += @('--host', $RechnerName) }
if ($Ja) { $weiter += '--ja' }
if ($OhneOverrides) { $weiter += '--ohne-overrides' }
& python3 -I (Join-Path $ort 'tools\einrichten.py') @weiter
exit $LASTEXITCODE
