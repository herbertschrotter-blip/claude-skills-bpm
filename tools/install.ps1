# Einrichtung des Marketplace workbench auf Windows (Windows PowerShell 5.1 oder PowerShell 7).
#
#   irm https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.ps1 | iex
#   powershell -ExecutionPolicy Bypass -File tools\install.ps1 [-Modus terminal|desktop] [-RechnerName NAME]
#              [-LogRepo owner/name] [-Ja] [-OhneOverrides]
#   Entfernen:  & ([scriptblock]::Create((irm https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.ps1))) -Entfernen
#               bzw. powershell -ExecutionPolicy Bypass -File tools\install.ps1 -Entfernen
# Protokoll fuer das Entfernen: ~/.claude/workbench-einrichtung.json (was das Skript installiert hat, was schon da war).
#
# Ablauf: Bestandsaufnahme ohne Netz -> Hintergrund-Pruefungen starten -> ALLE Fragen auf einmal -> unbeaufsichtigt
# installieren (winget nacheinander, Claude-Installer als eigener Prozess parallel) -> Marketplace -> einrichten.py
# (Plugins, Optionen, autoUpdate, skillOverrides, Probe) -> optional geplante Aufgabe fuer git-Updates -> Anmeldung.
# Ein erneuter Start setzt sauber fort (jeder Schritt prueft vorher, ob er noetig ist). Fehlerquellen:
# docs/installation.md.
#
# Absichtlich nur ASCII, ohne BOM, ohne param()-Block und ohne exit: so laeuft die Datei auch ueber "irm | iex".

$Repo = 'herbertschrotter-blip/claude-workbench'
$Marketplace = 'workbench'
$Modus = ''; $RechnerName = ''; $LogRepo = $null; $Ja = $false; $OhneOverrides = $false; $Entfernen = $false; $OhneLogin = $false
for ($i = 0; $i -lt $args.Count; $i++) {
    switch ($args[$i]) {
        '-Modus' { $i++; $Modus = $args[$i] }
        '-RechnerName' { $i++; $RechnerName = $args[$i] }
        '-LogRepo' { $i++; $LogRepo = $args[$i] }
        '-Ja' { $Ja = $true }
        '-OhneOverrides' { $OhneOverrides = $true }
        '-Entfernen' { $Entfernen = $true }
        '-OhneLogin' { $OhneLogin = $true }
    }
}

# --- Grundpruefungen, die vor allem anderen kommen muessen ------------------------------------------------------------
if ($ExecutionContext.SessionState.LanguageMode -ne 'FullLanguage') {
    Write-Host "ABBRUCH: PowerShell laeuft im Modus $($ExecutionContext.SessionState.LanguageMode) (AppLocker/WDAC)." -ForegroundColor Red
    Write-Host 'Das Skript braucht FullLanguage. Siehe docs/installation.md, Abschnitt "Eingeschraenkte PowerShell".'
    return
}
$ErrorActionPreference = 'Continue'
try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch { }
$Ise = [bool]$psISE
$Temp = Join-Path $env:TEMP 'workbench-einrichtung'
New-Item -ItemType Directory -Force -Path $Temp | Out-Null
$LocalBin = Join-Path $env:USERPROFILE '.local\bin'
$PsExe = (Get-Process -Id $PID).Path

# --- Ausgabe: Fortschritt oben fest (Write-Progress), Meldungen laufen darunter ----------------------------------------
# Gesamtbalken (Id 1) und darunter eingerueckt ein Balken fuer die laufende Aufgabe (Id 2). Beide bleiben oben stehen
# und scrollen nicht mit. PowerShell 7 zeigt Fortschritt sonst als schmale Zeile unten - deshalb "Classic".
if ($PSStyle) { try { $PSStyle.Progress.View = 'Classic' } catch { } }
$script:Pct = 0; $script:Text = ''
function Balken([int]$Prozent, [string]$Text) {
    $script:Pct = [Math]::Min(100, [Math]::Max($script:Pct, $Prozent)); if ($Text) { $script:Text = $Text }
    Write-Progress -Id 1 -Activity 'Einrichtung workbench' -Status ('{0,3}%  {1}' -f $script:Pct, $script:Text) -PercentComplete $script:Pct
}
function Teil([string]$Aufgabe, [int]$Prozent) {
    $p = [Math]::Min(100, [Math]::Max(0, $Prozent))
    Write-Progress -Id 2 -ParentId 1 -Activity $Aufgabe -Status ('{0,3}%' -f $p) -PercentComplete $p
}
function Teil-Fertig { Write-Progress -Id 2 -ParentId 1 -Activity 'Aufgabe' -Completed }
function Fortschritt-Ende { Teil-Fertig; Write-Progress -Id 1 -Activity 'Einrichtung workbench' -Completed }
function Meldung([string]$Text, [string]$Farbe = 'Gray') { Write-Host $Text -ForegroundColor $Farbe }
function Ok([string]$Text) { Meldung "  OK  $Text" 'Green' }
function Hinweis([string]$Text) { Meldung "  !   $Text" 'Yellow' }
function Fehler([string]$Text) { Meldung "  X   $Text" 'Red' }
function Frage([string]$Text, [bool]$Vorschlag = $true) {
    if ($Ja) { return $Vorschlag }
    $hint = if ($Vorschlag) { 'J/n' } else { 'j/N' }
    $antwort = Read-Host "  $Text [$hint]"
    if (-not $antwort) { return $Vorschlag }
    return ($antwort -match '^(j|ja|y|yes)$')
}
function Eingabe([string]$Text, [string]$Vorschlag) {
    if ($Ja) { return $Vorschlag }
    $antwort = Read-Host "  $Text [$Vorschlag]"
    if ($antwort) { return $antwort.Trim() } else { return $Vorschlag }
}

# --- Hilfen ------------------------------------------------------------------------------------------------------------
function Has([string]$Name) { [bool](Get-Command $Name -ErrorAction SilentlyContinue) }

function Neu-Pfad {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
    if ((Test-Path (Join-Path $LocalBin 'claude.exe')) -and -not (Im-Pfad $LocalBin $env:Path)) { $env:Path += ";$LocalBin" }
}

function Norm([string]$Dir) { ([Environment]::ExpandEnvironmentVariables($Dir)).TrimEnd('\').ToLowerInvariant() }
function Im-Pfad([string]$Dir, [string]$Pfad) { [bool](($Pfad -split ';') | Where-Object { $_ -and ((Norm $_) -eq (Norm $Dir)) }) }

function Pfad-Dauerhaft([string]$Dir) {
    # Benutzer-PATH als REG_EXPAND_SZ ergaenzen. Nie [Environment]::SetEnvironmentVariable('Path', ..., 'User'):
    # das schreibt REG_SZ, und Eintraege mit %USERPROFILE% gehen kaputt.
    $key = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment', $true)
    try {
        $roh = [string]$key.GetValue('Path', '', [Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
        if (-not (Im-Pfad $Dir $roh)) {
            $eintrag = $Dir.Replace($env:USERPROFILE, '%USERPROFILE%')
            $neu = (@($roh.TrimEnd(';')) + $eintrag | Where-Object { $_ }) -join ';'
            $key.SetValue('Path', $neu, [Microsoft.Win32.RegistryValueKind]::ExpandString)
            # WM_SETTINGCHANGE ausloesen, damit neue Fenster (Explorer, Desktop-App) den Pfad sehen
            [Environment]::SetEnvironmentVariable('WORKBENCH_PFAD', '1', 'User')
            [Environment]::SetEnvironmentVariable('WORKBENCH_PFAD', $null, 'User')
            Ok "Benutzer-PATH ergaenzt: $eintrag (neue Fenster und die Desktop-App sehen ihn nach einem Neustart)"
            $script:Protokoll += @{ was = 'pfad'; wert = $eintrag; aktion = 'installiert' }
        }
    } finally { $key.Close() }
    if (-not (Im-Pfad $Dir $env:Path)) { $env:Path += ";$Dir" }
}

function Pfad-Entfernen([string]$Dir) {
    $key = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment', $true)
    try {
        $roh = [string]$key.GetValue('Path', '', [Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
        $rest = @(($roh -split ';') | Where-Object { $_ -and ((Norm $_) -ne (Norm $Dir)) })
        if ($rest.Count -ne @(($roh -split ';') | Where-Object { $_ }).Count) {
            $key.SetValue('Path', ($rest -join ';'), [Microsoft.Win32.RegistryValueKind]::ExpandString)
            [Environment]::SetEnvironmentVariable('WORKBENCH_PFAD', '1', 'User')
            [Environment]::SetEnvironmentVariable('WORKBENCH_PFAD', $null, 'User')
        }
    } finally { $key.Close() }
}

function Python3-Ok {
    # Ohne Python liefert Windows unter dem Namen python3 nur eine Verknuepfung zum Microsoft Store, die mit Fehler
    # endet. Deshalb wirklich ausfuehren und nur Exit 0 mit der richtigen Version zaehlen.
    if (-not (Has 'python3')) { return $false }
    try { $null = & python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>&1; return ($LASTEXITCODE -eq 0) } catch { return $false }
}

function Json([string]$Text) {
    # Unter 5.1 gibt ConvertFrom-Json ein Array als ein einziges Objekt aus - mit foreach einzeln weitergeben
    if (-not $Text -or -not $Text.Trim()) { return }
    try { $obj = ConvertFrom-Json $Text } catch { return }
    foreach ($o in $obj) { $o }
}

function Claude-Json([string[]]$Argumente) { Json ((& claude @Argumente 2>$null) | Out-String) }

function Quote([string[]]$Argumente) {
    # Start-Process fuegt Argumente unter 5.1 ungequotet zusammen: leere Werte und Leerzeichen selbst quoten
    ($Argumente | ForEach-Object { if ($_ -eq '' -or $_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ } }) -join ' '
}

function Starte([string]$Name, [string]$Exe, [string[]]$Argumente) {
    # Eigener Prozess, Ausgabe in Dateien: haelt fremdes exit/StrictMode fern und laesst den Balken weiterlaufen
    $out = Join-Path $Temp "$Name.out.txt"; $err = Join-Path $Temp "$Name.err.txt"
    try {
        $p = Start-Process -FilePath $Exe -ArgumentList (Quote $Argumente) -NoNewWindow -PassThru `
            -RedirectStandardOutput $out -RedirectStandardError $err -ErrorAction Stop
        $null = $p.Handle  # ohne den Zugriff liefert .NET spaeter keinen ExitCode
        return [pscustomobject]@{ Name = $Name; Proc = $p; Out = $out; Err = $err }
    } catch {
        Set-Content -Path $err -Value $_.Exception.Message
        return [pscustomobject]@{ Name = $Name; Proc = $null; Out = $out; Err = $err }
    }
}

function Warte($Aufgaben, [int]$Von, [int]$Bis, [string]$Text) {
    # Dauer unbekannt: Gesamt- und Teilbalken naehern sich mit der Zeit dem Ziel; fertig = Teilbalken 100 %
    $Aufgaben = @($Aufgaben | Where-Object { $_ -and $_.Proc })
    $start = Get-Date
    while ($Aufgaben | Where-Object { -not $_.Proc.HasExited }) {
        $f = 1 - [Math]::Exp(-((Get-Date) - $start).TotalSeconds / 60)
        Balken ([int]($Von + ($Bis - $Von) * $f)) $Text
        Teil $Text ([int](99 * $f))
        Start-Sleep -Milliseconds 400
    }
    Teil $Text 100
    Balken $Bis $Text
    Teil-Fertig
}

function Code($Aufgabe) { if ($Aufgabe -and $Aufgabe.Proc) { $Aufgabe.Proc.WaitForExit(); return $Aufgabe.Proc.ExitCode } else { return -1 } }
function Ausgabe($Aufgabe) { ((Get-Content $Aufgabe.Out -ErrorAction SilentlyContinue) + (Get-Content $Aufgabe.Err -ErrorAction SilentlyContinue)) -join "`n" }
function Letzte($Aufgabe) { ((Ausgabe $Aufgabe) -split "`n" | Where-Object { $_.Trim() } | Select-Object -Last 3) -join ' | ' }

$script:Protokoll = @()
$ProtokollDatei = Join-Path $env:USERPROFILE '.claude\workbench-einrichtung.json'

# --- Entfernen: nur, was laut Protokoll vom Skript stammt ----------------------------------------------------------------
if ($Entfernen) {
    Write-Host ''
    Write-Host '=== workbench entfernen (nur, was die Einrichtung selbst angelegt hat) ===' -ForegroundColor Cyan
    if (-not (Test-Path $ProtokollDatei)) { Fehler "Kein Protokoll ($ProtokollDatei) - nichts zu tun. Von Hand: docs/installation.md, Abschnitt Entfernen."; Fortschritt-Ende; return }
    Neu-Pfad
    if ((Python3-Ok) -and (Has 'claude')) {
        $ort = (Claude-Json @('plugin', 'marketplace', 'list', '--json') | Where-Object { $_.name -eq $Marketplace } | Select-Object -First 1).installLocation
        if ($ort -and (Test-Path (Join-Path $ort 'tools\einrichten.py'))) {
            # Kopie, weil einrichten.py den Marketplace-Ordner selbst entfernt
            Copy-Item (Join-Path $ort 'tools\einrichten.py') (Join-Path $Temp 'einrichten.py') -Force
            $ea = @('-I', (Join-Path $Temp 'einrichten.py'), '--entfernen'); if ($Ja) { $ea += '--ja' }
            & python3 @ea
        } else { Hinweis 'Marketplace nicht gefunden - Plugins und Einstellungen bitte von Hand pruefen.' }
    } else { Hinweis 'python3 oder claude fehlt - Plugins und Einstellungen bitte von Hand pruefen.' }
    $eintraege = @(Json ((Get-Content $ProtokollDatei -Raw -ErrorAction SilentlyContinue) | Out-String) | ForEach-Object { $_.eintraege } | ForEach-Object { $_ })
    $offen = @($eintraege | Where-Object { $_.aktion -eq 'installiert' })
    Write-Host ''; Write-Host '[Entfernen] Windows' -ForegroundColor Cyan
    foreach ($e in $offen) {
        $weg = $false
        switch ($e.was) {
            'aufgabe' { if (Frage "Geplante Aufgabe '$($e.wert)' entfernen?" $true) { Unregister-ScheduledTask -TaskName $e.wert -Confirm:$false -ErrorAction SilentlyContinue; $weg = $true } }
            'pfad' { if (Frage "PATH-Eintrag $($e.wert) entfernen?" $true) { Pfad-Entfernen $e.wert; $weg = $true } }
            'claude' { if (Frage 'Claude Code entfernen (vom Skript installiert; ~/.claude mit Gespraechen und Skill-Log bleibt)?' $false) {
                    Remove-Item -Force (Join-Path $LocalBin 'claude.exe') -ErrorAction SilentlyContinue
                    Remove-Item -Recurse -Force (Join-Path $env:USERPROFILE '.local\share\claude') -ErrorAction SilentlyContinue
                    $weg = $true } }
            'git' { if (Frage 'git entfernen (vom Skript installiert)?' $false) { & winget uninstall -e --id Git.Git --silent --disable-interactivity; $weg = ($LASTEXITCODE -eq 0) } }
            'python' { if (Frage 'Python 3.12 aus dem Store entfernen (vom Skript installiert)?' $false) { & winget uninstall -e --id 9NCVDN91XZQP --disable-interactivity; $weg = ($LASTEXITCODE -eq 0) } }
        }
        if ($weg) { $e.aktion = 'entfernt'; Ok "$($e.was) $($e.wert) entfernt" }
    }
    if (-not @($eintraege | Where-Object { $_.aktion -eq 'installiert' })) {
        Remove-Item -Force $ProtokollDatei -ErrorAction SilentlyContinue; Ok 'Alles zurueckgenommen, Protokoll geloescht.'
    } else {
        (@{ version = 1; eintraege = $eintraege } | ConvertTo-Json -Depth 5) | Set-Content -Path $ProtokollDatei -Encoding UTF8
        Hinweis 'Einiges ist geblieben (abgelehnt) - steht weiter im Protokoll.'
    }
    return
}

# --- 1. Bestandsaufnahme ohne Netz ---------------------------------------------------------------------------------------
Write-Host ''
Write-Host '=== Einrichtung workbench (Skills, Skill-Log, Skill-Waechter) ===' -ForegroundColor Cyan
Balken 1 'Bestandsaufnahme'

if ([Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Hinweis 'PowerShell laeuft als Administrator. Eingerichtet wird fuer das Profil dieses Kontos.'
    if (-not (Frage "Ist das dein normales Konto ($env:USERNAME) und willst du fortfahren?" $false)) { Fehler 'Abgebrochen: bitte ein normales PowerShell-Fenster ohne "Als Administrator" verwenden.'; Fortschritt-Ende; return }
}
if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { Hinweis 'ARM64-Windows: Claude Code hat eine eigene ARM64-Fassung, Python aus dem Store ebenfalls.' }
if ($Ise) { Hinweis 'PowerShell ISE: besser ein normales PowerShell-Fenster.' }

# Claude Code liegt schon unter .local\bin, ist aber nicht im PATH: nur den PATH reparieren, nicht neu installieren
if ((Test-Path (Join-Path $LocalBin 'claude.exe')) -and -not (Im-Pfad $LocalBin ([Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [Environment]::GetEnvironmentVariable('Path', 'Machine')))) {
    Pfad-Dauerhaft $LocalBin
}

$hatGit = Has 'git'
$hatPython = Python3-Ok
$nurPythonOrg = $false
if (-not $hatPython -and (Has 'python')) {
    # "python" gibt es auch als Store-Verknuepfung ohne Python - nur zaehlen, wenn es wirklich laeuft
    try { $null = & python -c 'import sys' 2>&1; $nurPythonOrg = ($LASTEXITCODE -eq 0) } catch { }
}
$hatClaude = Has 'claude'
$wingetVersion = $null
if (Has 'winget') { try { $v = (& winget --version 2>$null | Out-String).Trim(); if ($v -match '(\d+)\.(\d+)') { $wingetVersion = [version]"$($Matches[1]).$($Matches[2])" } } catch { } }
$angemeldet = $false; $marketplaceDa = $false; $plugins = @()
if ($hatClaude) {
    $status = Claude-Json @('auth', 'status')
    $angemeldet = [bool]($status -and $status.loggedIn)
    $marketplaceDa = [bool](Claude-Json @('plugin', 'marketplace', 'list', '--json') | Where-Object { $_.name -eq $Marketplace })
    $plugins = @(Claude-Json @('plugin', 'list', '--json') | Where-Object { $_.id -like "*@$Marketplace" } | ForEach-Object { ($_.id -split '@')[0] })
    if (@(Get-Command claude -All -ErrorAction SilentlyContinue).Count -gt 1) { Hinweis 'Mehrere Claude-Installationen gefunden (z. B. npm und nativ). Pruefen mit: claude doctor' }
}
if ($hatGit) { $script:Protokoll += @{ was = 'git'; wert = 'Git.Git'; aktion = 'war-da' } }
if ($hatPython) { $script:Protokoll += @{ was = 'python'; wert = 'python3'; aktion = 'war-da' } }
if ($hatClaude) { $script:Protokoll += @{ was = 'claude'; wert = 'claude'; aktion = 'war-da' } }
$script:Protokoll += @{ was = 'marketplace'; wert = $Marketplace; aktion = $(if ($marketplaceDa) { 'war-da' } else { 'installiert' }) }
if ($hatGit) { Ok "git: $((git --version) -replace 'git version ', '')" }
if ($hatPython) { Ok "Python: $(python3 --version)" }
if ($hatClaude) { Ok ("Claude Code: $((claude --version) -replace ' \(Claude Code\)', '')" + $(if ($angemeldet) { ', angemeldet' } else { ', nicht angemeldet' })) }
if ($marketplaceDa) { Ok ("Marketplace $Marketplace" + $(if ($plugins) { ', Plugins: ' + ($plugins -join ', ') } else { '' })) }
Balken 5 'Bestandsaufnahme fertig'

# --- 2. Hintergrund-Pruefungen sofort starten ----------------------------------------------------------------------------
$bg = @{}
if ($hatClaude) {
    $bg.marketplace = if ($marketplaceDa) { Starte 'marketplace' 'claude' @('plugin', 'marketplace', 'update', $Marketplace) } else { Starte 'marketplace' 'claude' @('plugin', 'marketplace', 'add', $Repo) }
    $bg.claudeUpdate = Starte 'claude-update' 'claude' @('update')
}
if ($wingetVersion) {
    if ($hatGit) {
        $bg.gitUpdate = Starte 'git-update' 'winget' @('list', '-e', '--id', 'Git.Git', '--upgrade-available', '--accept-source-agreements', '--disable-interactivity')
    } elseif ($wingetVersion -ge [version]'1.8') {
        $bg.gitDownload = Starte 'git-download' 'winget' @('download', '-e', '--id', 'Git.Git', '-d', (Join-Path $Temp 'git'), '--accept-source-agreements', '--accept-package-agreements', '--disable-interactivity')
    }
}

# --- 3. Alle Fragen auf einmal -------------------------------------------------------------------------------------------
Balken 8 'Fragen'
Meldung ''
Meldung '  Bitte einmal alles beantworten - danach laeuft die Einrichtung ohne weitere Fragen.' 'Cyan'
$wollGit = $false; $wollPython = $false; $wollClaude = $false; $wollGitUpdate = $false
if (-not $hatGit) {
    if (-not $wingetVersion) { Fehler 'git fehlt und winget ist nicht da (App-Installer aus dem Microsoft Store). git von https://git-scm.com installieren und das Skript erneut starten.'; Fortschritt-Ende; return }
    $wollGit = Frage 'git fehlt. Mit winget installieren?'
    if (-not $wollGit) { Fehler 'Ohne git geht es nicht (der Marketplace ist ein Git-Repo).'; Fortschritt-Ende; return }
} elseif ($bg.gitUpdate) {
    Warte @($bg.gitUpdate) 8 10 'Pruefe git auf Updates'
    if ((Code $bg.gitUpdate) -eq 0 -and (Ausgabe $bg.gitUpdate) -match 'Git\.Git') {
        $wollGitUpdate = Frage 'Fuer git gibt es ein Update. Jetzt installieren (UAC-Abfrage)?'
    }
}
if (-not $hatPython) {
    if ($nurPythonOrg) { Hinweis 'Python ist da, aber ohne den Befehl python3, den die Hooks aufrufen (typisch fuer python.org). Siehe docs/installation.md.' }
    if (-not $wingetVersion) { Fehler 'python3 fehlt und winget ist nicht da. Python aus dem Microsoft Store installieren und erneut starten.'; Fortschritt-Ende; return }
    $wollPython = Frage 'python3 fehlt (Skill-Log und Waechter brauchen es). Python 3.12 aus dem Microsoft Store mit winget installieren?'
    if (-not $wollPython) { Fehler 'Ohne python3 laufen Skill-Log und Skill-Waechter nicht.'; Fortschritt-Ende; return }
}
if (-not $hatClaude) {
    $wollClaude = Frage 'Claude Code fehlt. Mit dem offiziellen Installer installieren?'
    if (-not $wollClaude) { Fehler 'Ohne Claude Code geht es nicht.'; Fortschritt-Ende; return }
}
if (-not $Modus) {
    $desktop = Frage 'Laeuft Claude hier in der Claude-Desktop-App (Skills kommen aus claude.ai)?' $false
    $Modus = if ($desktop) { 'desktop' } else { 'terminal' }
}
if (-not $RechnerName) {
    # Vorschlag: schon eingerichteter Name (frueherer Lauf), sonst der Windows-Computername
    $vorschlag = $env:COMPUTERNAME.ToLower()
    if ($hatClaude) {
        foreach ($id in @("work@$Marketplace", "work-hooks@$Marketplace")) {
            $cfg = Claude-Json @('plugin', 'configure', $id, '--json')
            if ($cfg -and $cfg.inputs -and $cfg.inputs.log_host) { $vorschlag = [string]$cfg.inputs.log_host; break }
        }
    }
    $RechnerName = Eingabe 'Rechnername im Skill-Log (Enter = Vorschlag)' $vorschlag
}
if ($null -eq $LogRepo) { $LogRepo = Eingabe 'Privates Sammel-Repo fuer das Skill-Log (owner/name, leer = keins)' '' }
$mitOverrides = $false
if ($Modus -eq 'terminal' -and -not $OhneOverrides) {
    $mitOverrides = Frage 'Sind dieselben Skills auch bei claude.ai hochgeladen (dann doppelte im Terminal ausblenden)?' $false
}
$wollAufgabe = $false
if ($wingetVersion -and -not (Get-ScheduledTask -TaskName 'workbench git-Update' -ErrorAction SilentlyContinue)) {
    $wollAufgabe = Frage 'Woechentliche geplante Aufgabe fuer git-Updates anlegen (jeweils mit UAC-Abfrage)?' $true
}

# --- 4. Installieren (winget nacheinander, Claude parallel) -------------------------------------------------------------
Meldung ''
Balken 12 'Installieren'
$claudeJob = $null
if ($wollClaude) {
    # Offizieller Installer im eigenen Prozess: sein exit und Set-StrictMode bleiben dort
    $claudeJob = Starte 'claude-install' $PsExe @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', 'irm https://claude.ai/install.ps1 | iex')
}
$wingetArgs = @('--accept-source-agreements', '--accept-package-agreements', '--disable-interactivity')
if ($wollGit) {
    if ($bg.gitDownload) { Warte @($bg.gitDownload) 12 18 'git wird geladen' }
    $j = Starte 'git-install' 'winget' (@('install', '-e', '--id', 'Git.Git', '--silent') + $wingetArgs)
    Warte @($j, $claudeJob) 18 30 'git wird installiert'
    if ((Code $j) -ne 0) { Fehler "git-Installation gescheitert: $(Letzte $j)"; Fortschritt-Ende; return }
    Ok 'git installiert'
    $script:Protokoll += @{ was = 'git'; wert = 'Git.Git'; aktion = 'installiert' }
}
if ($wollGitUpdate) {
    $j = Starte 'git-upgrade' 'winget' (@('upgrade', '-e', '--id', 'Git.Git', '--silent') + $wingetArgs)
    Warte @($j, $claudeJob) 18 30 'git wird aktualisiert'
    if ((Code $j) -eq 0) { Ok 'git aktualisiert' } else { Hinweis "git-Update gescheitert: $(Letzte $j)" }
}
if ($wollPython) {
    $j = Starte 'python-install' 'winget' (@('install', '-e', '--id', '9NCVDN91XZQP', '--source', 'msstore') + $wingetArgs)
    Warte @($j, $claudeJob) 30 42 'Python wird installiert'
    Neu-Pfad
    if (-not (Python3-Ok)) {
        $text = Letzte $j
        if ($text -match 'msstore|store|policy|0x8a15') { Fehler "Python aus dem Store ging nicht (Store gesperrt?): $text" } else { Fehler "python3 noch nicht verfuegbar: $text" }
        Meldung '      Loesungen: docs/installation.md, Abschnitt "Python". Danach das Skript erneut starten (es setzt fort).'
        Fortschritt-Ende; return
    }
    Ok "Python: $(python3 --version)"
    $script:Protokoll += @{ was = 'python'; wert = 'python3'; aktion = 'installiert' }
}
if ($claudeJob) {
    Warte @($claudeJob) 42 50 'Claude Code wird installiert'
    Neu-Pfad
    if (Test-Path (Join-Path $LocalBin 'claude.exe')) { Pfad-Dauerhaft $LocalBin }
    if (-not (Has 'claude')) {
        $text = Letzte $claudeJob
        Fehler "Claude Code nicht installiert: $text"
        if ($text -match 'region|supported-countries') { Meldung '      Der Download-Dienst ist in dieser Region nicht erreichbar.' }
        else { Meldung '      Proxy, Firewall oder Virenscanner? Siehe docs/installation.md, Abschnitt "Claude Code".' }
        Fortschritt-Ende; return
    }
    Ok "Claude Code: $((claude --version) -replace ' \(Claude Code\)', '')"
    $script:Protokoll += @{ was = 'claude'; wert = 'claude'; aktion = 'installiert' }
    $angemeldet = [bool]((Claude-Json @('auth', 'status')).loggedIn)
}

# --- 5. Marketplace ------------------------------------------------------------------------------------------------------
if (-not $bg.marketplace) {
    $bg.marketplace = Starte 'marketplace' 'claude' @('plugin', 'marketplace', 'add', $Repo)
}
Warte @($bg.marketplace, $bg.claudeUpdate) 50 58 "Marketplace $Marketplace"
$ort = (Claude-Json @('plugin', 'marketplace', 'list', '--json') | Where-Object { $_.name -eq $Marketplace } | Select-Object -First 1).installLocation
if (-not $ort) {
    $text = Letzte $bg.marketplace
    Fehler "Marketplace $Marketplace nicht eingerichtet: $text"
    if ($text -match 'strictKnownMarketplaces|managed|policy') { Meldung '      Verwaltete Einstellungen erlauben diesen Marketplace nicht (Firmenrechner) - IT fragen.' }
    Fortschritt-Ende; return
}
Ok "Marketplace $Marketplace"
if ($bg.claudeUpdate -and (Code $bg.claudeUpdate) -eq 0 -and (Ausgabe $bg.claudeUpdate) -match 'Successfully updated|updated to') { Ok 'Claude Code aktualisiert (gilt ab dem naechsten Start)' }

# --- 6. Geplante Aufgabe fuer git-Updates ------------------------------------------------------------------------------------
if ($wollAufgabe) {
    try {
        $winget = Join-Path $env:LOCALAPPDATA 'Microsoft\WindowsApps\winget.exe'
        $aktion = New-ScheduledTaskAction -Execute $winget -Argument 'upgrade -e --id Git.Git --silent --accept-source-agreements --accept-package-agreements --disable-interactivity'
        $wann = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9am
        $einst = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
        Register-ScheduledTask -TaskName 'workbench git-Update' -Action $aktion -Trigger $wann -Settings $einst `
            -Description 'git woechentlich mit winget aktualisieren (angelegt von claude-workbench tools/install.ps1)' -Force -ErrorAction Stop | Out-Null
        Ok 'Geplante Aufgabe "workbench git-Update" (montags 9 Uhr, holt nach, UAC-Abfrage beim Lauf)'
        $script:Protokoll += @{ was = 'aufgabe'; wert = 'workbench git-Update'; aktion = 'installiert' }
    } catch { Hinweis "Geplante Aufgabe nicht angelegt: $($_.Exception.Message)" }
}


# --- 7. Plugins, Einstellungen, Probe (einrichten.py, meldet seinen Fortschritt ueber ##BALKEN-Zeilen) ---------------------
$zusatz = Join-Path $Temp 'protokoll-zusatz.json'
ConvertTo-Json -InputObject @($script:Protokoll) -Depth 4 | Set-Content -Path $zusatz -Encoding UTF8
$weiter = @('-I', (Join-Path $ort 'tools\einrichten.py'), '--ja', '--balken', '--modus', $Modus, '--host', $RechnerName,
            '--log-repo', $LogRepo, '--protokoll-zusatz', $zusatz)
if ($mitOverrides) { $weiter += '--mit-overrides' } else { $weiter += '--ohne-overrides' }
$py = Starte 'einrichten' 'python3' $weiter
$gelesen = 0
while ($py.Proc -and -not $py.Proc.HasExited) {
    $zeilen = @(Get-Content $py.Out -ErrorAction SilentlyContinue)
    for (; $gelesen -lt $zeilen.Count; $gelesen++) {
        $z = $zeilen[$gelesen]
        if ($z -match '^##BALKEN (\d+) (.*)$') { Balken (58 + [int]$Matches[1] * 30 / 100) 'Plugins und Einstellungen'; Teil $Matches[2] ([int]$Matches[1]) } elseif ($z.Trim()) { Meldung $z }
    }
    Start-Sleep -Milliseconds 300
}
$zeilen = @(Get-Content $py.Out -ErrorAction SilentlyContinue)
for (; $gelesen -lt $zeilen.Count; $gelesen++) { $z = $zeilen[$gelesen]; if ($z -notmatch '^##BALKEN' -and $z.Trim()) { Meldung $z } }
$einrichtenOk = (Code $py) -eq 0
if (-not $einrichtenOk) { Fehler "einrichten.py meldet einen Fehler: $((Get-Content $py.Err -ErrorAction SilentlyContinue | Select-Object -Last 3) -join ' | ')" }
Teil-Fertig
Balken 88 'Plugins eingerichtet'

# --- 8. Anmeldung (claude plugin ... laeuft auch ohne; deshalb erst am Ende) -------------------------------------------------
Balken 92 'Anmeldung'
if (-not $angemeldet -and -not $OhneLogin) {
    Meldung ''
    Meldung '  Claude Code ist noch nicht angemeldet (die Anmeldung der Desktop-App zaehlt fuer das CLI nicht).' 'Cyan'
    Meldung '  Gleich oeffnet sich der Browser - dort anmelden, dann geht es hier weiter.' 'Cyan'
    Fortschritt-Ende
    & claude auth login
    $angemeldet = [bool]((Claude-Json @('auth', 'status')).loggedIn)
    if ($angemeldet) { Ok 'Claude Code angemeldet' } else { Hinweis 'Noch nicht angemeldet - spaeter mit: claude auth login' }
}
Balken 100 'Fertig'
Fortschritt-Ende
Write-Host ''
if ($einrichtenOk -and $angemeldet) {
    Write-Host '=== FERTIG - Claude Code neu starten (bzw. die Desktop-App beenden und neu oeffnen) ===' -ForegroundColor Green
} elseif ($einrichtenOk) {
    Write-Host '=== FERTIG bis auf die Anmeldung - claude auth login, dann Claude Code neu starten ===' -ForegroundColor Yellow
} else {
    Write-Host '=== NICHT FERTIG - siehe die rote Meldung oben; ein erneuter Start setzt fort ===' -ForegroundColor Red
}
# kein exit: beim Start mit "irm ... | iex" wuerde es das PowerShell-Fenster schliessen
