"""Tests gegen Home Assistant (pytest-homeassistant-custom-component).

Jeder Test bekommt ein eigenes Home Assistant; kein Test beeinflusst einen anderen.
"""

import pytest

pytest_plugins = ["pytest_homeassistant_custom_component"]


@pytest.fixture(autouse=True)
def eigene_integration(enable_custom_integrations):
    """Die Integration aus custom_components/ laden lassen."""
    return
