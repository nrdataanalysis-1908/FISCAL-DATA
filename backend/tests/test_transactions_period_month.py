import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_transactions_reject_month_thirteen():
    response = client.get("/api/v1/transactions?period=2026-13")

    assert response.status_code == 422
