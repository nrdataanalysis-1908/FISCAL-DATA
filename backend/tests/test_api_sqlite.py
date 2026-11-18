import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_reports_sqlite():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["database_engine"] == "SQLite"


def test_dashboard_summary_uses_demo_seed():
    response = client.get("/api/v1/dashboard/summary?period=2026-10")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_revenue"] == "150000.00"
    assert data["net_revenue"] == "132000.00"
    assert data["net_income"] == "32000.00"
    assert data["transaction_count"] == 12


def test_dre_is_marked_as_simulated():
    response = client.get("/api/v1/dre?period=2026-10")
    assert response.status_code == 200
    data = response.json()
    assert data["is_simulated"] is True
    assert data["net_margin_percent"] == "21.33"
