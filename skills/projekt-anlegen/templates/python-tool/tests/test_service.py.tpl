from {{package}}.service import StatusDienst


class FesterSpeicher:
    def status_lesen(self) -> str:
        return "ready"


def test_dienst_liest_den_speicher():
    assert StatusDienst(FesterSpeicher()).ausfuehren() == {"status": "ready"}
