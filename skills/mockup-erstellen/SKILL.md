---
name: mockup-erstellen
description: >
  Erstellt BPM-UI-Mockups als HTML-Entwürfe für neue Screens, Dialoge und
  Layoutvarianten. Use when users want to mocken, entwerfen, skizzieren,
  zeigen, visualisieren, layouten, or want to clarify how a screen should
  look before coding — including mockups, screen designs, UI proposals,
  layout drafts, dialog sketches, and tab/panel arrangements. For
  sequential intents like "mock and then implement": triggers as the first
  step (mockup), then defers to code-erstellen. Do not trigger for direct
  XAML implementation, small UI fixes in existing code, or non-UI design
  topics like database design.
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

## Vorrang / Delegation an andere Skills

**mockup-erstellen ist für UI-Entwürfe als HTML-Mockup. Wenn die Hauptabsicht
echte Code-Implementierung ist, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| XAML-Datei schreiben oder ändern (View, UserControl, Dialog) | **code-erstellen** |
| ViewModel, Commands, Bindings implementieren | **code-erstellen** |
| Kleiner UI-Fix in bestehendem Code (Farbe, Größe, Binding) | **code-erstellen** |
| Code-Struktur oder Logik der UI | **code-erstellen** |

Nur wenn die Hauptabsicht **ein neuer UI-Entwurf als HTML-Mockup** ist
(Screen-Vorschlag, Layout-Klärung vor dem Code, Dialog-Skizze),
bleibt mockup-erstellen zuständig.

**Wichtig:** Mockup-erstellen liefert HTML für `Docs/Mockups/`. Sobald es um
echten XAML-Code oder C# geht, gehört die Arbeit in code-erstellen.

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
| Fenster-Ordner existiert bereits (neue Variante) | Variante hinzufügen, Bestehende ersetzen, Abbrechen |
| Eingehende Links unklar beim neuen Fenster | Liste vorhandener Fenster aus Sitemap als Optionen + "Keine eingehenden Links" |

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

### Ordnerstruktur (ab 2026-05)

Jedes Fenster (Screen, Wizard, Dialog) bekommt **einen eigenen Ordner**. Mockup-Dateien
liegen innerhalb dieses Ordners. Damit lassen sich Wizard-Schritte, Tab-Varianten und
Design-Varianten sauber gruppieren.

```
Docs/Mockups/
├── <Modul>/
│   ├── _SITEMAP.md                       ← Navigationskanten (siehe Kapitel 6)
│   ├── NN_Fenster/
│   │   ├── NN_Variante.html
│   │   └── ...
│   ├── NN_NaechstesFenster/
│   │   └── ...
│   └── _Archiv/
│       └── ...
└── ...
```

### Schema

```
<Modul>/NN_Fenster/NN_Variante.html
```

| Teil | Beschreibung | Beispiel |
|------|-------------|----------|
| **Modul** | Modulname aus der App | PlanManager, Settings |
| **NN_Fenster** | Ordner pro Fenster, NN = Navigationstiefe (2-stellig) | 01_Projektuebersicht, 04_ProfilWizard |
| **NN_Variante** | Datei innerhalb des Fenster-Ordners. NN = Reihenfolge bei Mehrfach-Files | 01_Hauptansicht, 01_Datei, 05_Erkennung |

### NN-Vergabe für Fenster-Ordner

- **01** — Hauptseite des Moduls (z.B. Projektübersicht)
- **02** — Detail-/Unterseite (z.B. Projektdetail)
- **03+** — weitere Screens, Dialoge, Wizards in der Reihenfolge des Auftretens

### NN-Vergabe für Dateien innerhalb eines Fenster-Ordners

- **Single-Screen-Fenster:** eine Datei, z.B. `01_Hauptansicht.html` oder `01_<Fenstername>.html`
- **Tab-Ansichten:** eine Datei pro Tab, NN entspricht Tab-Reihenfolge
- **Wizard-Schritte:** eine Datei pro Schritt, NN = Schritt-Nummer
- **Design-Varianten während Klärungsphase:** `01_Variante_Kompakt.html`, `01_Variante_Breit.html` — nach Auswahl gelöscht (Memory-Regel: Mockup-Varianten aufräumen)

### Modul-Ordner

Ordnername = Modulname aus der App:
- `PlanManager`
- `Settings` (oder `Einstellungen`, je nach App-Namen)
- `Foto` (wenn Modul gebaut wird)
- `Zeiterfassung` (wenn Modul gebaut wird)
- `Bautagebuch` (wenn Modul gebaut wird)

### Beispiele

```
PlanManager/01_Projektuebersicht/01_Projektuebersicht.html
PlanManager/02_Projektdetail/01_Profile.html
PlanManager/02_Projektdetail/02_ManuellSortieren.html
PlanManager/02_Projektdetail/03_Sync.html
PlanManager/03_ImportVorschau/01_ImportVorschau.html
PlanManager/04_ProfilWizard/01_Datei.html
PlanManager/04_ProfilWizard/02_Segmente.html
PlanManager/04_ProfilWizard/03_Index.html
PlanManager/04_ProfilWizard/04_Zielordner.html
PlanManager/04_ProfilWizard/05_Erkennung.html
PlanManager/_Archiv/00_Gesamtuebersicht.html
Settings/01_Allgemein/01_Allgemein.html
Settings/02_DevTools/01_Log.html
Settings/02_DevTools/02_Reset.html
```

### Sonderregeln

- Keine Umlaute in Ordner- und Dateinamen (ue statt ü, ae statt ä)
- Keine Leerzeichen (Underscore als Trenner)
- Archiv-Ordner: `_Archiv/` mit Unterstrich-Prefix → sortiert ans Ende
- Bestehende einzelne Mockup-Dateien (Legacy-Stand vor 2026-05) werden bei Bedarf in passenden Fenster-Ordner verschoben

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
- Prüfe ob `NN_Fenster/`-Ordner schon existiert (dann ist es eine neue Variante, kein neues Fenster — siehe Kapitel 7)
- Bei Update einer bestehenden Mockup-Datei: Per ask_user_input_v0 fragen (Archivieren, Überschreiben, Abbrechen)

### Sitemap laden (zusätzlich, ab 2026-05)

Vor jedem neuen Mockup:
```
read_file → Docs/Mockups/<Modul>/_SITEMAP.md
```
- Bestehende Navigationskanten kennen (welche Fenster gibt es schon? wer ruft was auf?)
- Bei totem Pfad (`alert('Mockup folgt: X')`): prüfen ob X jetzt existiert → Cleanup (siehe Kapitel 6)

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
- `_SITEMAP.md` des betroffenen Moduls
- Memory prüfen auf Design-Entscheidungen (z.B. Karten-Design-Regeln)

### Schritt 3 — Preview im Chat
- Mockup als **Visualizer** (show_widget) im Chat anzeigen
- User bestätigt oder gibt Änderungswünsche
- Iterieren bis User zufrieden ist

### Schritt 4 — Auf Platte speichern
- Erst nach User-Bestätigung
- Via DC `write_file` in `<workFolder>/Docs/Mockups/<Modul>/<NN_Fenster>/`
- Dateiname nach Namenskonvention (Kapitel 1)
- User muss DC explizit triggern ("dc", "cc", "auf platte", "speichern")
- Sitemap (`_SITEMAP.md`) im selben Schritt aktualisieren (Kapitel 6)
- Aufrufer-HTMLs patchen mit `onclick`-Verweisen (Kapitel 5 + 7)
- Tote Pfade nach diesem Mockup scannen und ersetzen (Kapitel 7)

### Schritt 5 — Commit-Vorschlag
- Format: `[vX.Y.Z] Docs, Docs: Mockup <Modul>/<NN_Fenster>/<Dateiname>`
- Version: PATCH-Bump
- Falls Sitemap mitgeändert: in Commit-Message erwähnen
- Falls Aufrufer-Mockups gepatcht: in Commit-Message erwähnen

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
- **Klick-Navigation zwischen Mockups: PFLICHT** — siehe Kapitel 5
- Keine komplexe Logik — es ist ein Mockup, kein Prototyp

---

## 5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT, ab 2026-05)

Alle Mockups werden als **durchklickbarer Prototyp** ausgelegt. Buttons, Tabs, Karten,
Sidebar-Einträge, Wizard-Weiter/Zurück: alles bekommt ein Klick-Ziel.

### Klickbare Elemente

Jedes interaktive Element bekommt:
```html
onclick="location.href='<relativer_pfad>'"
```

Plus visueller Hinweis auf Klickbarkeit (mindestens `cursor:pointer`, idealerweise Hover-Effekt).

### Relative Pfade

Pfade beziehen sich auf den Ordner des aktuellen Mockups:

```
gleicher Fenster-Ordner:     ./<NN_Variante>.html         (z.B. Wizard-Schritt → nächster Schritt)
Geschwister-Fenster:         ../<NN_Fenster>/<datei>.html  (z.B. Projektübersicht → Projektdetail)
Anderes Modul:               ../../<Modul>/<NN_Fenster>/<datei>.html  (z.B. Sidebar Settings)
```

### Tote Pfade (Ziel-Mockup existiert noch nicht)

Wenn das Ziel-Mockup geplant aber noch nicht gebaut ist:

```html
onclick="alert('Mockup folgt: <Fenstername>')"
style="border: 1px dashed #858585; opacity: 0.7;"
```

Plus visueller Hinweis (gestrichelter Rand, reduzierte Deckkraft) — damit User beim
Durchklicken sieht: hier ist Klickbarkeit geplant, aber Ziel fehlt noch.

Tote Pfade werden in der Sitemap mit Status `🟡 tot` markiert (Kapitel 6).

### Navigation-Verhalten

- **Gleicher Tab** (Default — natürliche App-Navigation, Browser-Zurück funktioniert)
- Kein `target="_blank"` — Mockups simulieren echte App-Navigation, nicht externe Links
- Sidebar/Modulleisten verlinken zwischen Modul-Ordnern

### Beispiele

**Projektübersicht-Karte klickt zur Detail-Ansicht:**
```html
<div class="projekt-karte" onclick="location.href='../02_Projektdetail/01_Profile.html'">
  ...
</div>
```

**Wizard "Weiter →"-Button:**
```html
<button onclick="location.href='./02_Segmente.html'">Weiter →</button>
```

**Sidebar Settings-Eintrag aus PlanManager-Modul:**
```html
<div onclick="location.href='../../Settings/01_Allgemein/01_Allgemein.html'">⚙ Einstellungen</div>
```

**Toter Pfad (Mockup noch nicht da):**
```html
<button onclick="alert('Mockup folgt: ImportVorschau')"
        style="border:1px dashed #858585;opacity:0.7;">Import starten</button>
```

---

## 6. SITEMAP & SELBSTCHECK (ab 2026-05)

### `_SITEMAP.md` pro Modul-Ordner

Zentrale Wahrheit für Navigationskanten. Wird bei jedem neuen Mockup gelesen und
nach Mockup-Erstellung aktualisiert.

**Speicherort:** `Docs/Mockups/<Modul>/_SITEMAP.md`

### Format

```markdown
# <Modul> — Sitemap

## Fenster

| Ordner | Status | Datei(en) |
|---|---|---|
| 01_Projektuebersicht | ✅ aktiv | 01_Projektuebersicht.html |
| 02_Projektdetail | ✅ aktiv | 01_Profile.html, 02_ManuellSortieren.html, 03_Sync.html |
| 04_ProfilWizard | 🟡 in Arbeit | 05_Erkennung.html (1-4 fehlen) |

## Navigationskanten

| Quelle | Ziel | Trigger | Status |
|---|---|---|---|
| 01_Projektuebersicht/01_Projektuebersicht.html | 02_Projektdetail/01_Profile.html | Projekt-Karte (Klick) | ✅ |
| 02_Projektdetail/01_Profile.html | 01_Projektuebersicht/01_Projektuebersicht.html | Zurück-Pfeil (←) | ✅ |
| 02_Projektdetail/01_Profile.html | 04_ProfilWizard/01_Datei.html | "+ Neuen Dokumenttyp" | 🟡 tot |
| 02_Projektdetail/01_Profile.html | 04_ProfilWizard/01_Datei.html | "✎ Profil" pro Profil | 🟡 tot |
| 04_ProfilWizard/01_Datei.html | 04_ProfilWizard/02_Segmente.html | "Weiter →" | 🟡 tot |
```

### Status-Symbole

- **✅ aktiv** — beide Mockups existieren, Klick-Navigation funktioniert
- **🟡 tot** — Ziel-Mockup fehlt noch, Aufrufer hat `alert('Mockup folgt: X')`
- **❌ kaputt** — Pfad-Inkonsistenz (z.B. Datei verschoben, Link nicht angepasst)

### Pflege-Pflicht

- **Vor jedem neuen Mockup:** Sitemap lesen
- **Nach jedem neuen Mockup:** Sitemap aktualisieren (neue Kanten ergänzen, tote → aktiv wenn Ziel jetzt da)
- **Bei Umbenennung/Verschiebung:** alle Pfade in Sitemap UND in HTML-onclick-Refs anpassen
- **Bei Mockup-Löschung:** Sitemap-Einträge entfernen, eingehende Kanten auf `🟡 tot` setzen oder Aufrufer-Mockups patchen

### Selbstcheck

Vor Commit:

1. **Sitemap-Kanten vs HTML-onclick-Refs vergleichen**
   - Jede Kante in Sitemap muss als `onclick` im Quell-HTML existieren
   - Jeder `onclick` im HTML muss als Kante in der Sitemap stehen
2. **Datei-Existenz prüfen**
   - Jedes Ziel in `onclick="location.href='...'"` muss als Datei existieren
   - Falls nicht → Kante als `🟡 tot` markieren ODER `alert('Mockup folgt: X')` verwenden
3. **Diskrepanzen melden** statt stillschweigend zu korrigieren — User entscheidet

---

## 7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert)

Wenn ein komplett neues Fenster (Screen, Wizard, Dialog) angelegt wird, läuft der
Skill folgenden Sub-Workflow ab:

### Schritt 1 — User fragen (B-Mechanik)

Per `ask_user_input_v0` oder Prosa (bei freiem Text-Input):

- **Eingehende Links:** Aus welchen bestehenden Fenstern wird das neue aufgerufen?
  - Liste der vorhandenen Fenster aus Sitemap als Optionen
  - Plus "Keine eingehenden Links" (z.B. neues Hauptmenü)
- **Trigger im Aufrufer:** Welcher Button/Karte/Tab löst die Navigation aus?
  - Freier Text-Input (z.B. "Button 'Neuen Dokumenttyp anlernen'")
- **Ausgehende Links / Zurück-Verhalten:** Wohin kehrt das neue Fenster zurück?
  - Aufrufer (typisch bei Dialogen) | Hauptseite | Anderes Fenster | Nirgends (Standalone)
- **NN-Vergabe:** nächste freie Nummer, oder dazwischen-rücken (dann müssen nachfolgende renamed werden)

### Schritt 2 — Aufrufer-HTMLs patchen (B-Mechanik)

Für jede genannte Eingangs-Quelle:
1. HTML-Datei laden
2. Passende Klick-Stelle suchen (Button-Label, Karte mit bekanntem Text, Tab)
3. `onclick="location.href='<pfad_zum_neuen_fenster>'"` einfügen
4. Falls bisher `alert('Mockup folgt: X')` mit dem genauen Fenster-Namen drin war → ersetzen

### Schritt 3 — Neues Mockup erstellen

Standard-Workflow (Kapitel 3) für das neue Fenster:
- Stil-Referenz: bestehende Mockups im selben Modul
- Klick-Navigation: Zurück-Pfeil/Schließen-Button mit `onclick` zum angegebenen Rückkehr-Ziel
- Tote Pfade für noch nicht existente Folge-Mockups

### Schritt 4 — Sitemap aktualisieren (A-Persistenz)

`_SITEMAP.md` patchen:
- Neuen Fenster-Eintrag in "Fenster"-Tabelle
- Neue Kanten in "Navigationskanten"-Tabelle (eingehend + ausgehend)
- Status entsprechend: `✅` wenn beide Seiten existieren, `🟡 tot` wenn Ziel/Quelle fehlt

### Schritt 5 — Tote Pfade scannen

In allen HTML-Files des Moduls nach `alert('Mockup folgt: <neues_fenster>')` suchen:
- Wenn gefunden → durch echten `location.href`-Link ersetzen
- Sitemap-Status entsprechend von `🟡 tot` auf `✅` aktualisieren

### Schritt 6 — Selbstcheck

Kapitel 6 — Sitemap-Kanten vs HTML-onclick-Refs vergleichen, Datei-Existenz prüfen.

---

## 8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN

Wenn ein Fenster nachträglich (nach mehreren bereits gebauten Mockups) hinzugefügt
wird, gilt der gleiche Workflow wie Kapitel 7, plus:

### Zusatz-Schritt — Bidirektionalität prüfen

Beim nachträglichen Einfügen verändern sich oft auch **bestehende Navigationsflüsse**:

- Bestehendes Fenster A ruft jetzt zusätzlich das neue Fenster N auf
- Bestehendes Fenster B verlinkt evtl. auf N statt auf altes Fenster C
- Sitemap-Reorganisation möglich (NN-Vergabe)

**Aktion:** Per `ask_user_input_v0` fragen ob bestehende Flüsse angepasst werden müssen.

### NN-Reorganisation (Vorsicht)

Falls die NN-Vergabe geändert werden soll (z.B. neues Fenster zwischen alten 02 und 03
→ alle ab 03 hochrücken):

- ALLE Mockup-Ordner umbenennen
- ALLE relativen Pfade in allen `onclick="location.href='...'"` anpassen
- Sitemap komplett neu pflegen

Das ist aufwendig. **Default:** neue Nummer am Ende vergeben (z.B. 06_NeuesFenster),
auch wenn es thematisch zwischen 02 und 03 gehört. Sitemap stellt den logischen Fluss
ohnehin separat dar.

### Sitemap-Cleanup auch hier

Wie in Kapitel 7 Schritt 5: tote Pfade auf das neue Fenster scannen und ersetzen,
Sitemap-Status nachziehen.

---

## VERBOTEN

- Farbwerte, Spacing-Werte, Token-Namen im Skill hardcoden
- Mockup erstellen ohne Docs zu laden
- Mockup auf Platte schreiben ohne User-Bestätigung im Chat
- Mockup auf Platte schreiben ohne expliziten DC-Trigger vom User
- NN-Nummer doppelt vergeben
- Umlaute oder Leerzeichen in Dateinamen oder Ordnernamen
- Mockup im Visualizer anzeigen und direkt das Visualizer-HTML speichern
  (Visualizer nutzt andere CSS-Variablen als BPM)
- Branch automatisch annehmen ohne ask_user_input_v0
- Archiv-vs-Überschreiben-Entscheidung als Prosa — IMMER ask_user_input_v0
- Prosa-Fragen bei festen Entscheidungsoptionen
- **Mockup ohne Klick-Navigation auf interaktive Elemente speichern** — alle Buttons/Tabs/Karten brauchen `onclick` (Kapitel 5)
- **Sitemap-Update vergessen nach Mockup-Erstellung** — `_SITEMAP.md` ist Single Source of Truth (Kapitel 6)
- **Tote Pfade nicht prüfen vor Mockup-Erstellung** — `alert('Mockup folgt: X')` muss ersetzt werden wenn X jetzt existiert
- **Aufrufer-HTMLs nicht patchen** beim Anlegen eines neuen Fensters — Workflow Kapitel 7 Schritt 2 ist Pflicht
- **Pfade in onclick ohne Selbstcheck speichern** — Datei-Existenz und Sitemap-Konsistenz prüfen (Kapitel 6)
