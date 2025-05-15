# Rules Automation Application

A full-stack application for automating document request rules based on application conditions. Built with FastAPI, React, TypeScript, and PostgreSQL.

## 🚀 Features

- **Rule Management**

  - Create, view, and manage rules
  - Define conditions using different data types (boolean, enum, year-based)
  - Set document request actions for matching rules
  - Enable/disable rules

- **Condition Types**

  - Boolean conditions (e.g., is business owner)
  - Enum conditions (e.g., family status: new/returning)
  - Year-based conditions (e.g., tax filing status for specific years)

- **Application Processing**
  - Submit applications with various fields
  - Automatic rule evaluation
  - Document request generation based on matching rules
  - OR logic for rule conditions (rule matches if any condition is met)

## 🏗 Architecture

### Backend (FastAPI)

- **Models**

  - `Application`: Stores application data
  - `Rule`: Defines rules and their actions
  - `ConditionType`: Defines available condition types
  - `Evaluation`: Records rule evaluation results

- **Services**
  - `RuleEngine`: Evaluates applications against rules
  - Handles condition matching with OR logic

### Frontend (React + TypeScript)

- **Components**

  - Rule Editor
  - Condition Builder
  - Action Builder
  - Application Form

- **State Management**
  - React Context for rule state
  - Type-safe API integration

## 🛠 Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+

### Backend Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```bash
   # Create a .env file with your database configuration
   echo "DATABASE_URL=postgresql://user:password@localhost:5432/rules_db" > .env

   # Run migrations
   alembic upgrade head

   # Seed initial data
   python -m app.db.seed
   ```

4. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## 📝 Usage

### Creating Rules

1. Navigate to the Rules page
2. Click "Create New Rule"
3. Enter rule name and description
4. Add conditions:
   - Select condition type
   - Set condition value
   - Add year if applicable
5. Add document request action
6. Save the rule

### Submitting Applications

1. Fill out the application form
2. Submit the application
3. The system automatically:
   - Evaluates all active rules
   - Creates document requests for matching rules
   - Records evaluations

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🔄 Rule Evaluation Logic

The system uses OR logic for rule conditions:

- A rule matches if ANY of its conditions are met
- Conditions are evaluated in sequence
- Evaluation stops as soon as a matching condition is found

Example:

```python
# Rule: Request tax form if:
# - Family is new OR
# - Is a business owner
rule = {
    "name": "Tax Form Request",
    "conditions": [
        {"type": "enum", "field": "family_status", "value": "new"},
        {"type": "boolean", "field": "business_owner", "value": "true"}
    ],
    "action": "Request Tax Form"
}
```

## 📚 API Documentation

Once the backend is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
