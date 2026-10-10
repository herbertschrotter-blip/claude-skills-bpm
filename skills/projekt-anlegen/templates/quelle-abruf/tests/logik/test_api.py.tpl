"""Beispiel-Verbindung ohne Home Assistant."""

import asyncio

import pytest
from api import Client, VerbindungFehler


def test_abruf_liefert_zustand():
    assert asyncio.run(Client("192.0.2.1").abrufen()) == {"zustand": "ok"}


def test_ohne_adresse_keine_verbindung():
    with pytest.raises(VerbindungFehler):
        asyncio.run(Client(" ").abrufen())
