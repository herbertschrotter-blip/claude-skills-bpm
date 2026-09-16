---
name: mockup-erstellen
description: >
  Erstellt UI-Mockups als HTML-Entwürfe für neue Screens, Dialoge und
  Layoutvarianten – nach dem Mockup-Profil des Projekts (BPM: Docs/Mockups mit
  Sitemap; Heidi: dreame_x60/mockups im Bento-Design mit --dx-Tokens). Use when users want to mocken, entwerfen, skizzieren,
  zeigen, visualisieren, layouten, or want to clarify how a screen should
  look before coding — including mockups, screen designs, UI proposals,
  layout drafts, dialog sketches, and tab/panel arrangements. For
  sequential intents like "mock and then implement": triggers as the first
  step (mockup), then defers to code-erstellen. Do not trigger for direct
  XAML or Lit component implementation, small UI fixes in existing code, or
  non-UI design topics like database design.
---

# Mockup-Erstellen — UI-Entwürfe als HTML

## Zweck

Erstellt HTML-Mockups für die Screens des aktiven Projekts. Stellt sicher dass:
- Die Namenskonvention und Ablage des Projekts eingehalten wird (Mockup-Profil)
- Die richtigen Docs und Design-Tokens des Projekts geladen werden
- Der Workflow (Preview → Bestätigung → Speichern → Abnahme festhalten) befolgt wird
- Bestehende Mockups nicht überschrieben werden
- Der Stil konsistent über alle Screens bleibt (Token-Abgleich mit der Design-Quelle)

Was projektspezifisch ist, steht im **Mockup-Profil** (Abschnitt „Voraussetzung: Mockup-Profil“).
BPM: `Docs/Mockups/<Modul>/NN_Fenster/`, Sitemap, Klick-Navigation, Tokens aus Colors.xaml.
Heidi: `dreame_x60/mockups/*.html`, alle Seiten in einer Datei mit Tabs, Tokens `--dx-*` aus
`tokens.ts`, Referenz `bento.html`, Abnahme im Bauplan.

---

## Vorrang / Delegation an andere Skills

**mockup-erstellen ist für UI-Entwürfe als HTML-Mockup. Wenn die Hauptabsicht
echte Code-Implementierung ist, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| View/Komponente schreiben oder ändern (XAML, Lit-Komponente, Dialog) | **code-erstellen** |
| ViewModel, Commands, Bindings, Selektoren implementieren | **code-erstellen** |
| Kleiner UI-Fix in bestehendem Code (Farbe, Größe, Binding) | **code-erstellen** |
| Code-Struktur oder Logik der UI | **code-erstellen** |

Nur wenn die Hauptabsicht **ein neuer UI-Entwurf als HTML-Mockup** ist
(Screen-Vorschlag, Layout-Klärung vor dem Code, Dialog-Skizze),
bleibt mockup-erstellen zuständig.

**Wichtig:** Mockup-erstellen liefert HTML in die Mockup-Ablage des Profils. Sobald es um
echten Code (XAML/C#, TypeScript/Lit) geht, gehört die Arbeit in code-erstellen. Umgekehrt
ruft code-erstellen diesen Skill über den **Mockup-Hook** (Deep + UI + Profil „Mockup-Pflicht: ja“)
auf und wartet auf die festgehaltene Abnahme (Kapitel 3, Schritt 4b).

---

## 🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage
gestellt werden — KEINE Prosa-Fragen.** Auswahlfrage = Frage-Werkzeug der Umgebung
mit anklickbaren Optionen (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`).

### Diese Fragen IMMER als Auswahlfrage:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (nur wenn die Shell ihn nicht liefert) | Branch-Namen aus `git branch -a` |
| Token-Abgleich zeigt Abweichungen | Mockup an Tokens anpassen, Tokens-Datei ändern (→ code-erstellen), Abweichung begründet lassen |
| Pflichtansicht fehlt (Profil „Ansichten“) | Ansicht ergänzen, Ohne speichern (Begründung), Abbrechen |
| Abnahme | Abgenommen, Änderungen nötig, Später |
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

Branch aus Chat-Kontext verwenden. Mit Shell (Claude Code: Bash/PowerShell, Cowork: DC):
`git branch --show-current`; Pflicht-Branch aus dem Code-Profil beachten. Ohne Shell und
unbekannt: Auswahlfrage. NIE automatisch einen Branch annehmen.

---

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`).
Cowork: für Schreiboperationen Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

---

## Voraussetzung: Mockup-Profil

Abschnitt `## Mockup-Profil` in der `CLAUDE.md` des Repos (Claude Code liest sie automatisch;
Cowork per DC). Felder:

| Feld | Bedeutung | BPM | Heidi |
|------|-----------|-----|-------|
| Ablage | Ordner für Mockups | `Docs/Mockups/<Modul>/NN_Fenster/` | `dreame_x60/mockups/` (flach) |
| Namensschema | Datei- und Ordnernamen | `NN_Fenster/NN_Variante.html` (Kapitel 1) | `<thema>.html`, klein, ohne Umlaute; ein Mockup = alle betroffenen Seiten mit Tabs |
| Design-Quelle | Datei mit den gültigen Tokens | `Colors.xaml`, `UI_UX_Guidelines.md`, `WPF_UI_Architecture.md`, `Icons.xaml` | `dreame_x60/card/src/styles/tokens.ts` (`--dx-*`), Designvorgabe „Automotive Dark Bento“ |
| Referenz-Mockup | Stilvorlage für neue Mockups | letztes Mockup im selben Modul | `dreame_x60/mockups/bento.html` |
| Token-Form im HTML | wie Tokens im Mockup stehen | Hex-Werte aus Colors.xaml | CSS-Variablen `--dx-*` mit denselben Werten wie tokens.ts (`:root`-Block) |
| Ansichten | Pflichtansichten je Mockup | Desktop | Desktop **und** 390 px (Smartphone) nebeneinander, Tablet wenn Container-Regeln betroffen |
| Sitemap / Klick-Navigation | Kapitel 1 und 5–8 anwenden? | ja | nein (Tabs in der Datei, keine Kanten) |
| Vorschau | wie der User das Mockup sieht | Visualizer (Cowork) | Claude Code: Browser-Bereich (Datei öffnen) oder Datei per SendUserFile; Cowork: Visualizer |
| Abnahme-Ort | wo die Abnahme festgehalten wird | `_SITEMAP.md` (Status ✅) | Bauplan Abschnitt 7 (Seitentabelle: „Abgenommen von Herbert am <Datum> (Mockup <Datei>)“) und Notiz in Abschnitt 10; Abweichung zu v1 → PD-Eintrag 10a |
| Commit-Modul | Modulname für den Commit | `Docs` | `Doku` |

**Fehlt das Profil:** BPM-Werte aus diesem Skill annehmen (Kapitel 1–8) – nur wenn das Repo
tatsächlich `Docs/Mockups/` hat; sonst Auswahlfrage „Profil anlegen (Vorschlag aus dem Repo)“.

---

## 1. NAMENSKONVENTION (VERBINDLICH bei Profil „Sitemap: ja“ – BPM)

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
Stattdessen werden die **Design-Quelle** und das **Referenz-Mockup** aus dem Profil gelesen
(Claude Code: Read; Cowork: DC `read_file` oder `github:get_file_contents`).

Heidi: `tokens.ts` komplett (alle `--dx-*`), `bento.html` Kopf (`:root`-Block, Layout-Regeln
Bento 12/6/1 Spalten, `dx-nav`-Formen), Bauplan Abschnitt 7 (Seitentabelle) und die
Aufgabenkarte des Schritts, für den das Mockup entsteht. Regel 14 des Bauplans: System-Schriftstapel,
keine externen Ressourcen – gilt auch im Mockup.

### Quickload-First-Pass (BPM)

Folgende Docs laden (Quickload reicht, kein Langform):

| Doc | Zweck | Laden via |
|-----|-------|-----------|
| **UI_UX_Guidelines.md** | Design-Token, Spacing, Komponenten | `github:get_file_contents` → `Docs/Referenz/UI_UX_Guidelines.md` |
| **WPF_UI_Architecture.md** | Token→WPF-Key Mapping, Dialog-Pattern | `github:get_file_contents` → `Docs/Referenz/WPF_UI_Architecture.md` |
| **Colors.xaml** | Aktuelle Farbwerte | `github:get_file_contents` → `src/BauProjektManager.App/Themes/Colors.xaml` |
| **Icons.xaml** | Verfügbare Icon-Keys | `github:get_file_contents` → `src/BauProjektManager.App/Themes/Icons.xaml` |

### Bestehende Mockups prüfen

Vor Erstellung eines neuen Mockups die Ablage des Profils listen:
```
Cowork:      list_directory → Docs/Mockups/<Modul>/
Claude Code: Glob → <Ablage>/*.html   (Heidi: dreame_x60/mockups/)
```
- Prüfe ob `NN_Fenster/`-Ordner schon existiert (dann ist es eine neue Variante, kein neues Fenster — siehe Kapitel 7)
- Bei Update einer bestehenden Mockup-Datei: Per Auswahlfrage fragen (Archivieren, Überschreiben, Abbrechen).
  Heidi: abgelöste Mockups bleiben liegen und werden im Bauplan als „abgelöst durch <Datei>“ vermerkt (wie `seiten.html` → `bento.html`)

### Sitemap laden (zusätzlich, ab 2026-05 – nur bei Profil „Sitemap: ja“)

Vor jedem neuen Mockup:
```
read_file → Docs/Mockups/<Modul>/_SITEMAP.md
```
- Bestehende Navigationskanten kennen (welche Fenster gibt es schon? wer ruft was auf?)
- Bei totem Pfad (`alert('Mockup folgt: X')`): prüfen ob X jetzt existiert → Cleanup (siehe Kapitel 6)

### Design-Referenz aus bestehenden Screens

Wenn ein neuer Screen im gleichen Modul/Stil wie ein bestehender sein soll:
- Bestehenden UI-Code laden (BPM: XAML via GitHub/DC; Heidi: Komponente `src/components/dx-*.ts` + `styles/controls.ts`) als Stil-Referenz
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
- Design-Quelle und Referenz-Mockup des Profils (Kapitel 2); BPM zusätzlich Quickload-First-Pass, Colors.xaml
- `_SITEMAP.md` des betroffenen Moduls (nur BPM)
- Aufgabenquelle des Schritts (Heidi: Bauplan-Karte, Akzeptanz = was das Mockup zeigen muss)
- Memory prüfen auf Design-Entscheidungen (z.B. Karten-Design-Regeln; Heidi: Bauplan Abschnitt 10, PD-Register)

### Schritt 3 — Preview
- **Cowork:** Mockup als **Visualizer** (show_widget) im Chat anzeigen
- **Claude Code:** Datei in die Ablage schreiben (Schritt 4 ist hier dieselbe Datei) und im
  **Browser-Bereich** öffnen (`file://`-Pfad bzw. `preview_start`), Screenshot prüfen, zusätzlich
  per `SendUserFile` (render) an den User; Ansichten aus dem Profil im Browser nachstellen
  (`resize_window` 390 px)
- User bestätigt oder gibt Änderungswünsche
- Iterieren bis User zufrieden ist

### Schritt 3b — Token-Abgleich (Pflicht vor dem Speichern)
- Alle Token-Werte im Mockup (`:root`-Block bzw. Hex-Werte) gegen die **Design-Quelle** des Profils
  vergleichen (Heidi: `tokens.ts`; BPM: Colors.xaml)
- Abweichungen als Liste (Token, Mockup-Wert, Quell-Wert) → Auswahlfrage: Mockup anpassen /
  Tokens-Datei ändern (Aufgabe für code-erstellen) / begründet lassen (Begründung ins Mockup als Kommentar)
- Neue Tokens, die es in der Quelle nicht gibt, gelten als Abweichung
- Mockup darf keine Werte enthalten, die später „aus Versehen“ Karten-Standard werden

### Schritt 3c — Ansichten prüfen (Profil „Ansichten“)
- Jede Pflichtansicht ist im Mockup vorhanden (Heidi: Desktop + 390 px; Tablet bei Container-Regeln)
- Fehlt eine → Auswahlfrage: ergänzen / ohne speichern (Begründung) / abbrechen

### Schritt 4 — Auf Platte speichern
- Erst nach User-Bestätigung
- **Claude Code:** Write in die Ablage des Profils (Repo-Wurzel + Ablage); kein zusätzlicher Trigger nötig
- **Cowork:** via DC `write_file` in `<workFolder>/<Ablage>/…`; User muss DC explizit triggern ("dc", "cc", "auf platte", "speichern")
- Dateiname nach Namensschema des Profils (BPM: Kapitel 1)
- Nur bei Profil „Sitemap: ja“: Sitemap aktualisieren (Kapitel 6), Aufrufer-HTMLs patchen (Kapitel 5 + 7), tote Pfade scannen (Kapitel 7)

### Schritt 4b — Abnahme festhalten (Pflicht, sobald der User abnimmt)
- Auswahlfrage „Abgenommen / Änderungen nötig / Später“ – erst nach der Vorschau der finalen Datei
- Bei „Abgenommen“ an den **Abnahme-Ort des Profils** schreiben: Datum, Datei, Umfang (welche Seiten/Zustände),
  bewusst weggelassene Extras. Heidi: Bauplan Abschnitt 7 (Zeile der Seite: „Abgenommen von Herbert am <Datum>
  (Mockup <Datei>)“) + Notiz in Abschnitt 10 (Art `Befund · Info`); Abweichung zum bisherigen Verhalten →
  PD-Eintrag 10a mit Status `freigegeben`. BPM: Sitemap-Status ✅.
- Ohne festgehaltene Abnahme gilt das Mockup für code-erstellen (Mockup-Hook) als **nicht** abgenommen.
- Bei „Später“: Hinweis, dass der Bau des Schritts blockiert bleibt.

### Schritt 5 — Commit-Vorschlag
- Format: `[vX.Y.Z] <Commit-Modul des Profils>, Docs: Mockup <Datei> – <Kurztitel>` (BPM: `Docs`, Heidi: `Doku`)
- Version: Bump-Regel des Commit-Profils (BPM: PATCH; Heidi: reine Doku-Commits behalten die Kartenversion)
- Abnahme-Eintrag (Schritt 4b) im selben Commit
- Falls Sitemap mitgeändert oder Aufrufer-Mockups gepatcht: in Commit-Message erwähnen

---

## 4. HTML-REGELN FÜR MOCKUPS

### Standalone-fähig
- Mockup-HTML muss im Browser allein öffenbar sein
- Eigenes `<style>` Block mit den Tokens der Design-Quelle des Profils (geladen, nicht im Skill gespeichert)
- Kein Framework, keine externen Dependencies (keine Web-Fonts, keine CDN-Skripte – Heidi Regel 14)

### Tokens in der Form des Profils, keine Visualizer-Variablen
- Der Visualizer (Cowork) nutzt eigene CSS-Variablen (--color-background-primary etc.) – die dürfen nie ins gespeicherte Mockup
- BPM: Tokens als Hex-Werte aus Colors.xaml
- Heidi: Tokens als CSS-Variablen `--dx-*` in einem `:root`-Block mit **denselben Werten wie tokens.ts** (Token-Abgleich, Schritt 3b); Komponenten-Klassen wie in `bento.html`
- Werte aus der Design-Quelle laden, nicht hardcoden im Skill

### Struktur
```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title><Projekt> <Modul/Seite> — <Blatt></title>
<style>
/* Tokens aus der Design-Quelle des Profils (BPM: Colors.xaml als Hex; Heidi: :root { --dx-* } wie tokens.ts) */
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
- **Klick-Navigation zwischen Mockups: PFLICHT bei Profil „Sitemap: ja“** — siehe Kapitel 5; Heidi: Tabs innerhalb der Datei, Zustände (Leerlauf/Lauf/Fehler) als umschaltbare Varianten
- Keine komplexe Logik — es ist ein Mockup, kein Prototyp

---

## 5. INTERAKTIVITÄT & KLICK-NAVIGATION (PFLICHT bei Profil „Sitemap: ja“, ab 2026-05)

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

## 6. SITEMAP & SELBSTCHECK (ab 2026-05, nur bei Profil „Sitemap: ja“)

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

## 7. WORKFLOW: NEUES FENSTER ANLEGEN (A+B kombiniert, nur bei Profil „Sitemap: ja“)

Wenn ein komplett neues Fenster (Screen, Wizard, Dialog) angelegt wird, läuft der
Skill folgenden Sub-Workflow ab:

### Schritt 1 — User fragen (B-Mechanik)

Per Auswahlfrage oder Prosa (bei freiem Text-Input):

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

## 8. WORKFLOW: NACHTRÄGLICH FENSTER HINZUFÜGEN (nur bei Profil „Sitemap: ja“)

Wenn ein Fenster nachträglich (nach mehreren bereits gebauten Mockups) hinzugefügt
wird, gilt der gleiche Workflow wie Kapitel 7, plus:

### Zusatz-Schritt — Bidirektionalität prüfen

Beim nachträglichen Einfügen verändern sich oft auch **bestehende Navigationsflüsse**:

- Bestehendes Fenster A ruft jetzt zusätzlich das neue Fenster N auf
- Bestehendes Fenster B verlinkt evtl. auf N statt auf altes Fenster C
- Sitemap-Reorganisation möglich (NN-Vergabe)

**Aktion:** Per Auswahlfrage fragen ob bestehende Flüsse angepasst werden müssen.

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
- Mockup auf Platte schreiben ohne expliziten DC-Trigger vom User (Cowork)
- NN-Nummer doppelt vergeben (BPM)
- Umlaute oder Leerzeichen in Dateinamen oder Ordnernamen
- Mockup im Visualizer anzeigen und direkt das Visualizer-HTML speichern
  (Visualizer nutzt andere CSS-Variablen als das Projekt)
- Branch automatisch annehmen (Shell fragen oder Auswahlfrage)
- Archiv-vs-Überschreiben-Entscheidung als Prosa — IMMER Auswahlfrage
- **Speichern ohne Token-Abgleich** gegen die Design-Quelle (Schritt 3b) oder mit Tokens, die es dort nicht gibt
- **Speichern ohne die Pflichtansichten des Profils** (Heidi: Desktop + 390 px) ohne Auswahlfrage
- **Abnahme nur im Chat** – ohne Eintrag am Abnahme-Ort gilt das Mockup als nicht abgenommen (Schritt 4b)
- **BPM-Ablage oder -Namensschema für ein anderes Projekt annehmen** – alles aus dem Mockup-Profil
- **Externe Ressourcen im Mockup** (Web-Fonts, CDN), wenn das Projekt sie verbietet
- Prosa-Fragen bei festen Entscheidungsoptionen
- **Mockup ohne Klick-Navigation auf interaktive Elemente speichern** (Profil „Sitemap: ja“) — alle Buttons/Tabs/Karten brauchen `onclick` (Kapitel 5)
- **Sitemap-Update vergessen nach Mockup-Erstellung** (Profil „Sitemap: ja“) — `_SITEMAP.md` ist Single Source of Truth (Kapitel 6)
- **Tote Pfade nicht prüfen vor Mockup-Erstellung** — `alert('Mockup folgt: X')` muss ersetzt werden wenn X jetzt existiert
- **Aufrufer-HTMLs nicht patchen** beim Anlegen eines neuen Fensters — Workflow Kapitel 7 Schritt 2 ist Pflicht
- **Pfade in onclick ohne Selbstcheck speichern** — Datei-Existenz und Sitemap-Konsistenz prüfen (Kapitel 6)
