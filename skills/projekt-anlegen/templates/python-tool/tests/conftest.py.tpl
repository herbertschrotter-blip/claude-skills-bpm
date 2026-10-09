import pytest


@pytest.fixture
def daten(tmp_path, monkeypatch):
    """Eigener Datenordner je Test – kein Test beeinflusst einen anderen."""
    monkeypatch.setenv("{{package_upper}}_DATEN", str(tmp_path))
    return tmp_path
