# Runde 2 – Entscheidungen Herbert (09.10.2026)

- Noch eine Runde vor der Umsetzung: Description-Entwurf und offene Details mit ChatGPT klären.

Von Claude ohne Rückfrage entschieden (technisch, siehe 03-claude-analysis.md): JSON-Auftrag v1 wie vorgeschlagen;
strukturierter Renderer für gemeinsame Dateien; Walking Skeleton „status“; zwei Phasen Prepare / Verify & Publish;
eigener Workflow für die Kombinationen; Regel für code-erstellen (Grundentscheidungen lesen); ci-github standardmäßig
bei GitHub-Repos; Herkunftsdatei im erzeugten Projekt; neue Abhängigkeitsversionen nur nach grünen Tests und Freigabe;
HA mit SQLite später über eigenen Adapter.
