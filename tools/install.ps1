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

function Ende([string]$Text) {
    Write-Progress -Activity 'Einrichtung workbench' -Completed
    Write-Host ''; Write-Host "  ABBRUCH: $Text" -ForegroundColor Red; return
}
function Schritt([string]$Text, [int]$Nummer) {
    Write-Host ''; Write-Host $Text -ForegroundColor Cyan
    # Fortschrittsbalken oben im Fenster; verschwindet am Ende (Write-Progress -Completed)
    Write-Progress -Activity 'Einrichtung workbench' -Status $Text -PercentComplete ([int](($Nummer - 1) * 100 / 5))
}
function Ok([string]$Text) { Write-Host "  OK  $Text" -ForegroundColor Green }

Write-Host ''
Write-Host '=== Einrichtung workbench (Skills, Skill-Log, Skill-Waechter) ===' -ForegroundColor Cyan
Schritt '[1/5] Voraussetzungen' 1
if (Has 'git') { Ok "git: $(git --version)" }
elseif ((Has 'winget') -and (Frage 'git fehlt. Mit winget installieren?')) {
    winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements; Neu-Pfad
    if (-not (Has 'git')) { Ende 'git noch nicht gefunden - neues PowerShell-Fenster oeffnen und das Skript erneut starten.'; return }
} else { Ende 'Ohne git geht es nicht (der Marketplace ist ein Git-Repo).'; return }

if (Python3-Ok) { Ok "Python: $(python3 --version)" }
elseif ((Has 'winget') -and (Frage 'python3 fehlt (die Hooks rufen python3 auf). Python aus dem Microsoft Store mit winget installieren?')) {
    winget install -e --id 9NCVDN91XZQP --source msstore --accept-source-agreements --accept-package-agreements; Neu-Pfad
    if (-not (Python3-Ok)) { Ende 'python3 noch nicht verfuegbar - neues PowerShell-Fenster oeffnen und das Skript erneut starten.'; return }
    Ok "Python: $(python3 --version)"
} else { Ende 'Ohne python3 laufen Skill-Log und Skill-Waechter nicht. Python aus dem Microsoft Store installieren und erneut starten.'; return }

if (Has 'claude') { Ok "Claude Code: $(claude --version)" }
elseif (Frage 'Claude Code fehlt. Mit dem offiziellen Installer installieren (irm https://claude.ai/install.ps1 | iex)?') {
    Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression; Neu-Pfad
    $env:Path += ";$env:USERPROFILE\.local\bin"
    if (-not (Has 'claude')) { Ende 'claude noch nicht im PATH - neues PowerShell-Fenster oeffnen und das Skript erneut starten.'; return }
    Write-Host 'Anmelden: claude starten und /login ausfuehren, danach dieses Skript erneut starten.'; return
} else { Ende 'Ohne Claude Code geht es nicht.'; return }

Schritt "[2/5] Marketplace $Marketplace" 2
function Marketplaces {
    # Unter 5.1 gibt ConvertFrom-Json ein Array als ein einziges Objekt aus - deshalb mit foreach einzeln weitergeben
    $json = (claude plugin marketplace list --json | Out-String)
    if (-not $json.Trim()) { return }
    $list = ConvertFrom-Json $json
    foreach ($m in $list) { $m }
}
if (@(Marketplaces) | Where-Object { $_.name -eq $Marketplace }) { claude plugin marketplace update $Marketplace }
else { claude plugin marketplace add $Repo }
$ort = (@(Marketplaces) | Where-Object { $_.name -eq $Marketplace } | Select-Object -First 1).installLocation
if (-not $ort) { Ende "Marketplace $Marketplace nicht gefunden - Ausgabe oben pruefen."; return }
Ok "Marketplace $Marketplace in $ort"

$weiter = @()
if ($Modus) { $weiter += @('--modus', $Modus) }
if ($RechnerName) { $weiter += @('--host', $RechnerName) }
if ($Ja) { $weiter += '--ja' }
if ($OhneOverrides) { $weiter += '--ohne-overrides' }
Write-Progress -Activity 'Einrichtung workbench' -Status '[3-5/5] Plugins, Einstellungen, Probe der Hooks' -PercentComplete 50
& python3 -I (Join-Path $ort 'tools\einrichten.py') --schritt 3 @weiter
Write-Progress -Activity 'Einrichtung workbench' -Completed
if ($LASTEXITCODE -eq 0) {
    Write-Host ''
    Write-Host '=== FERTIG - Claude Code jetzt neu starten (bzw. die Desktop-App beenden und neu oeffnen) ===' -ForegroundColor Green
} else {
    Write-Host ''
    Write-Host '=== NICHT FERTIG - siehe die rote Meldung oben ===' -ForegroundColor Red
}
# kein exit: beim Start mit "irm ... | iex" wuerde es das PowerShell-Fenster schliessen
