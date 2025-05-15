from sqlalchemy.orm import Session
from app.models.condition import ConditionType
from app.models.rule import Rule, rule_conditions


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
