from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.application import Application
from sqlalchemy.orm import Session
import pytest
from datetime import datetime


@pytest.fixture
def test_client(client):
    return TestClient(client)


def test_submit_application(test_client, test_db):
    # Test data
    application_data = {
        "applicant_name": "John Doe",
        "applicant_email": "john@example.com",
        "family_status": "new",
        "business_owner": True,
        "filed_us_taxes": True,
        "tax_year": 2023,
        "submitted_at": datetime.utcnow().isoformat()
    }

    # Make the request
    response = test_client.post("/api/applications", json=application_data)

    # Check response
    assert response.status_code == 200
    data = response.json()

    # Verify the response contains all the expected fields
    assert data["applicant_name"] == application_data["applicant_name"]
    assert data["applicant_email"] == application_data["applicant_email"]
    assert data["family_status"] == application_data["family_status"]
    assert data["business_owner"] == application_data["business_owner"]
    assert data["filed_us_taxes"] == application_data["filed_us_taxes"]
    assert data["tax_year"] == application_data["tax_year"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_submit_application_invalid_data(test_client):
    # Test with missing required field
    invalid_data = {
        "applicant_name": "John Doe",
        "family_status": "new",
        # Missing required fields
    }

    response = test_client.post("/api/applications", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_submit_application_invalid_family_status(test_client):
    # Test with invalid family status
    invalid_data = {
        "applicant_name": "John Doe",
        "applicant_email": "john@example.com",
        "family_status": "invalid_status",
        "business_owner": True,
        "filed_us_taxes": True,
        "tax_year": 2023,
        "submitted_at": datetime.utcnow().isoformat()
    }

    response = test_client.post("/api/applications", json=invalid_data)
    assert response.status_code == 422  # Validation error
    error_data = response.json()
    # Verify the error mentions family_status
    assert "family_status" in str(error_data)


def test_submit_application_with_rules(test_client, test_db):
    # Test data that should trigger a rule
    application_data = {
        "applicant_name": "Jane Smith",
        "applicant_email": "jane@example.com",
        "family_status": "returning",
        "business_owner": True,
        "filed_us_taxes": True,
        "tax_year": 2023,
        "submitted_at": datetime.utcnow().isoformat()
    }

    # Make the request
    response = test_client.post("/api/applications", json=application_data)

    # Check response
    assert response.status_code == 200
    data = response.json()

    # Verify the application was created
    assert data["applicant_name"] == application_data["applicant_name"]
    assert data["applicant_email"] == application_data["applicant_email"]

    # Note: We can't directly test the rule evaluation results here
    # as they are printed to console. In a production environment,
    # we would want to mock the RuleEngine and verify it was called
    # with the correct parameters.
