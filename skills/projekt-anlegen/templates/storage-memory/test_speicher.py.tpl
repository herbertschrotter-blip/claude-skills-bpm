from {{package}}.config import laden
from {{package}}.speicher import speicher_fuer


def test_status(daten):
    assert speicher_fuer(laden()).status_lesen() == "ready"
