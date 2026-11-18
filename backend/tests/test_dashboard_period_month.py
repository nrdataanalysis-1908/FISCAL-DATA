import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_summary_rejects_month_thirteen():
    response = client.get("/api/v1/dashboard/summary?period=2026-13")

    assert response.status_code == 422
