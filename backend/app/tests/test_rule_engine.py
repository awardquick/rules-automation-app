import pytest
from services.rule_engine import RuleEngine
from schemas.application import ApplicationCreate
from models.rule import Rule
from unittest.mock import MagicMock


@pytest.fixture
def db_session_mock():
    """Mock database session for testing"""
    db = MagicMock()
    return db


@pytest.fixture
def sample_rules():
    return [
        Rule(id=1, name="New Family", condition="family_status == new",
             action="Request Tax Form", is_active=True),
        Rule(id=2, name="Business Owner", condition="business_owner == true",
             action="Request Business Docs", is_active=True),
        Rule(id=3, name="Did Not File Taxes", condition="did not file us taxes in 2024",
             action="Request Tax Exemption Form", is_active=True),
    ]


def test_evaluate_condition_family_status():
    engine = RuleEngine(db=None)
    app_data = ApplicationCreate(
        family_status="new", business_owner=False, filed_us_taxes=True, tax_year=2024)

    assert engine.evaluate_condition(app_data, "family_status == new") is True
    assert engine.evaluate_condition(
        app_data, "family_status == returning") is False


def test_evaluate_condition_business_owner():
    engine = RuleEngine(db=None)
    app_data = ApplicationCreate(
        family_status="returning", business_owner=True, filed_us_taxes=True, tax_year=2024)

    assert engine.evaluate_condition(
        app_data, "business_owner == true") is True


def test_evaluate_condition_did_not_file_taxes():
    engine = RuleEngine(db=None)
    app_data = ApplicationCreate(
        family_status="new", business_owner=False, filed_us_taxes=False, tax_year=2024)

    assert engine.evaluate_condition(
        app_data, "did not file us taxes in 2024") is True


def test_evaluate_applies_correct_rules(db_session_mock, sample_rules):
    db_session_mock.query.return_value.filter.return_value.all.return_value = sample_rules

    app_data = ApplicationCreate(
        family_status="new",
        business_owner=True,
        filed_us_taxes=False,
        tax_year=2024)

    engine = RuleEngine(db=db_session_mock)

    actions = engine.evaluate_application(application_record=MagicMock(
        id=1), application_data=app_data)

    assert len(actions) == 3
    assert "Request Tax Form" in actions
    assert "Request Business Docs" in actions
    assert "Request Tax Exemption Form" in actions
