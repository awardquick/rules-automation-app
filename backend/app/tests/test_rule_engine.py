import pytest
from services.rule_engine import RuleEngine
from schemas.application import ApplicationCreate
from models.rule import Rule, rule_conditions
from models.condition import ConditionType
from unittest.mock import MagicMock, patch
from datetime import datetime


@pytest.fixture
def db_session_mock():
    """Mock database session for testing"""
    db = MagicMock()
    return db


@pytest.fixture
def sample_condition_types():
    return [
        ConditionType(
            id=1,
            name="Family Status",
            field="family_status",
            description="Checks if the family is new or returning",
            data_type="enum",
            options=["new", "returning"]
        ),
        ConditionType(
            id=2,
            name="Is Business Owner",
            field="business_owner",
            description="Checks if the applicant is a business owner",
            data_type="boolean"
        ),
        ConditionType(
            id=3,
            name="US Tax Filing Status",
            field="filed_us_taxes",
            description="Checks if the family filed US taxes in the specified year",
            data_type="year_boolean",
            year_field="tax_year"
        )
    ]


@pytest.fixture
def sample_rule_conditions():
    return [
        # Rule 1: New Family
        {"rule_id": 1, "condition_type_id": 1, "value": "new", "year": None},
        # Rule 2: Business Owner
        {"rule_id": 2, "condition_type_id": 2, "value": "true", "year": None},
        # Rule 3: Did Not File Taxes
        {"rule_id": 3, "condition_type_id": 3, "value": "false", "year": 2024}
    ]


@pytest.fixture
def sample_rules(sample_condition_types):
    return [
        Rule(
            id=1,
            name="New Family",
            action="Request Tax Form",
            action_description="Request tax form for new families",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Rule(
            id=2,
            name="Business Owner",
            action="Request Business Docs",
            action_description="Request business documentation",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Rule(
            id=3,
            name="Did Not File Taxes",
            action="Request Tax Exemption Form",
            action_description="Request tax exemption documentation",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]


def test_evaluate_condition_family_status():
    engine = RuleEngine(db=None)
    app_data = ApplicationCreate(
        applicant_name="John Doe",
        applicant_email="john@example.com",
        family_status="new",
        business_owner=False,
        filed_us_taxes=True,
        tax_year=2024,
        submitted_at=datetime.utcnow()
    )
    condition_type = ConditionType(
        id=1,
        name="Family Status",
        field="family_status",
        data_type="enum",
        options=["new", "returning"]
    )
    assert engine.evaluate_condition(app_data, condition_type, "new") is True
    assert engine.evaluate_condition(
        app_data, condition_type, "returning") is False


def test_evaluate_condition_business_owner():
    engine = RuleEngine(db=None)
    app_data = ApplicationCreate(
        applicant_name="John Doe",
        applicant_email="john@example.com",
        family_status="returning",
        business_owner=True,
        filed_us_taxes=True,
        tax_year=2024,
        submitted_at=datetime.utcnow()
    )
    condition_type = ConditionType(
        id=2,
        name="Is Business Owner",
        field="business_owner",
        description="Checks if the applicant is a business owner",
        data_type="boolean"
    )
    assert engine.evaluate_condition(app_data, condition_type, "true") is True
    assert engine.evaluate_condition(
        app_data, condition_type, "false") is False


def test_evaluate_condition_did_not_file_taxes():
    engine = RuleEngine(db=None)
    app_data = ApplicationCreate(
        applicant_name="John Doe",
        applicant_email="john@example.com",
        family_status="new",
        business_owner=False,
        filed_us_taxes=False,
        tax_year=2024,
        submitted_at=datetime.utcnow()
    )
    condition_type = ConditionType(
        id=3,
        name="US Tax Filing Status",
        field="filed_us_taxes",
        description="Checks if the family filed US taxes in the specified year",
        data_type="year_boolean",
        year_field="tax_year"
    )
    # For year_boolean type, we check if the field is False AND the year matches
    assert engine.evaluate_condition(
        app_data, condition_type, "false", 2024) is True
    # If the year doesn't match, it should be False
    assert engine.evaluate_condition(
        app_data, condition_type, "false", 2023) is False
    # If the field is True, it should be False regardless of year
    app_data.filed_us_taxes = True
    assert engine.evaluate_condition(
        app_data, condition_type, "false", 2024) is False


def test_evaluate_applies_correct_rules(db_session_mock, sample_rules, sample_condition_types, sample_rule_conditions):
    # Create a mock query object that can handle different queries
    mock_query = MagicMock()

    # Set up the rules query
    def get_rules():
        mock = MagicMock()
        mock.filter.return_value.all.return_value = sample_rules
        return mock

    # Set up the rule conditions query
    def get_rule_conditions():
        mock = MagicMock()
        # Filter conditions by rule_id

        def filter_conditions(rule_id):
            filtered_conditions = [
                MagicMock(
                    rule_id=rc['rule_id'],
                    condition_type_id=rc['condition_type_id'],
                    value=rc['value'],
                    year=rc['year']
                )
                for rc in sample_rule_conditions
                if rc['rule_id'] == rule_id
            ]
            mock.all.return_value = filtered_conditions
            return mock
        mock.filter.side_effect = filter_conditions
        return mock

    # Set up the condition type query
    def get_condition_type(id):
        return next((ct for ct in sample_condition_types if ct.id == id), None)

    # Configure the mock query to handle different queries
    def mock_query_side_effect(*args, **kwargs):
        print(f"\nMock query called with args: {args}")
        if args and (args[0] == Rule or (hasattr(args[0], '__name__') and args[0].__name__ == 'Rule')):
            print("Returning rules mock")
            mock = MagicMock()
            mock.filter.return_value.all.return_value = sample_rules
            return mock
        elif args and (args[0] == ConditionType or (hasattr(args[0], '__name__') and args[0].__name__ == 'ConditionType')):
            print("Returning condition type mock")
            mock = MagicMock()
            mock.get.side_effect = get_condition_type
            return mock
        elif args and (args[0] == rule_conditions or (hasattr(args[0], 'name') and args[0].name == 'rule_conditions')):
            print("Returning rule conditions mock")
            return get_rule_conditions()
        print("Returning default mock")
        return MagicMock()

    db_session_mock.query.side_effect = mock_query_side_effect

    # Mock the commit method
    db_session_mock.commit = MagicMock()

    # Mock the add method
    db_session_mock.add = MagicMock()

    engine = RuleEngine(db_session_mock)
    app_data = ApplicationCreate(
        applicant_name="John Doe",
        applicant_email="john@example.com",
        family_status="new",
        business_owner=True,
        filed_us_taxes=False,
        tax_year=2024,
        submitted_at=datetime.utcnow()
    )

    # Mock the application record
    app_record = MagicMock()
    app_record.id = 1

    # Test rule evaluation
    evaluations = engine.evaluate_application(app_record, app_data)

    # Print debug information
    print("\nDebug Information:")
    print(f"Number of evaluations: {len(evaluations)}")
    print(f"Sample rules: {sample_rules}")
    print(f"Sample condition types: {sample_condition_types}")
    print(f"Sample rule conditions: {sample_rule_conditions}")

    # Verify that the correct rules were applied
    assert len(evaluations) == 3  # All three rules should match
    actions = [e.action_taken for e in evaluations]
    assert "Request document: Request Tax Form" in actions
    assert "Request document: Request Business Docs" in actions
    assert "Request document: Request Tax Exemption Form" in actions
