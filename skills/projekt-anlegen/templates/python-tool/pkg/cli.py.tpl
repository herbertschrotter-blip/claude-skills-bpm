"""Befehlszeile. Technischer Durchlauf: status → Dienst → Speicher."""

import argparse
import json
import logging
import sys

from .config import EinstellungsFehler, laden
from .service import StatusDienst
from .speicher import speicher_fuer

log = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="{{package}}",
        description="{{name}}",
    )
    parser.add_argument("befehl", choices=["status"])
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    try:
        einstellungen = laden()
    except EinstellungsFehler as exc:
        print(f"Fehler in den Einstellungen: {exc}", file=sys.stderr)
        return 2
    try:
        dienst = StatusDienst(speicher_fuer(einstellungen))
        ergebnis = dienst.ausfuehren()
    except Exception as exc:  # Grenze nach außen: Meldung statt Traceback
        log.debug("Fehler bei %s", args.befehl, exc_info=True)
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(ergebnis))
    return 0
