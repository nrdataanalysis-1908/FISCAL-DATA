import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dre_rejects_month_zero():
    response = client.get("/api/v1/dre?period=2026-00")

    assert response.status_code == 422
