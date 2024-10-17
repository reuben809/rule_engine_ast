<<<<<<< HEAD
# Rule Engine with AST

An efficient implementation of a rule engine using Abstract Syntax Trees (AST) for evaluating complex conditions based on user attributes.

## Features

- Create and store rules using a simple string syntax
- Combine multiple rules into a single AST
- Evaluate rules against user data
- FastAPI-based REST API for rule management and evaluation
- SQLite database for rule storage
- Efficient AST-based rule evaluation

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rule-engine-ast.git
   cd rule-engine-ast
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn src.main:app --reload
   ```

2. Access the API documentation at `http://localhost:8000/docs`

3. Use the API endpoints to create, combine, and evaluate rules

## API Endpoints

- `POST /rules`: Create a new rule
- `POST /rules/combine`: Combine multiple rules
- `POST /rules/evaluate`: Evaluate a rule against provided data

## Running Tests

Execute the test suite using pytest:

```
pytest
```

## License

This project is licensed under the MIT License.
=======
# rule_engine_ast
>>>>>>> origin/main
