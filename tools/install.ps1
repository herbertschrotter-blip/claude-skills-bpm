# Einrichtung des Marketplace workbench auf Windows (Windows PowerShell 5.1 oder PowerShell 7).
# Prueft git, Python 3 (Befehl python3, den die Hooks aufrufen) und Claude Code, installiert Fehlendes nach Rueckfrage
# mit winget bzw. dem offiziellen Installer, legt den Marketplace an bzw. aktualisiert ihn und uebergibt dann an
# tools/einrichten.py (Plugins, Optionen, autoUpdate, skillOverrides, Probe der Hooks).
#
#   irm https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.ps1 | iex
#   powershell -ExecutionPolicy Bypass -File tools\install.ps1 [-Modus terminal|desktop] [-RechnerName NAME] [-Ja] [-OhneOverrides]
#
# Absichtlich nur ASCII und ohne param()-Block: so laeuft die Datei auch ueber "irm | iex" und ohne BOM unter 5.1.

$Repo = 'herbertschrotter-blip/claude-workbench'
$Marketplace = 'workbench'
$Modus = ''; $RechnerName = ''; $Ja = $false; $OhneOverrides = $false
for ($i = 0; $i -lt $args.Count; $i++) {
    switch ($args[$i]) {
        '-Modus' { $i++; $Modus = $args[$i] }
        '-RechnerName' { $i++; $RechnerName = $args[$i] }
        '-Ja' { $Ja = $true }
        '-OhneOverrides' { $OhneOverrides = $true }
    }
}

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
    # Ohne Python liefert Windows unter dem Namen python3 nur eine Verknuepfung zum Microsoft Store, die eine Meldung
    # ausgibt und mit Fehler endet. Deshalb wirklich ausfuehren und nur Exit 0 mit der richtigen Version zaehlen.
    if (-not (Has 'python3')) { return $false }
    $alt = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    try { $null = & python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>&1; return ($LASTEXITCODE -eq 0) }
    catch { return $false }
    finally { $ErrorActionPreference = $alt }
}

function Ende([string]$Text) { Write-Host ''; Write-Host $Text -ForegroundColor Red; return }

Write-Host '== Voraussetzungen'
if (Has 'git') { Write-Host "git: $(git --version)" }
elseif ((Has 'winget') -and (Frage 'git fehlt. Mit winget installieren?')) {
    winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements; Neu-Pfad
    if (-not (Has 'git')) { Ende 'git noch nicht gefunden - neues PowerShell-Fenster oeffnen und das Skript erneut starten.'; return }
} else { Ende 'Ohne git geht es nicht (der Marketplace ist ein Git-Repo).'; return }

if (Python3-Ok) { Write-Host "Python: $(python3 --version)" }
elseif ((Has 'winget') -and (Frage 'python3 fehlt (die Hooks rufen python3 auf). Python aus dem Microsoft Store mit winget installieren?')) {
    winget install -e --id 9NCVDN91XZQP --source msstore --accept-source-agreements --accept-package-agreements; Neu-Pfad
    if (-not (Python3-Ok)) { Ende 'python3 noch nicht verfuegbar - neues PowerShell-Fenster oeffnen und das Skript erneut starten.'; return }
    Write-Host "Python: $(python3 --version)"
} else { Ende 'Ohne python3 laufen Skill-Log und Skill-Waechter nicht. Python aus dem Microsoft Store installieren und erneut starten.'; return }

if (Has 'claude') { Write-Host "Claude Code: $(claude --version)" }
elseif (Frage 'Claude Code fehlt. Mit dem offiziellen Installer installieren (irm https://claude.ai/install.ps1 | iex)?') {
    Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression; Neu-Pfad
    $env:Path += ";$env:USERPROFILE\.local\bin"
    if (-not (Has 'claude')) { Ende 'claude noch nicht im PATH - neues PowerShell-Fenster oeffnen und das Skript erneut starten.'; return }
    Write-Host 'Anmelden: claude starten und /login ausfuehren, danach dieses Skript erneut starten.'; return
} else { Ende 'Ohne Claude Code geht es nicht.'; return }

Write-Host "== Marketplace $Marketplace"
function Marketplaces { $json = (claude plugin marketplace list --json | Out-String); if ($json.Trim()) { ConvertFrom-Json $json } }
if (@(Marketplaces) | Where-Object { $_.name -eq $Marketplace }) { claude plugin marketplace update $Marketplace }
else { claude plugin marketplace add $Repo }
$ort = (@(Marketplaces) | Where-Object { $_.name -eq $Marketplace } | Select-Object -First 1).installLocation
if (-not $ort) { Ende "Marketplace $Marketplace nicht gefunden - Ausgabe oben pruefen."; return }

Write-Host '== Plugins und Einstellungen'
$weiter = @()
if ($Modus) { $weiter += @('--modus', $Modus) }
if ($RechnerName) { $weiter += @('--host', $RechnerName) }
if ($Ja) { $weiter += '--ja' }
if ($OhneOverrides) { $weiter += '--ohne-overrides' }
& python3 -I (Join-Path $ort 'tools\einrichten.py') @weiter
# kein exit: beim Start mit "irm ... | iex" wuerde es das PowerShell-Fenster schliessen
