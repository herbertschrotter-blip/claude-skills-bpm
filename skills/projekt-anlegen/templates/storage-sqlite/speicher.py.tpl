"""SQLite-Speicher mit Schema-Version.

Schema ändern: SCHEMA_VERSION erhöhen und den Übergang in `_einrichten` behandeln.
Ohne produktive Daten darf die Datenbank neu angelegt werden; mit produktiven Daten
braucht es eine ausdrückliche Entscheidung. Nie automatisch löschen.
"""

import sqlite3
from pathlib import Path

from .config import Einstellungen

SCHEMA_VERSION = 1


class SchemaFehler(RuntimeError):
    """Die Datenbank hat eine andere Schema-Version als der Code."""


class SqliteSpeicher:
    def __init__(self, datei: Path) -> None:
        self._datei = datei
        datei.parent.mkdir(parents=True, exist_ok=True)
        self._einrichten()

    def _einrichten(self) -> None:
        con = sqlite3.connect(self._datei)
        try:
            with con:
                con.execute("CREATE TABLE IF NOT EXISTS schema_meta (version INTEGER NOT NULL)")
                zeile = con.execute("SELECT version FROM schema_meta").fetchone()
                if zeile is None:
                    con.execute(
                        "CREATE TABLE system_status "
                        "(id INTEGER PRIMARY KEY CHECK (id = 1), state TEXT NOT NULL)"
                    )
                    con.execute("INSERT INTO system_status (id, state) VALUES (1, 'ready')")
                    con.execute("INSERT INTO schema_meta (version) VALUES (?)", (SCHEMA_VERSION,))
                elif zeile[0] != SCHEMA_VERSION:
                    raise SchemaFehler(
                        f"Datenbank {self._datei} hat Schema {zeile[0]}, erwartet {SCHEMA_VERSION}"
                    )
        finally:
            con.close()

    def status_lesen(self) -> str:
        con = sqlite3.connect(self._datei)
        try:
            return con.execute("SELECT state FROM system_status WHERE id = 1").fetchone()[0]
        finally:
            con.close()


def speicher_fuer(einstellungen: Einstellungen) -> SqliteSpeicher:
    return SqliteSpeicher(einstellungen.daten / "{{package}}.db")
