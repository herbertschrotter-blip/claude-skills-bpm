import sqlite3

import pytest

from {{package}}.config import laden
from {{package}}.speicher import (
    SCHEMA_VERSION,
    SchemaFehler,
    speicher_fuer,
)


def test_status_aus_der_datenbank(daten):
    assert speicher_fuer(laden()).status_lesen() == "ready"
    con = sqlite3.connect(daten / "{{package}}.db")
    try:
        assert con.execute("SELECT version FROM schema_meta").fetchone()[0] == SCHEMA_VERSION
    finally:
        con.close()


def test_zweiter_start_mit_derselben_datenbank(daten):
    speicher_fuer(laden())
    assert speicher_fuer(laden()).status_lesen() == "ready"


def test_fremde_schema_version(daten):
    speicher_fuer(laden())
    con = sqlite3.connect(daten / "{{package}}.db")
    with con:
        con.execute("UPDATE schema_meta SET version = 99")
    con.close()
    with pytest.raises(SchemaFehler):
        speicher_fuer(laden())
