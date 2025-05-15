from sqlalchemy.orm import Session
from app.models.condition import ConditionType
from app.models.rule import Rule, rule_conditions
from app.models.application import Application
from datetime import datetime


def seed_condition_types(db: Session):
    # Check if we already have condition types
    existing = db.query(ConditionType).first()
    if existing:
        print("Condition types already seeded")
        return

    # Define initial condition types
    condition_types = [
        ConditionType(
            name="Family Status",
            field="family_status",
            description="Checks if the family is new or returning",
            data_type="enum",
            options=["New", "Returning"]
        ),
        ConditionType(
            name="Is Business Owner",
            field="business_owner",
            description="Checks if the applicant is a business owner",
            data_type="boolean"
        ),
        ConditionType(
            name="US Tax Filing Status",
            field="filed_us_taxes",
            description="Checks if the family filed US taxes in the specified year",
            data_type="year_boolean",
            year_field="tax_year"
        )
    ]

    # Add to database
    for condition_type in condition_types:
        db.add(condition_type)

    db.commit()
    print("Seeded condition types successfully")


def seed_sample_rule(db: Session):
    # Check if we already have rules
    existing = db.query(Rule).first()
    if existing:
        print("Sample rules already seeded")
        return

    # Get condition types
    family_status = db.query(ConditionType).filter(
        ConditionType.field == "family_status").first()
    business_owner = db.query(ConditionType).filter(
        ConditionType.field == "business_owner").first()
    tax_filing = db.query(ConditionType).filter(
        ConditionType.field == "filed_us_taxes").first()

    # Create a sample rule for new families
    new_family_rule = Rule(
        name="New Family Tax Form Request",
        description="Request tax forms from new families",
        action="Tax Form",
        action_description="Request previous year's tax form"
    )
    db.add(new_family_rule)
    db.flush()  # Get the rule ID

    # Add condition
    db.execute(
        rule_conditions.insert().values(
            rule_id=new_family_rule.id,
            condition_type_id=family_status.id,
            value="New"
        )
    )

    # Create a sample rule for business owners
    business_rule = Rule(
        name="Business Owner Document Request",
        description="Request business documents from business owners",
        action="Business Documents",
        action_description="Request business registration and financial documents"
    )
    db.add(business_rule)
    db.flush()

    # Add condition
    db.execute(
        rule_conditions.insert().values(
            rule_id=business_rule.id,
            condition_type_id=business_owner.id,
            value="true"
        )
    )

    # Create a sample rule for non-tax filers
    tax_rule = Rule(
        name="Non-Tax Filer Document Request",
        description="Request tax exemption forms from families who did not file taxes",
        action="Tax Exemption Form",
        action_description="Request tax exemption documentation"
    )
    db.add(tax_rule)
    db.flush()

    # Add condition
    db.execute(
        rule_conditions.insert().values(
            rule_id=tax_rule.id,
            condition_type_id=tax_filing.id,
            value="false",
            year=2024
        )
    )

    db.commit()
    print("Seeded sample rules successfully")


def seed_applications(db: Session):
    # Check if we already have applications
    existing = db.query(Application).first()
    if existing:
        print("Applications already seeded")
        return

    # Define sample applications
    applications = [
        # Business owners who filed taxes
        Application(
            applicant_name="John Smith",
            applicant_email="john.smith@example.com",
            family_status="New",
            business_owner=True,
            filed_us_taxes=True,
            tax_year=2023,
            submitted_at=datetime(2024, 1, 15, 10, 0, 0)
        ),
        Application(
            applicant_name="Sarah Johnson",
            applicant_email="sarah.j@example.com",
            family_status="Returning",
            business_owner=True,
            filed_us_taxes=True,
            tax_year=2022,
            submitted_at=datetime(2024, 1, 20, 14, 30, 0)
        ),
        # Business owners who didn't file taxes
        Application(
            applicant_name="Mike Brown",
            applicant_email="mike.b@example.com",
            family_status="New",
            business_owner=True,
            filed_us_taxes=False,
            tax_year=2023,
            submitted_at=datetime(2024, 2, 1, 9, 15, 0)
        ),
        # Non-business owners who filed taxes
        Application(
            applicant_name="Emily Davis",
            applicant_email="emily.d@example.com",
            family_status="Returning",
            business_owner=False,
            filed_us_taxes=True,
            tax_year=2023,
            submitted_at=datetime(2024, 2, 5, 11, 45, 0)
        ),
        Application(
            applicant_name="David Wilson",
            applicant_email="david.w@example.com",
            family_status="New",
            business_owner=False,
            filed_us_taxes=True,
            tax_year=2022,
            submitted_at=datetime(2024, 2, 10, 16, 20, 0)
        ),
        # Non-business owners who didn't file taxes
        Application(
            applicant_name="Lisa Anderson",
            applicant_email="lisa.a@example.com",
            family_status="Returning",
            business_owner=False,
            filed_us_taxes=False,
            tax_year=2023,
            submitted_at=datetime(2024, 2, 15, 13, 10, 0)
        ),
        # Different family statuses
        Application(
            applicant_name="Robert Taylor",
            applicant_email="robert.t@example.com",
            family_status="New",
            business_owner=True,
            filed_us_taxes=True,
            tax_year=2023,
            submitted_at=datetime(2024, 2, 20, 15, 30, 0)
        ),
        Application(
            applicant_name="Jennifer Martinez",
            applicant_email="jennifer.m@example.com",
            family_status="Returning",
            business_owner=False,
            filed_us_taxes=True,
            tax_year=2022,
            submitted_at=datetime(2024, 2, 25, 10, 45, 0)
        ),
        # Different tax years
        Application(
            applicant_name="James Thompson",
            applicant_email="james.t@example.com",
            family_status="New",
            business_owner=True,
            filed_us_taxes=True,
            tax_year=2021,
            submitted_at=datetime(2024, 3, 1, 9, 0, 0)
        ),
        Application(
            applicant_name="Patricia Garcia",
            applicant_email="patricia.g@example.com",
            family_status="Returning",
            business_owner=False,
            filed_us_taxes=False,
            tax_year=2021,
            submitted_at=datetime(2024, 3, 5, 14, 15, 0)
        )
    ]

    # Add to database
    for application in applications:
        db.add(application)

    db.commit()
    print("Seeded applications successfully")


def seed_all(db: Session):
    """Run all seed functions"""
    seed_condition_types(db)
    seed_sample_rule(db)
    seed_applications(db)
    print("All seeding completed successfully")
