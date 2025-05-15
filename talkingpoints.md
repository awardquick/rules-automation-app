# Talking Points: Current Implementation and Future Considerations

## 📚 Current Implementation

- **Document Requests:**

  - Each matching rule creates a separate evaluation record, even if multiple rules request the same document
  - No priority system between rules - all matching rules are evaluated and create their own evaluations
  - Document requests are stored in the `Evaluation` table with the format "Request document: {rule.action}"

- **Condition Types:**

  - Three predefined condition types are implemented:
    1. `boolean` - Simple true/false conditions (e.g., business_owner)
    2. `enum` - Predefined options (e.g., family_status with options ["new", "returning"])
    3. `year_boolean` - Boolean conditions that require a specific year (e.g., filed_us_taxes with tax_year)
  - Conditions are strictly typed through the `ConditionType` model
  - No free text or custom condition definitions allowed

- **Tax Year Handling:**

  - For `year_boolean` type conditions, the year is required
  - If year is not provided, the condition evaluation fails
  - Year must exactly match the specified year in the condition

- **Rule Evaluation:**
  - Rules are evaluated synchronously during application submission
  - Each rule's conditions are evaluated in sequence
  - If any condition fails, the rule is not applied
  - All matching rules create separate evaluation records

## 📚 Design Decisions & Assumptions

- **Rule Evaluation Timing:**

  - Rules are only evaluated on application submission
  - No evaluation on updates or status changes
  - This simplifies the implementation and makes the behavior predictable

- **Condition Definition:**

  - Chose predefined condition types over free text to:
    - Ensure data consistency
    - Make validation straightforward
    - Simplify the UI/UX
  - No complex logical combinations (AND/OR) to keep the system simple and maintainable

- **Document Request Behavior:**

  - Each rule creates its own evaluation record to:
    - Maintain clear audit trail
    - Allow tracking which rules triggered which requests
    - Support future rule-specific metadata

- **Tax Year Requirements:**

  - Made tax year mandatory for year_boolean conditions to:
    - Ensure data accuracy
    - Prevent ambiguous matches
    - Make the behavior explicit and predictable

- **Evaluation Storage:**
  - Store all evaluations for historical audit purposes
  - Currently not surfaced directly to end users
  - Focus on system behavior rather than user visibility

## 📚 Future Considerations

- **Document Request Deduplication:**

  - Should we consolidate multiple rules requesting the same document into a single evaluation?
  - Would this require tracking which rules contributed to the evaluation?

- **Rule Priority:**

  - Should we implement a priority system for rules?
  - How should we handle conflicting rules?

- **Action Types:**

  - Currently limited to document requests
  - Could be extended to support other actions (notifications, flags, etc.)
  - Would require changes to the `Rule` model and `RuleEngine` class

- **Performance Optimization:**

  - Current synchronous evaluation might not scale well for large numbers of rules
  - Could consider batch processing or async evaluation
  - Might need to add caching for frequently used rules/conditions

- **Error Handling:**

  - Basic error handling exists but could be enhanced
  - No retry mechanism for failed actions
  - No alert system for critical failures
  - Could add more detailed error logging and monitoring

- **Rule Management:**
  - Current UI allows basic rule creation
  - Could add more sophisticated rule management features
  - Might need better validation and testing tools for rules

## 📚 Technical Debt & Improvements

- **Code Organization:**

  - `RuleEngine` class handles both evaluation and database operations
  - Could separate concerns into distinct services
  - Might benefit from a more formal rule DSL

- **Testing:**

  - Current tests cover basic functionality
  - Need more edge cases and error scenarios
  - Could add performance testing

- **Documentation:**
  - Need better documentation of rule evaluation logic
  - Should document expected behavior for edge cases
  - Could add examples of common rule patterns
