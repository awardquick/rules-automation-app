import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.rule import Rule
from app.schemas.rule import RuleCreate, RuleResponse
from unittest.mock import patch, MagicMock
from datetime import datetime

client = TestClient(app)


@pytest.fixture
def mock_db():
    """Mock database session for testing"""
    with patch("app.api.routes.rule.get_db") as mock:
        yield mock


def test_create_rule(mock_db):
    """Test creating a new rule"""
    # Use a unique name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rule_data = {
        "name": f"Test Rule {timestamp}",
        "description": "Test Description",
        "conditions": [
            {
                "condition_type_id": 1,
                "value": "test",
                "year": 2024
            }
        ],
        "action": "Test Action",
        "action_description": "Test Action Description"
    }

    # Mock the CRUD function
    with patch("app.api.routes.rule.rule_crud.create_rule") as mock_create:
        # Create a mock response that matches our schema
        mock_response = RuleResponse(
            id=1,
            name=rule_data["name"],
            description=rule_data["description"],
            action=rule_data["action"],
            action_description=rule_data["action_description"],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            conditions=[
                {
                    "condition_type_id": 1,
                    "value": "test",
                    "year": 2024
                }
            ]
        )
        mock_create.return_value = mock_response

        response = client.post("/api/rules", json=rule_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == rule_data["name"]
        assert data["action"] == rule_data["action"]
        assert len(data["conditions"]) == 1
        assert data["conditions"][0]["condition_type_id"] == 1


def test_get_rules(mock_db):
    """Test getting all rules"""
    # Mock the CRUD function
    with patch("app.api.routes.rule.rule_crud.get_rules") as mock_get:
        # Create mock responses that match our schema
        mock_rules = [
            RuleResponse(
                id=1,
                name="Rule 1",
                action="Action 1",
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                conditions=[]
            ),
            RuleResponse(
                id=2,
                name="Rule 2",
                action="Action 2",
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                conditions=[]
            )
        ]
        mock_get.return_value = mock_rules

        response = client.get("/api/rules")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["name"] == "Rule 1"
        assert data[1]["name"] == "Rule 2"


def test_create_rule_validation():
    """Test rule creation validation"""
    # Test missing required fields
    invalid_rule = {
        "description": "Test Description",
        "conditions": [],
        "action": "Test Action"
    }

    response = client.post("/api/rules", json=invalid_rule)
    assert response.status_code == 422  # Validation error

    # Test invalid condition type
    invalid_condition_rule = {
        "name": "Test Rule",
        "conditions": [
            {
                "condition_type_id": "invalid",  # Should be a number
                "value": "test"
            }
        ],
        "action": "Test Action"
    }

    response = client.post("/api/rules", json=invalid_condition_rule)
    assert response.status_code == 422
