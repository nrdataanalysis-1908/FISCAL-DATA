import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_tax_estimate_rejects_reference_month_thirteen():
    response = client.post(
        "/api/v1/tax/scenarios/estimate",
        json={
            "regime": "SIMPLES_NACIONAL",
            "taxable_base": "1000.00",
            "illustrative_rate_percent": "5.00",
            "reference_period": "2026-13",
            "scenario_name": "Cenário de teste",
        },
    )

    assert response.status_code == 422
