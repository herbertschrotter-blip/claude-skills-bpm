---
name: mockup-erstellen
description: >
  Erstellt BPM-UI-Mockups als HTML-Entwürfe für neue Screens, Dialoge und
  Layoutvarianten. Use when users want a mockup, a screen design, a UI proposal,
  a layout draft, or need to clarify how a screen should look before coding.
  Do not trigger for direct XAML implementation, small UI fixes in existing
  code, or non-UI design topics like architecture or database design.
---

# Mockup-Erstellen — UI-Entwürfe für BPM

## Zweck

Erstellt HTML-Mockups für BPM-Screens. Stellt sicher dass:
- Die Namenskonvention eingehalten wird
- Die richtigen Docs für Design-Infos geladen werden
- Der Workflow (Preview → Bestätigung → Speichern) befolgt wird
- Bestehende Mockups nicht überschrieben werden
- Der Stil konsistent über alle Screens bleibt

---

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (unbekannt) | Branch-Namen aus `git branch -a` |
| Bestehendes Mockup gefunden: Archiv vs. Überschreiben | Archivieren (_ARCHIV suffix), Überschreiben, Abbrechen |
| NN-Nummer belegt | Nächste freie Nummer, Andere Nummer wählen, Abbrechen |
| Mehrere Stil-Referenzen möglich | Referenz-Dateinamen als Optionen |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. "Welche Daten/Felder soll der Screen zeigen?")
- User hat Präferenz signalisiert
- Freitext-Input nötig

---

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden.
Wenn Branch in dieser Session noch nicht bekannt: Per ask_user_input_v0 fragen.
NIE automatisch einen Branch annehmen.

---

## Arbeitsverzeichnis (PFLICHT bei DC-Zugriff)

Für Schreiboperationen: Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

---

## 1. NAMENSKONVENTION (VERBINDLICH)

### Ordnerstruktur
```
Docs/Mockups/
├── <Modul>/
│   ├── NN_Blatt[_Untermenue].html
│   └── ...
└── ...
```

### Schema
```
NN_Blatt[_Untermenue].html
```

| Teil | Beschreibung | Beispiel |
|------|-------------|----------|
| **NN** | Navigationstiefe (2-stellig) | 01, 02, 03 |
| **Blatt** | Fenstername/Screen | Projektuebersicht, Projektdetail |
| **Untermenue** | Optional, bei Tabs/Bereichen | Profile, ManuellSortieren, Sync |

### NN-Nummern
- **00** — Archiv/Gesamtübersicht (veraltete Mockups)
- **01** — Hauptseite des Moduls
- **02** — Detail-/Unterseite
- **03+** — Dialoge, Wizards, Modals

### Modul-Ordner
Ordnername = Modulname aus der App:
- `PlanManager`
- `Einstellungen`
- `Foto` (wenn Modul gebaut wird)
- `Zeiterfassung` (wenn Modul gebaut wird)
- `Bautagebuch` (wenn Modul gebaut wird)

### Beispiele
```
PlanManager/01_Projektuebersicht.html
PlanManager/02_Projektdetail_Profile.html
PlanManager/02_Projektdetail_ManuellSortieren.html
PlanManager/02_Projektdetail_Sync.html
PlanManager/03_ImportVorschau.html
PlanManager/04_ProfilWizard.html
Einstellungen/01_Projekte.html
Einstellungen/02_StandardOrdnerstruktur.html
```

### Sonderregeln
- Keine Umlaute in Dateinamen (ue statt ü, ae statt ä)
- Keine Leerzeichen (Underscore als Trenner)
- Überholte Mockups: Suffix `_ARCHIV` → `00_Gesamtuebersicht_ARCHIV.html`

---

## 2. DOCS LADEN (PFLICHT vor Mockup-Erstellung)

Der Skill speichert KEINE Farbwerte, Spacing, Token-Namen.
Stattdessen werden die relevanten Docs gelesen.

### Quickload-First-Pass

Folgende Docs laden (Quickload reicht, kein Langform):

| Doc | Zweck | Laden via |
|-----|-------|-----------|
| **UI_UX_Guidelines.md** | Design-Token, Spacing, Komponenten | `github:get_file_contents` → `Docs/Referenz/UI_UX_Guidelines.md` |
| **WPF_UI_Architecture.md** | Token→WPF-Key Mapping, Dialog-Pattern | `github:get_file_contents` → `Docs/Referenz/WPF_UI_Architecture.md` |
| **Colors.xaml** | Aktuelle Farbwerte | `github:get_file_contents` → `src/BauProjektManager.App/Themes/Colors.xaml` |
| **Icons.xaml** | Verfügbare Icon-Keys | `github:get_file_contents` → `src/BauProjektManager.App/Themes/Icons.xaml` |

### Bestehende Mockups prüfen

Vor Erstellung eines neuen Mockups:
```
list_directory → Docs/Mockups/<Modul>/
```
- Prüfe ob NN-Nummer noch frei ist
- Prüfe ob ähnliches Mockup schon existiert
- Bei Update: altes Mockup mit `_ARCHIV` suffixen oder überschreiben (Per ask_user_input_v0 fragen: Archivieren, Überschreiben, Abbrechen)

### Design-Referenz aus bestehenden Screens

Wenn ein neuer Screen im gleichen Modul/Stil wie ein bestehender sein soll:
- Bestehenden XAML-Code laden (via GitHub oder DC) als Stil-Referenz
- ODER Screenshot vom User anfragen
- Ziel: Konsistenz über alle Screens

---

## 3. WORKFLOW (VERBINDLICH)

### Schritt 1 — Kontext sammeln
- Welches Modul? Welcher Screen?
- Gibt es schon ein Mockup das aktualisiert werden soll?
- Welche Daten/Felder soll der Screen zeigen?
- Gibt es einen bestehenden Screen als Stil-Referenz?

### Schritt 2 — Docs laden
- Quickload-First-Pass (siehe Kapitel 2)
- Colors.xaml für aktuelle Farbwerte
- Memory prüfen auf Design-Entscheidungen (z.B. Karten-Design-Regeln)

### Schritt 3 — Preview im Chat
- Mockup als **Visualizer** (show_widget) im Chat anzeigen
- User bestätigt oder gibt Änderungswünsche
- Iterieren bis User zufrieden ist

### Schritt 4 — Auf Platte speichern
- Erst nach User-Bestätigung
- Via DC `write_file` in `<workFolder>/Docs/Mockups/<Modul>/`
- Dateiname nach Namenskonvention (Kapitel 1)
- User muss DC explizit triggern ("dc", "cc", "auf platte", "speichern")

### Schritt 5 — Commit-Vorschlag
- Format: `[vX.Y.Z] Docs, Docs: Mockup <Modul>/<Dateiname>`
- Version: PATCH-Bump

---

## 4. HTML-REGELN FÜR MOCKUPS

### Standalone-fähig
- Mockup-HTML muss im Browser allein öffenbar sein
- Eigenes `<style>` Block mit BPM-Farben (aus Colors.xaml geladen, nicht im Skill gespeichert)
- Kein Framework, keine externen Dependencies

### Keine CSS-Variablen aus dem Visualizer
- Der Visualizer nutzt CSS-Variablen (--color-background-primary etc.)
- Mockup-HTML für Platte muss BPM-Tokens als Hex-Werte verwenden
- Werte aus Colors.xaml/UI_UX_Guidelines.md laden, nicht hardcoden im Skill

### Struktur
```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>BPM <Modul> — <Blatt></title>
<style>
/* BPM Dark Theme Tokens — aus Colors.xaml geladen */
</style>
</head>
<body>
<!-- Mockup Content -->
</body>
</html>
```

### Interaktivität
- Hover-Effekte über `onmouseover`/`onmouseout` erlaubt
- Tab-Wechsel via einfaches JS erlaubt
- Keine komplexe Logik — es ist ein Mockup, kein Prototyp

---

## 5. VERBOTEN

- Farbwerte, Spacing-Werte, Token-Namen im Skill hardcoden
- Mockup erstellen ohne Docs zu laden
- Mockup auf Platte schreiben ohne User-Bestätigung im Chat
- Mockup auf Platte schreiben ohne expliziten DC-Trigger vom User
- NN-Nummer doppelt vergeben
- Umlaute oder Leerzeichen in Dateinamen
- Mockup im Visualizer anzeigen und direkt das Visualizer-HTML speichern
  (Visualizer nutzt andere CSS-Variablen als BPM)
- Branch automatisch annehmen ohne ask_user_input_v0
- Archiv-vs-Überschreiben-Entscheidung als Prosa — IMMER ask_user_input_v0
- Prosa-Fragen bei festen Entscheidungsoptionen
