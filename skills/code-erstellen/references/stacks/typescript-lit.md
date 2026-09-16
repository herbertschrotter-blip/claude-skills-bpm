# Stack: typescript-lit — TypeScript strict + Lit 3 Web Components (Heidi-Karte)

Stack-Referenz für `code-erstellen`. Wird geladen, wenn das Code-Profil des Projekts
`Stacks: typescript-lit` enthält. Projektspezifisches (Pfade, Pflicht-Docs, Deploy) steht
im Code-Profil, nicht hier.

---

## Schichten und Kopplungsregeln

- **Vertrag** (`ha/contract.ts`): einzige Stelle für Entitäts-IDs, Dienste, Optionen. Neue Entität
  zuerst hier (und in der Vertrags-Doku des Projekts), dann weiter.
- **Erkennung/Profil** (`ha/device.ts`, `ha/profile.ts`): Gerätename, Räume, Optionen, Fähigkeiten
  aus HA lesen – nichts davon fest verdrahten.
- **Selektoren** (`ha/selectors.ts`, `memoizeSelector`): memoisierte Views aus `hass.states`;
  `ids` als Liste oder Funktion; eigener Vergleich nur wenn nötig. Komponenten lesen **nur** Views.
- **Schreiben** nur über die API-Klasse (`ha/api.ts`, `DxApi`): Dienstaufrufe, Teilfehler sammeln
  (`Promise.allSettled`), Ergebnis `{ok, fehlgeschlagen}`.
- **Komponenten** (`components/dx-*.ts`): Lit `render()` ohne Fachlogik; Fachlogik in `domain/*`
  als reine Funktionen mit Tests.
- **Shell** (`<name>-panel.ts`): erzeugt Views, reicht `hass`, Views, `api` nach unten; Overlay,
  Toast, Navigation; kein `shouldUpdate` in der Shell.
- Styles als Design-Tokens (`styles/tokens.ts`, `--dx-*`); keine Farben/Abstände hart in Komponenten.
- Keine externen Ressourcen (Fonts, CDN, Bilder) – alles im Bundle.

## Modus-Eskalation (Beispiele)

| Standard | Deep |
|----------|------|
| neue Funktion in Selector oder Komponente | neuer Vertragseintrag, neue API-Methode |
| neue Komponente / Dialog-Variante | neue Seite, neuer Benutzerfluss |
| neue Statuslogik in `domain/*` | Karte + Backend zusammen; Integration/WebSocket |
| mehrere Dateien in einer Schicht | Shell/Selektoren-Verdrahtung, Render-Verhalten |

## Impact-Check-Zeilen (Stack-Lesart)

- UI / Lit-Templates / Tokens `--dx-*`
- Selektoren / Views (memoisiert? `ids` vollständig?)
- Domäne (`domain/*`) / Vertrag (`contract.ts`)
- Backend-Entitäten betroffen (→ Stack home-assistant-yaml)
- Verdrahtung: Shell, `ALL_SELECTORS`, `define()`
- HA-Dienste / WebSocket (`callService`, `callWS`, `subscribeEvents`)
- Render-Verhalten bei irrelevanten `hass`-Ticks (0 Neuerzeugungen)
- Abzüge/Fixtures ohne Tokens und GPS

## Blocking: welche Doc/Datei zuerst

| Betroffen | Zuerst laden |
|-----------|--------------|
| neue Entität/Dienst | Vertrags-Doku + `contract.ts` |
| Verdrahtung | Shell + `selectors.ts` |
| UI-Umbau (Deep) | abgenommenes Mockup + `tokens.ts` |
| Domänenregel | Portierungstabelle / Regeln des Projekts |

## Tests

- **Unit:** `node --test` über `tsx`, Dateien `tests/unit/*.test.ts`; Vektoren als JSON
  (`*.v1.json` aus der Referenz, `*.spec.json` handgeschrieben)
- **E2E:** Playwright gegen Fixtures `tests/fixtures/states-*.json`, Harness mit Stubs für
  `callService`/`callApi`/`callWS`/`subscribeEvents`; jede Bedienung → erwarteter Call
- **Pflicht:** `npm run check` (tsc), `npm run lint` (eslint), `npm test` (check + unit + build + E2E), Exit-Code 0
- Je Akzeptanz-Zeile ein Test; Render-Zähler für „0 Neuerzeugungen bei irrelevanten Ticks“

## Typische Fehler

- IDs, Räume, Optionen oder Namen hart im Code statt aus Vertrag/Profil
- Komponente liest `hass.states` direkt statt über Selector
- Tipp-Handler mit eingefrorener Auswahl (Closure) statt aktuellem Zustand
- `hass.entities` als Änderungssignal (wechselt nicht bei Register-Updates → Ereignis abonnieren)
- Unused imports/vars → eslint rot; `any` in strict
- Version nur in einer Quelle hochgezählt (package.json **und** Lock **und** Ressourcen-`?v=`)
