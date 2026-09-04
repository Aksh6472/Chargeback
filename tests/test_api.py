"""
Integration Tests for FastAPI API Gateway
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "Chargeback Evidence AI"

def test_list_cases():
    response = client.get("/api/cases")
    assert response.status_code == 200
    cases = response.json()
    assert isinstance(cases, list)

def test_auth_send_otp():
    response = client.post("/api/auth/phone-otp/send", json={"phone": "+91 9876543210"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "session_id" in data
