#requires -Version 7.2
<#
.SYNOPSIS
  Prüft die Skills des Skill-Repos mechanisch.

.DESCRIPTION
  Fehler sind eindeutige Regelverstöße (Exit 1): Frontmatter, Name, Description, tote Verweise, doppelte Namen,
  fehlende zentrale Dateien, unbekannte Profil-Version.
  Warnungen sind Hinweise für Umbau und Review (Exit 0): Länge, fehlende Inhaltsverzeichnisse, Historie im Regeltext,
  Werkzeugnamen einer Umgebung, Nummern-Querverweise, Windows-Pfade, Projektbegriffe, Altlasten, fehlende Eval-Fälle.
  Exit 2: Das Prüfskript selbst ist gescheitert.
  Die Regeln stehen in docs/skill-quality.md; was ein Urteil braucht, prüft audit.

.PARAMETER Root
  Wurzel des Skill-Repos. Standard: der Ordner über tools/.

.PARAMETER Skill
  Nur diese Skills prüfen (Ordnernamen unter skills/). Ohne Angabe: alle.

.PARAMETER JsonPath
  Bericht zusätzlich als JSON in diese Datei schreiben.

.PARAMETER Detail
  Alle Fundstellen mit Zeile ausgeben statt höchstens drei je Befund.

.PARAMETER RuleInventory
  Statt zu prüfen: einen Entwurf für das Regel-Inventar eines Refactors in diese Datei schreiben (nur mit genau einem
  -Skill; eine vorhandene Datei wird nicht überschrieben). Der Entwurf enthält Kandidaten – Description, Sätze mit
  Pflichtwörtern, Listenpunkte unter VERBOTEN, Tabellenzeilen, nummerierte Regel-Überschriften –, kein vollständiges
  Regelverständnis. Format und Ablauf: skills/skill-pflege/references/rule-inventory.md.

.EXAMPLE
  pwsh -NoProfile -File tools/validate-skills.ps1
  pwsh -NoProfile -File tools/validate-skills.ps1 -Skill tracker,ticket -JsonPath quality/results/skill-validation.json
  pwsh -NoProfile -File tools/validate-skills.ps1 -Skill audit -RuleInventory docs/skill-refactors/2026-10-01-audit.md
#>
[CmdletBinding()]
param(
    [string]$Root = (Split-Path -Parent $PSScriptRoot),
    [string[]]$Skill,
    [string]$JsonPath,
    [switch]$Detail,
    [string]$RuleInventory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Grenzwerte aus docs/skill-quality.md
$MaxDescription = 1024
$MaxNameLength = 64
$BodyLineTarget = 500
$ReferenceTocThreshold = 100
$ShownFindings = 3

$AllowedFrontmatterKeys = @(
    'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility',
    'disable-model-invocation', 'user-invocable', 'argument-hint', 'model', 'context', 'agent', 'hooks'
)
# Werkzeugnamen einer bestimmten Umgebung; erlaubt nur in Referenzen für Cowork, Lieferung und Desktop Commander
$EnvironmentToolPattern = 'ask_user_input_v0|present_files|create_file|memory_user_edits|recent_chats|conversation_search|tool_search|bash_tool|github:get_file_contents|Desktop Commander:|desktop-commander:'
$EnvironmentReferencePattern = '^references/(cowork|delivery|desktop-commander)[^/]*\.md$'
$ProjectTermPattern = '\bBPM\b|\bHeidi\b|dreame_x60|\bHANDOFF\b|\bBauplan|\bBAUPLAN|herbert-smarthome'
$WindowsPathPattern = '[A-Za-z]:\\|\.\\[\w-]+\\|\\[\w.-]+\.(?:ps1|md|json|js|py|ya?ml|cs|xaml)\b'
# Regel-Kandidaten für -RuleInventory (CGR-2026-09-24-skillsystem r2, Abschnitt 7)
$NormativeUpperPattern = '\b(MUSS|MÜSSEN|NIE|NIEMALS|IMMER|PFLICHT|VERBOTEN|KEIN|KEINE|KEINEN|NUR)\b'
$NormativePattern = '(?i)\b(muss|müssen|darf nicht|dürfen nicht|nie|niemals|immer|pflicht\w*|verboten)\b'
$NumberedRuleHeadingPattern = '^(\d+[a-z]?\.|Schritt\s+\d+[a-z]?\b|Regel\s+\d+)'
$RuleCoreLength = 140

function Get-FileLines([string]$Path) {
    return (Get-Content -LiteralPath $Path -Raw -Encoding utf8) -split "\r?\n"
}

function Measure-Characters([string]$Text) {
    return @($Text.EnumerateRunes()).Count
}

# Entfernt nur ein umschließendes Paar gleicher Anführungszeichen (YAML), nicht alle an den Enden.
function Remove-OuterQuotes([string]$Value) {
    if ($Value.Length -ge 2 -and ($Value[0] -eq '"' -or $Value[0] -eq "'") -and $Value[-1] -eq $Value[0]) {
        return $Value.Substring(1, $Value.Length - 2)
    }
    return $Value
}

function Read-Frontmatter([string[]]$Lines) {
    if ($Lines.Count -lt 2 -or $Lines[0].Trim() -ne '---') { return $null }
    $end = -1
    for ($i = 1; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i].Trim() -eq '---') { $end = $i; break }
    }
    if ($end -lt 0) { return $null }

    $values = [ordered]@{}
    $i = 1
    while ($i -lt $end) {
        $line = $Lines[$i]
        if ($line -match '^([A-Za-z0-9_-]+):\s*(.*)$') {
            $key = $Matches[1]
            $value = $Matches[2].Trim()
            if ($value -match '^[>|][+-]?$') {
                $block = [System.Collections.Generic.List[string]]::new()
                $i++
                while ($i -lt $end -and ($Lines[$i] -match '^\s' -or $Lines[$i].Trim() -eq '')) {
                    if ($Lines[$i].Trim() -ne '') { $block.Add($Lines[$i].Trim()) }
                    $i++
                }
                $values[$key] = ($block -join ' ')
                continue
            }
            $values[$key] = Remove-OuterQuotes $value
        }
        $i++
    }
    return @{ Fields = $values; End = $end }
}

function Find-Lines([string[]]$Lines, [string]$Pattern, [int]$Offset = 0) {
    $found = [System.Collections.Generic.List[object]]::new()
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match $Pattern) { $found.Add(@{ Line = $i + 1 + $Offset; Text = $Lines[$i].Trim() }) }
    }
    return ,$found
}

function Format-Findings([string]$File, $Findings) {
    $take = if ($Detail) { $Findings.Count } else { [Math]::Min($ShownFindings, $Findings.Count) }
    $parts = for ($k = 0; $k -lt $take; $k++) {
        $text = $Findings[$k].Text
        if ($text.Length -gt 70) { $text = $text.Substring(0, 67) + '...' }
        "${File}:$($Findings[$k].Line) »$text«"
    }
    $more = if ($Findings.Count -gt $take) { " (+$($Findings.Count - $take) weitere)" } else { '' }
    return ($parts -join '; ') + $more
}

function Test-HasTableOfContents([string[]]$Lines) {
    $head = $Lines | Select-Object -First 30
    if (@($head | Where-Object { $_ -match '^#{1,4}\s*(Inhalt|Inhaltsverzeichnis|Contents|Table of contents)\b' }).Count -gt 0) {
        return $true
    }
    return @($head | Where-Object { $_ -match '^\s*[-*]\s*\[[^\]]+\]\(#' }).Count -ge 3
}

function Get-DeadLinks([string]$File, [string[]]$Lines, [string]$SkillDir, [string]$RepoRoot) {
    $dead = [System.Collections.Generic.List[object]]::new()
    $fileDir = Split-Path -Parent $File
    $inFence = $false
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        # Vorlagen und Beispiele in Codeblöcken sind keine echten Verweise
        if ($Lines[$i] -match '^\s*(```|~~~)') { $inFence = -not $inFence; continue }
        if ($inFence) { continue }
        foreach ($m in [regex]::Matches($Lines[$i], '\[[^\]\n]*\]\(([^)\s]+)\)')) {
            $target = $m.Groups[1].Value
            if ($target -match '^(https?:|mailto:|#)' -or $target -match '[<>*{}$]') { continue }
            $pathPart = ($target -split '#')[0]
            if ($pathPart -eq '') { continue }
            if (-not (Test-Path -LiteralPath (Join-Path $fileDir $pathPart))) {
                $dead.Add(@{ Line = $i + 1; Text = $target })
            }
        }
        foreach ($m in [regex]::Matches($Lines[$i], '`(references/[^`\s]+?\.md)`')) {
            $target = $m.Groups[1].Value
            if ($target -match '[<>*{}$]') { continue }
            if (-not (Test-Path -LiteralPath (Join-Path $SkillDir $target))) { $dead.Add(@{ Line = $i + 1; Text = $target }) }
        }
        foreach ($m in [regex]::Matches($Lines[$i], '`(skills/[a-z0-9-]+/[^`\s]+?)`')) {
            $target = $m.Groups[1].Value
            if ($target -match '[<>*{}$]') { continue }
            if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot $target))) { $dead.Add(@{ Line = $i + 1; Text = $target }) }
        }
    }
    return ,$dead
}

function Get-EvalCoverage([string]$RepoRoot) {
    $covered = @{}
    $evalRoot = Join-Path $RepoRoot 'quality/evals'
    if (-not (Test-Path -LiteralPath $evalRoot)) { return $covered }
    foreach ($grader in Get-ChildItem -LiteralPath $evalRoot -Recurse -File -Filter '*.md' |
            Where-Object { $_.Directory.Name -eq 'graders' }) {
        $fm = Read-Frontmatter @(Get-FileLines $grader.FullName)
        if ($null -eq $fm) { continue }
        $v = $fm.Fields
        if ($v['type'] -ne 'tool_used' -or $v['tool'] -ne 'Skill') { continue }
        if ($v.Contains('max') -and $v['max'] -eq '0') { continue }
        $match = [regex]::Match([string]$v['input_match'], ':\)\?([a-z0-9-]+)"')
        if ($match.Success) { $covered[$match.Groups[1].Value] = $true }
    }
    return $covered
}

# Plugin-Manifeste: Claude Code lehnt ein Plugin bei einem unbekannten Eintrag ab, Pfade beginnen mit ./
# Ohne version gilt der Git-Commit als Version: jeder Push kommt als Update an (gewollt, siehe docs/skillsystem-umbau.md)
$PluginKeys = @('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords', 'commands',
    'agents', 'skills', 'hooks', 'mcpServers', 'outputStyles', 'lspServers', 'userConfig', 'dependencies', 'experimental')
$MarketplaceKeys = @('$schema', 'name', 'owner', 'description', 'version', 'metadata', 'plugins', 'forceRemoveDeletedPlugins')
$EntryKeys = @('name', 'source', 'description', 'version', 'author', 'homepage', 'repository', 'license', 'keywords',
    'category', 'tags', 'strict', 'commands', 'agents', 'skills', 'hooks', 'mcpServers', 'outputStyles', 'lspServers',
    'userConfig', 'dependencies')
$PathKeys = @('commands', 'agents', 'skills', 'hooks', 'mcpServers', 'outputStyles', 'lspServers')

function Read-Json([string]$Path, $Errors, [string]$Rel) {
    try { return Get-Content -LiteralPath $Path -Raw -Encoding utf8 | ConvertFrom-Json -AsHashtable }
    catch { $Errors.Add("${Rel}: kein gültiges JSON ($($_.Exception.Message))"); return $null }
}

# JSON mit sortierten Schlüsseln, damit zwei Hashtables unabhängig von der Reihenfolge vergleichbar sind
function ConvertTo-SortedJson($Value) {
    if ($Value -is [System.Collections.IDictionary]) {
        $parts = foreach ($key in ($Value.Keys | Sort-Object)) { (ConvertTo-Json $key -Compress) + ':' + (ConvertTo-SortedJson $Value[$key]) }
        return '{' + ($parts -join ',') + '}'
    }
    if ($Value -is [System.Collections.IEnumerable] -and $Value -isnot [string]) {
        return '[' + ((@($Value) | ForEach-Object { ConvertTo-SortedJson $_ }) -join ',') + ']'
    }
    return (ConvertTo-Json $Value -Compress)
}

function Test-PluginFolder([string]$Folder, [string]$RepoRoot, [string]$ExpectedName, $Errors, $Warnings) {
    $rel = [System.IO.Path]::GetRelativePath($RepoRoot, $Folder) -replace '\\', '/'
    $manifest = Join-Path $Folder '.claude-plugin/plugin.json'
    if (-not (Test-Path -LiteralPath $manifest)) { $Errors.Add("${rel}: .claude-plugin/plugin.json fehlt"); return }
    $data = Read-Json $manifest $Errors "$rel/.claude-plugin/plugin.json"
    if ($null -eq $data) { return }
    foreach ($key in $data.Keys) {
        if ($key -notin $PluginKeys) { $Errors.Add("$rel/.claude-plugin/plugin.json: unbekannter Eintrag »$key« (Claude Code lehnt das Plugin ab)") }
    }
    if ($data['name'] -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$') { $Errors.Add("$rel/.claude-plugin/plugin.json: name fehlt oder ist nicht kebab-case") }
    elseif ($ExpectedName -and $data['name'] -ne $ExpectedName) { $Errors.Add("$rel/.claude-plugin/plugin.json: name »$($data['name'])« weicht vom Marketplace-Eintrag »$ExpectedName« ab") }
    foreach ($key in $PathKeys) {
        if (-not $data.ContainsKey($key)) { continue }
        foreach ($value in @($data[$key])) {
            if ($value -is [string] -and -not $value.StartsWith('./')) { $Errors.Add("$rel/.claude-plugin/plugin.json: Pfad in »$key« beginnt nicht mit ./ ($value)") }
        }
    }
    $hooksFile = Join-Path $Folder 'hooks/hooks.json'
    if (Test-Path -LiteralPath $hooksFile) {
        $text = Get-Content -LiteralPath $hooksFile -Raw -Encoding utf8
        if ($null -ne (Read-Json $hooksFile $Errors "$rel/hooks/hooks.json")) {
            foreach ($m in [regex]::Matches($text, '\$\{CLAUDE_PLUGIN_ROOT\}/([^"\\\s]+)')) {
                if (-not (Test-Path -LiteralPath (Join-Path $Folder $m.Groups[1].Value))) { $Errors.Add("$rel/hooks/hooks.json: Skript fehlt: $($m.Groups[1].Value)") }
            }
        }
    }
}

function Test-Marketplace([string]$RepoRoot, $Errors, $Warnings) {
    $file = Join-Path $RepoRoot '.claude-plugin/marketplace.json'
    if (-not (Test-Path -LiteralPath $file)) { return }
    $data = Read-Json $file $Errors '.claude-plugin/marketplace.json'
    if ($null -eq $data) { return }
    foreach ($key in $data.Keys) {
        if ($key -notin $MarketplaceKeys) { $Errors.Add(".claude-plugin/marketplace.json: unbekannter Eintrag »$key«") }
    }
    if ($data['name'] -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$') { $Errors.Add('.claude-plugin/marketplace.json: name fehlt oder ist nicht kebab-case') }
    if (-not $data['owner'] -or -not $data['owner']['name']) { $Errors.Add('.claude-plugin/marketplace.json: owner.name fehlt') }
    $seen = @{}
    $owners = @{}
    foreach ($entry in @($data['plugins'])) {
        $name = $entry['name']
        foreach ($key in $entry.Keys) {
            if ($key -notin $EntryKeys) { $Errors.Add(".claude-plugin/marketplace.json: Plugin »$name« mit unbekanntem Eintrag »$key«") }
        }
        if ($seen.ContainsKey("$name")) { $Errors.Add(".claude-plugin/marketplace.json: Plugin »$name« doppelt") }
        $seen["$name"] = $true
        $source = $entry['source']
        if ($source -isnot [string]) { continue }  # GitHub- oder URL-Quellen prüft Claude Code selbst
        if (-not $source.StartsWith('./')) { $Errors.Add(".claude-plugin/marketplace.json: source von »$name« beginnt nicht mit ./ ($source)"); continue }
        $sub = $source.Substring(2).TrimEnd('/')
        $folder = if ($sub) { Join-Path $RepoRoot $sub } else { $RepoRoot }
        if (-not (Test-Path -LiteralPath $folder -PathType Container)) { $Errors.Add(".claude-plugin/marketplace.json: Ordner von »$name« fehlt ($source)"); continue }
        if ($entry.ContainsKey('strict') -and $entry['strict'] -eq $false) {
            Test-MarketplaceEntry $entry $folder $Errors $Warnings $owners
        } else {
            Test-PluginFolder $folder $RepoRoot $name $Errors $Warnings
        }
    }
    # Jeder Skill gehört zu höchstens einem Plugin; Skills ohne Plugin (z. B. nur für Cowork) sind ein Hinweis
    foreach ($skill in $owners.Keys) {
        if ($owners[$skill].Count -gt 1) { $Errors.Add(".claude-plugin/marketplace.json: Skill »$skill« steht in mehreren Plugins ($($owners[$skill] -join ', '))") }
    }
    $skillsRoot = Join-Path $RepoRoot 'skills'
    if ($owners.Count -gt 0 -and (Test-Path -LiteralPath $skillsRoot)) {
        foreach ($folder in Get-ChildItem -LiteralPath $skillsRoot -Directory) {
            if (-not $owners.ContainsKey($folder.Name)) { $Warnings.Add(".claude-plugin/marketplace.json: Skill »$($folder.Name)« gehört zu keinem Plugin") }
        }
    }
}

# Eintrag mit strict: false – der Eintrag selbst beschreibt das Plugin (Skills als Pfade, Hooks direkt eingetragen)
function Test-MarketplaceEntry($Entry, [string]$Folder, $Errors, $Warnings, $Owners) {
    $name = $Entry['name']
    $where = ".claude-plugin/marketplace.json: Plugin »$name«"
    if ($name -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$') { $Errors.Add("${where}: name ist nicht kebab-case") }
    if (Test-Path -LiteralPath (Join-Path $Folder '.claude-plugin/plugin.json')) {
        $Errors.Add("${where}: strict: false, aber im Quellordner liegt eine .claude-plugin/plugin.json (Claude Code meldet widersprüchliche Manifeste)")
    }
    foreach ($key in $PathKeys) {
        if (-not $Entry.ContainsKey($key) -or $key -eq 'hooks') { continue }
        foreach ($value in @($Entry[$key])) {
            if ($value -isnot [string]) { continue }
            if (-not $value.StartsWith('./')) { $Errors.Add("${where}: Pfad in »$key« beginnt nicht mit ./ ($value)"); continue }
            $target = Join-Path $Folder $value.Substring(2)
            if (-not (Test-Path -LiteralPath $target)) { $Errors.Add("${where}: Pfad in »$key« fehlt ($value)"); continue }
            if ($key -eq 'skills') {
                if (-not (Test-Path -LiteralPath (Join-Path $target 'SKILL.md'))) { $Errors.Add("${where}: $value hat keine SKILL.md") }
                $skill = Split-Path -Leaf $target
                if (-not $Owners.ContainsKey($skill)) { $Owners[$skill] = [System.Collections.Generic.List[string]]::new() }
                $Owners[$skill].Add($name)
            }
        }
    }
    if ($Entry.ContainsKey('hooks')) {
        if ($Entry['hooks'] -is [string] -or $Entry['hooks'] -is [array]) {
            $Errors.Add("${where}: hooks als Dateipfad oder Liste geht im Marketplace-Eintrag nicht – direkt als Objekt eintragen")
        } else {
            $text = $Entry['hooks'] | ConvertTo-Json -Depth 20
            foreach ($m in [regex]::Matches($text, '\$\{CLAUDE_PLUGIN_ROOT\}/([^"\\\s]+)')) {
                if (-not (Test-Path -LiteralPath (Join-Path $Folder $m.Groups[1].Value))) { $Errors.Add("${where}: Hook-Skript fehlt: $($m.Groups[1].Value)") }
            }
            # Liegen die Skripte in einem Plugin-Ordner mit eigener hooks.json (z. B. work-hooks), müssen beide Hooks gleich sein
            $pluginDirs = @([regex]::Matches($text, '\$\{CLAUDE_PLUGIN_ROOT\}/(plugins/[^/"]+)/') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
            foreach ($dir in $pluginDirs) {
                $hooksFile = Join-Path $Folder "$dir/hooks/hooks.json"
                if (-not (Test-Path -LiteralPath $hooksFile)) { continue }
                $other = Read-Json $hooksFile $Errors "$dir/hooks/hooks.json"
                if ($null -eq $other -or -not $other.ContainsKey('hooks')) { continue }
                $mine = (ConvertTo-SortedJson $Entry['hooks']).Replace('${CLAUDE_PLUGIN_ROOT}/' + $dir + '/', '${CLAUDE_PLUGIN_ROOT}/')
                if ($mine -ne (ConvertTo-SortedJson $other['hooks'])) {
                    $Errors.Add("${where}: Hooks weichen von $dir/hooks/hooks.json ab – beide gleich halten (nur der Pfad $dir/ unterscheidet sich)")
                }
                # Plugin-Optionen (userConfig) gleich wie im Manifest des Plugin-Ordners, weil die Hooks dieselben Optionen lesen
                $manifest = Join-Path $Folder "$dir/.claude-plugin/plugin.json"
                if (Test-Path -LiteralPath $manifest) {
                    $plugin = Read-Json $manifest $Errors "$dir/.claude-plugin/plugin.json"
                    if ($null -ne $plugin -and (ConvertTo-SortedJson $Entry['userConfig']) -ne (ConvertTo-SortedJson $plugin['userConfig'])) {
                        $Errors.Add("${where}: userConfig weicht von $dir/.claude-plugin/plugin.json ab – beide gleich halten")
                    }
                }
            }
        }
    }
}

function Invoke-Validation {
    $repoRoot = (Resolve-Path -LiteralPath $Root).Path
    $skillsRoot = Join-Path $repoRoot 'skills'
    if (-not (Test-Path -LiteralPath $skillsRoot)) { throw "Ordner skills/ nicht gefunden unter $repoRoot" }

    $allFolders = @(Get-ChildItem -LiteralPath $skillsRoot -Directory | Sort-Object Name)
    $skillNames = @($allFolders | ForEach-Object Name)
    $folders = if ($Skill) {
        $unknown = @($Skill | Where-Object { $_ -notin $skillNames })
        if ($unknown.Count -gt 0) { throw "Unbekannte Skills: $($unknown -join ', ')" }
        @($allFolders | Where-Object { $_.Name -in $Skill })
    } else { $allFolders }

    $skillAlternation = ($skillNames | ForEach-Object { [regex]::Escape($_) }) -join '|'
    $historyPattern = "\b20\d\d-\d\d-\d\d\b|\b\d{1,2}\.\d{1,2}\.20\d\d\b|\bseit\s+(?:v?\d|dem\s+\d)|\bTeil\s+\d+\b|" +
        "\b(?:$skillAlternation)-0\d\d\b|\bAdressiert\b|\bv0\.\d+(?:\.\d+)?\b"
    $numberedReferencePattern = "\b(?:$skillAlternation)\b[^\n]{0,25}?\b(?:Kapitel|Regel|Modus|Schritt|Abschnitt)\s+\d"

    $coverage = Get-EvalCoverage $repoRoot
    $repoErrors = [System.Collections.Generic.List[string]]::new()
    $repoWarnings = [System.Collections.Generic.List[string]]::new()
    $results = [System.Collections.Generic.List[object]]::new()
    $seenNames = @{}

    foreach ($folder in $folders) {
        $errors = [System.Collections.Generic.List[string]]::new()
        $warnings = [System.Collections.Generic.List[string]]::new()
        $result = [ordered]@{
            name = $folder.Name; lines = 0; bodyLines = 0; descriptionLength = 0; references = 0
            errors = $errors; warnings = $warnings
        }
        $results.Add($result)

        $skillFile = Join-Path $folder.FullName 'SKILL.md'
        if (-not (Test-Path -LiteralPath $skillFile)) { $errors.Add('SKILL.md fehlt'); continue }
        $lines = @(Get-FileLines $skillFile)
        $result.lines = $lines.Count

        $fm = Read-Frontmatter $lines
        if ($null -eq $fm) {
            $errors.Add('kein gültiges Frontmatter (--- am Anfang und am Ende)')
        } else {
            $result.bodyLines = $lines.Count - $fm.End - 1
            $v = $fm.Fields
            $name = [string]$v['name']
            if ([string]::IsNullOrWhiteSpace($name)) {
                $errors.Add('name fehlt')
            } else {
                if ($name -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$') { $errors.Add("name »$name« ist nicht kebab-case") }
                if ($name.Length -gt $MaxNameLength) { $errors.Add("name länger als $MaxNameLength Zeichen") }
                if ($name -match 'anthropic|claude') { $errors.Add("name »$name« enthält ein reserviertes Wort") }
                if ($name -ne $folder.Name) { $warnings.Add("name »$name« weicht vom Ordnernamen ab") }
                if ($seenNames.ContainsKey($name)) { $repoErrors.Add("Skill-Name »$name« doppelt ($($seenNames[$name]), $($folder.Name))") }
                else { $seenNames[$name] = $folder.Name }
            }
            $description = [string]$v['description']
            if ([string]::IsNullOrWhiteSpace($description)) {
                $errors.Add('description fehlt oder ist leer')
            } else {
                $length = Measure-Characters $description
                $result.descriptionLength = $length
                if ($length -gt $MaxDescription) { $errors.Add("description hat $length Zeichen (höchstens $MaxDescription)") }
                if ($description -match '[<>]') { $errors.Add('description enthält spitze Klammern') }
                if ($description -notmatch 'Do not trigger') { $warnings.Add('description ohne »Do not trigger«-Teil') }
                if ($description -match '\bBPM\b|\bHeidi\b') { $warnings.Add('description nennt ein Projekt (BPM/Heidi)') }
            }
            $unknownKeys = @($v.Keys | Where-Object { $_ -notin $AllowedFrontmatterKeys })
            if ($unknownKeys.Count -gt 0) { $warnings.Add("unbekannte Frontmatter-Schlüssel: $($unknownKeys -join ', ')") }
            if ($result.bodyLines -ge $BodyLineTarget) {
                $warnings.Add("SKILL.md-Körper hat $($result.bodyLines) Zeilen (Richtwert unter $BodyLineTarget)")
            }
        }

        # Alle Markdown-Dateien des Skills: SKILL.md und references/**
        $files = [System.Collections.Generic.List[object]]::new()
        $files.Add(@{ Rel = 'SKILL.md'; Full = $skillFile; Lines = $lines })
        $referenceRoot = Join-Path $folder.FullName 'references'
        if (Test-Path -LiteralPath $referenceRoot) {
            foreach ($ref in Get-ChildItem -LiteralPath $referenceRoot -Recurse -File -Filter '*.md' | Sort-Object FullName) {
                $rel = [System.IO.Path]::GetRelativePath($folder.FullName, $ref.FullName) -replace '\\', '/'
                $refLines = @(Get-FileLines $ref.FullName)
                $files.Add(@{ Rel = $rel; Full = $ref.FullName; Lines = $refLines })
                $result.references++
                if ($refLines.Count -gt $ReferenceTocThreshold -and -not (Test-HasTableOfContents $refLines)) {
                    $warnings.Add("$rel hat $($refLines.Count) Zeilen ohne Inhaltsverzeichnis")
                }
            }
        }

        foreach ($f in $files) {
            $dead = Get-DeadLinks $f.Full $f.Lines $folder.FullName $repoRoot
            if ($dead.Count -gt 0) { $errors.Add("toter Verweis: $(Format-Findings $f.Rel $dead)") }

            $history = Find-Lines $f.Lines $historyPattern
            if ($history.Count -gt 0) { $warnings.Add("$($history.Count) Zeilen mit Historie: $(Format-Findings $f.Rel $history)") }

            if ($f.Rel -notmatch $EnvironmentReferencePattern) {
                $tools = Find-Lines $f.Lines $EnvironmentToolPattern
                if ($tools.Count -gt 0) { $warnings.Add("$($tools.Count) Zeilen mit Werkzeugnamen einer Umgebung: $(Format-Findings $f.Rel $tools)") }
            }

            $numbered = Find-Lines $f.Lines $numberedReferencePattern
            if ($numbered.Count -gt 0) { $warnings.Add("$($numbered.Count) Querverweise über Nummern: $(Format-Findings $f.Rel $numbered)") }

            $windows = Find-Lines $f.Lines $WindowsPathPattern
            if ($windows.Count -gt 0) { $warnings.Add("$($windows.Count) Zeilen mit Windows-Pfad: $(Format-Findings $f.Rel $windows)") }

            $project = Find-Lines $f.Lines $ProjectTermPattern
            if ($project.Count -gt 0) { $warnings.Add("$($project.Count) Zeilen mit Projektbegriffen in $($f.Rel)") }
        }

        if (Test-Path -LiteralPath (Join-Path $folder.FullName 'test-prompts.md')) {
            $warnings.Add('test-prompts.md ist eine Altlast – Eval-Fälle gehören nach quality/evals/')
        }
        foreach ($zip in Get-ChildItem -LiteralPath $folder.FullName -Recurse -File -Filter '*.zip') {
            $warnings.Add("Zip im Skill-Ordner: $([System.IO.Path]::GetRelativePath($folder.FullName, $zip.FullName) -replace '\\', '/')")
        }
        if (-not $coverage.ContainsKey($folder.Name)) { $warnings.Add('kein Eval-Fall, der diesen Skill auslösen soll') }
    }

    # Prüfungen für das ganze Repo
    foreach ($central in '.claude-plugin/marketplace.json', 'quality/.claude-plugin/plugin.json', 'docs/skill-quality.md', 'docs/skill-profile-v1.md') {
        if (-not (Test-Path -LiteralPath (Join-Path $repoRoot $central))) { $repoErrors.Add("zentrale Datei fehlt: $central") }
    }
    $claudeFile = Join-Path $repoRoot 'CLAUDE.md'
    if (Test-Path -LiteralPath $claudeFile) {
        $claudeText = Get-Content -LiteralPath $claudeFile -Raw -Encoding utf8
        if ($claudeText -match '(?m)^## Skill-Profil\s*$') {
            if ($claudeText -match '(?m)^- Profil-Version:\s*(\S+)') {
                if ($Matches[1] -ne '1') { $repoErrors.Add("unbekannte Profil-Version »$($Matches[1])« in CLAUDE.md (erlaubt: 1)") }
            } else { $repoErrors.Add('Skill-Profil in CLAUDE.md ohne »Profil-Version«') }
        } else { $repoWarnings.Add('CLAUDE.md hat noch kein »## Skill-Profil«') }
    }
    if (Test-Path -LiteralPath (Join-Path $repoRoot 'projects')) {
        $repoWarnings.Add('projects/ existiert noch – Projektwerte gehören nicht ins Skill-Repo (Umbau Phase 6/7)')
    }
    foreach ($zip in Get-ChildItem -LiteralPath $skillsRoot -File -Filter '*.zip') {
        $repoWarnings.Add("Zip direkt unter skills/: $($zip.Name)")
    }
    Test-Marketplace $repoRoot $repoErrors $repoWarnings

    $errorCount = $repoErrors.Count + ($results | ForEach-Object { $_.errors.Count } | Measure-Object -Sum).Sum
    $warningCount = $repoWarnings.Count + ($results | ForEach-Object { $_.warnings.Count } | Measure-Object -Sum).Sum
    return [ordered]@{
        schemaVersion = 1
        status = if ($errorCount -eq 0) { 'pass' } else { 'fail' }
        root = $repoRoot
        summary = [ordered]@{ skills = $results.Count; errors = [int]$errorCount; warnings = [int]$warningCount }
        repo = [ordered]@{ errors = $repoErrors; warnings = $repoWarnings }
        skills = $results
    }
}

function Get-CleanHeading([string]$Text) {
    $clean = $Text -replace '[\p{So}\p{Cs}️‍]', '' -replace '\*\*|`', ''
    return ($clean -replace '\s{2,}', ' ').Trim()
}

function Format-RuleCore([string]$Text) {
    $core = ($Text -replace '(?<!\\)\|', '\|').Trim()
    if ($core.Length -gt $RuleCoreLength) { $core = $core.Substring(0, $RuleCoreLength - 1) + '…' }
    return $core
}

# Kandidaten einer Datei: Pflichtwörter, Listenpunkte unter VERBOTEN, Tabellenzeilen, nummerierte Regel-Überschriften
function Get-RuleCandidates([string]$Rel, [string[]]$Lines, [int]$Start) {
    $found = [System.Collections.Generic.List[object]]::new()
    $heading = 'Anfang'
    $inFence = $false
    $inTable = $false
    for ($i = $Start; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match '^\s*(```|~~~)') { $inFence = -not $inFence; $inTable = $false; continue }
        if ($inFence) { continue }
        $line = $Lines[$i].Trim()
        if ($line -eq '') { $inTable = $false; continue }
        $text = $null
        if ($line -match '^#{1,6}\s+(.+)$') {
            $heading = Get-CleanHeading $Matches[1]
            $inTable = $false
            if ($heading -match $NumberedRuleHeadingPattern) { $text = $heading }
        } elseif ($line.StartsWith('|')) {
            # Die erste Zeile einer Tabelle ist der Kopf, die zweite die Trennzeile
            $isHeader = -not $inTable
            $inTable = $true
            if (-not $isHeader -and $line -notmatch '^\|[\s:|-]+\|?$') {
                $cells = @(($line.Trim('|') -split '(?<!\\)\|') | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' })
                $text = $cells -join ' / '
            }
        } else {
            $inTable = $false
            $isListItem = $line -match '^([-*+]|\d+\.)\s+\S'
            if (($isListItem -and $heading -match 'VERBOTEN') -or $line -cmatch $NormativeUpperPattern -or $line -match $NormativePattern) {
                $text = $line -replace '^([-*+]|\d+\.)\s+', ''
            }
        }
        if ($text) { $found.Add(@{ Rel = $Rel; Heading = $heading; Line = $i + 1; Text = $text }) }
    }
    return ,$found
}

function Export-RuleInventory {
    $repoRoot = (Resolve-Path -LiteralPath $Root).Path
    if (-not $Skill -or @($Skill).Count -ne 1) { throw '-RuleInventory braucht genau einen Skill (-Skill <name>)' }
    $skillName = @($Skill)[0]
    $folder = Join-Path $repoRoot "skills/$skillName"
    $skillFile = Join-Path $folder 'SKILL.md'
    if (-not (Test-Path -LiteralPath $skillFile)) { throw "SKILL.md nicht gefunden: skills/$skillName" }
    $target = if ([System.IO.Path]::IsPathRooted($RuleInventory)) { $RuleInventory } else { Join-Path (Get-Location) $RuleInventory }
    if (Test-Path -LiteralPath $target) { throw "Datei existiert schon: $target – ein Inventar wird nicht überschrieben" }

    $candidates = [System.Collections.Generic.List[object]]::new()
    $sources = [System.Collections.Generic.List[string]]::new()
    $lines = @(Get-FileLines $skillFile)
    $sources.Add('SKILL.md')
    $start = 0
    $fm = Read-Frontmatter $lines
    if ($null -ne $fm) {
        $start = $fm.End + 1
        $descriptionLine = @(Find-Lines @($lines[0..$fm.End]) '^description:')
        $lineNumber = if ($descriptionLine.Count -gt 0) { $descriptionLine[0].Line } else { 1 }
        $candidates.Add(@{ Rel = 'SKILL.md'; Heading = 'Frontmatter'; Line = $lineNumber; Text = "description: $($fm.Fields['description'])" })
    }
    foreach ($c in (Get-RuleCandidates 'SKILL.md' $lines $start)) { $candidates.Add($c) }
    $referenceRoot = Join-Path $folder 'references'
    if (Test-Path -LiteralPath $referenceRoot) {
        foreach ($ref in Get-ChildItem -LiteralPath $referenceRoot -Recurse -File -Filter '*.md' | Sort-Object FullName) {
            $rel = [System.IO.Path]::GetRelativePath($folder, $ref.FullName) -replace '\\', '/'
            $sources.Add($rel)
            foreach ($c in (Get-RuleCandidates $rel @(Get-FileLines $ref.FullName) 0)) { $candidates.Add($c) }
        }
    }

    $commit = 'unbekannt'
    $head = git -C $repoRoot rev-parse --short HEAD 2>$null
    if ($LASTEXITCODE -eq 0 -and $head) { $commit = "$head".Trim() }
    $today = Get-Date -Format 'yyyy-MM-dd'

    $out = [System.Collections.Generic.List[string]]::new()
    $out.Add("# Regel-Inventar – $skillName – $today")
    $out.Add('')
    $out.Add('Entwurf aus `tools/validate-skills.ps1 -RuleInventory`: Kandidaten, kein vollständiges Regelverständnis. Nach')
    $out.Add('Urteil ergänzen und zusammenfassen, dann je Zeile Zustand, Neu-Ort und Prüfung eintragen')
    $out.Add('(`skills/skill-pflege/references/rule-inventory.md`).')
    $out.Add('')
    $out.Add("- Skill: $skillName")
    $out.Add("- Stand: $commit ($today)")
    $out.Add("- Quellen: $($sources -join ', ')")
    $out.Add("- Kandidaten: $($candidates.Count)")
    $out.Add('')
    $out.Add('| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |')
    $out.Add('|---|---|---|---|---|---|---|---|')
    $n = 0
    foreach ($c in $candidates) {
        $n++
        $place = Format-RuleCore "$($c.Rel)#$($c.Heading) (Z. $($c.Line))"
        $out.Add(('| R{0:000} | {1} | {2} | | | | | |' -f $n, $place, (Format-RuleCore $c.Text)))
    }

    $dir = Split-Path -Parent $target
    if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    $out | Set-Content -LiteralPath $target -Encoding utf8
    Write-Host "Regel-Inventar: $($candidates.Count) Kandidaten aus $($sources.Count) Dateien → $target"
}

function Write-Report($Report) {
    $s = $Report.summary
    Write-Host "Skill-Prüfung: $($s.skills) Skills, $($s.errors) Fehler, $($s.warnings) Warnungen – $($Report.status)"
    foreach ($e in $Report.repo.errors) { Write-Host "  FEHLER  Repo: $e" }
    foreach ($w in $Report.repo.warnings) { Write-Host "  WARNUNG Repo: $w" }
    foreach ($r in $Report.skills) {
        Write-Host ("{0,-18} {1,4} Zeilen (Körper {2,4})  Description {3,4}  References {4,2}  Fehler {5}  Warnungen {6}" -f
            $r.name, $r.lines, $r.bodyLines, $r.descriptionLength, $r.references, $r.errors.Count, $r.warnings.Count)
        foreach ($e in $r.errors) { Write-Host "  FEHLER  $e" }
        foreach ($w in $r.warnings) { Write-Host "  WARNUNG $w" }
    }
}

try {
    if ($RuleInventory) {
        Export-RuleInventory
        exit 0
    }
    $report = Invoke-Validation
    Write-Report $report
    if ($JsonPath) {
        $target = if ([System.IO.Path]::IsPathRooted($JsonPath)) { $JsonPath } else { Join-Path (Get-Location) $JsonPath }
        $dir = Split-Path -Parent $target
        if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
        $report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $target -Encoding utf8
        Write-Host "JSON-Bericht: $target"
    }
    exit $(if ($report.summary.errors -eq 0) { 0 } else { 1 })
} catch {
    # Continue, sonst beendet ErrorActionPreference Stop das Skript mit Exit 1 vor dem exit 2
    Write-Error "Prüfskript gescheitert: $($_.Exception.Message)" -ErrorAction Continue
    exit 2
}
