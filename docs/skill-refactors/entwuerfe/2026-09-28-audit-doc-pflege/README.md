# Entwürfe – Grenze audit ↔ doc-pflege (Umbau Phase 5), nicht freigegeben

Stand 28.09.2026 abends. Zielbild von Herbert freigegeben: **prüfen = audit, ändern = doc-pflege**; doc-pflege-Modi
bekommen Namen statt Nummern. Die Entwürfe hier sind noch **nicht** freigegeben und liegen deshalb nicht unter `skills/`
(Dateiname `SKILL.entwurf.md`, damit sie nicht als Skill geladen werden).

## Inhalt

| Datei | Ziel im Repo | Inhalt |
|---|---|---|
| `audit/SKILL.entwurf.md` | `skills/audit/SKILL.md` | neue Description (901 Zeichen), Zweck/Delegation, Profile laden mit Skill-Profil v1, Modul 6 über die neue Reference, neues Modul 7 „Skills (im Skill-Repo)“; 310 → 337 Zeilen |
| `audit/references/doku-validierung.md` | `skills/audit/references/doku-validierung.md` | Prüflisten aus doc-pflege Modus 6 und audit Modul 6 (MOVE); 65 Zeilen |
| `audit/inventory.md` | `docs/skill-refactors/2026-09-28-audit-2.md` | Regel-Inventar, keine DROP-Zeile |
| `doc-pflege/SKILL.entwurf.md` | `skills/doc-pflege/SKILL.md` | neue Description (980 Zeichen, ohne „validieren“), benannte Modi, Modus 3/4 in „Doku-Hinweise nach Code-Änderungen“, Modus 6 → audit, neu „Prüfen nach dem Schreiben“; 463 → 422 Zeilen |
| `doc-pflege/inventory.md` | `docs/skill-refactors/2026-09-28-doc-pflege-2.md` | Regel-Inventar (155 R-Zeilen, N001–N007), keine DROP-Zeile |
| `chat-wechsel/SKILL.entwurf.md` | `skills/chat-wechsel/SKILL.md` | Safe Patch: 7× „doc-pflege Modus 8“ → „doc-pflege, Sitzungsabschluss“ (auch in der Description, 542 Zeichen) |
| `chatgpt-review/SKILL.entwurf.md` | `skills/chatgpt-review/SKILL.md` | Safe Patch: „doc-pflege (Modus 7a/2)“ → „doc-pflege (Neue Doc, Begleit-Docs)“ |

Die Modusnamen: Projekt-Init · Router nachziehen · Begleit-Docs · Doku pflegen · Neue Doc oder Umbau (Neue Doc, Doc
umbauen) · Sitzungsabschluss; Modus 3/4 → Abschnitt „Doku-Hinweise nach Code-Änderungen“; Modus 6 → audit.

## Offene Fragen an Herbert (vor dem Schreiben)

1. Zielstrukturen audit und doc-pflege freigeben (Auswahlfrage je Skill).
2. `Doku.Validierungsregeln: none` – keine Prüfung oder Rückfall auf die Prüflisten in `doku-validierung.md`?
3. Im Skill-Repo zeigt `Doku.Validierungsregeln` auf `docs/skill-quality.md#skill-prüfung` – Modul 6 und das neue Modul 7
   prüfen dort dasselbe; Modul 6 im Skill-Repo auf Modul 7 verweisen lassen?
4. Die Kurzprüfungen in `doku-validierung.md` doppeln Stufe A/B – zusammenführen?
5. `Doku.Validierungsregeln` als Pflichtfeld von doc-pflege in `docs/skill-profile-v1.md` (wegen „Prüfen nach dem
   Schreiben“)?
6. doc-pflege, Grundsätze-Zeile „Doc-Pflege Modus bei doc-relevanter Änderung“ umbenennen?

## Danach (Reihenfolge)

1. Entwürfe an ihre Ziel-Orte kopieren (alle in einem Durchgang – ohne `doku-validierung.md` meldet das Prüfskript einen
   toten Verweis in doc-pflege), Inventare als `…-2.md` ablegen, diesen Ordner löschen.
2. INDEX: Zeilen audit und doc-pflege anpassen („validieren“ raus bei doc-pflege, „Skills prüfen“ bei audit),
   Konfliktpaar audit ↔ doc-pflege ergänzen.
3. Prüfskript, CHANGELOG `[v0.39.2]`, `docs/skillsystem-umbau.md` Phase 5 abhaken, Commits je Skill, Push.
4. Routing-Eval `--tag audit --tag doc-pflege --tag chat-wechsel` (Achtung `audit-bauplan`: „Bauplan check“ fällt aus der
   audit-Description); Ziel-Fall `audit-readonly` soll bestehen.
5. Lieferung einzeln: audit (Zip mit references), doc-pflege, chat-wechsel, chatgpt-review.
6. Echte Sitzungen: EXT-03 (audit ↔ code-review) und EXT-05 (cc-steuerung in Claude Code), Vergleichswert je 3/3.
