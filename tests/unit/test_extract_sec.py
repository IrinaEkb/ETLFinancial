import pytest

from src.extract.extract_sec import fetch_company_facts


class DummyResponse:
    def __init__(self):
        self.status_code = 200
        self.headers = {
            "Content-Type": "text/html; charset=utf-8"
        }
        self.text = "<html><body>blocked</body></html>"

    def json(self):
        raise ValueError("No JSON object could be decoded")


def test_fetch_company_facts_rejects_non_json_response(monkeypatch):

    def fake_get(*args, **kwargs):
        return DummyResponse()


    monkeypatch.setattr(
        "requests.get",
        fake_get
    )


    with pytest.raises(
        RuntimeError,
        match="Expected JSON"
    ):
        fetch_company_facts(
            "https://data.sec.gov/api/xbrl/companyfacts/CIK0000049079.json"
        )