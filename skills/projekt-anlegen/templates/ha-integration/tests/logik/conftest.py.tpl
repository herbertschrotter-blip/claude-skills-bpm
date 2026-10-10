"""Die Fachlogik ohne Home Assistant importierbar machen."""

import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WURZEL / "custom_components" / "{{package}}"))
