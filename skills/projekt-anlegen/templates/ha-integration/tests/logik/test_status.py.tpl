"""Fachlogik ohne Home Assistant: technischer Status."""

import pytest
from logik.status import BEREIT, QUELLE_FEHLT, status


@pytest.mark.parametrize("zustand", ["5", "on", "docked"])
def test_quelle_verfuegbar(zustand):
    assert status(zustand) == BEREIT


@pytest.mark.parametrize("zustand", [None, "", "unavailable", "unknown"])
def test_quelle_fehlt(zustand):
    assert status(zustand) == QUELLE_FEHLT
