import pytest
from src.rule_engine import RuleEngine
from src.ast_node import ASTNode


def test_create_rule():
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    ast = RuleEngine.create_rule(rule_string)
    assert isinstance(ast, ASTNode)
    assert ast.type == "AND"


def test_combine_rules():
    rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
    combined_ast = RuleEngine.combine_rules([rule1, rule2])
    assert isinstance(combined_ast, ASTNode)
    assert combined_ast.type == "AND"


def test_evaluate_rule():
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    ast = RuleEngine.create_rule(rule_string)

    data1 = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    assert RuleEngine.evaluate_rule(ast, data1) == True

    data2 = {"age": 28, "department": "Marketing", "salary": 45000, "experience": 2}
    assert RuleEngine.evaluate_rule(ast, data2) == False


def test_invalid_rule():
    with pytest.raises(ValueError):
        RuleEngine.create_rule("invalid rule")


def test_missing_data():
    rule_string = "age > 30"
    ast = RuleEngine.create_rule(rule_string)
    data = {"department": "Sales"}
    assert RuleEngine.evaluate_rule(ast, data) == False


def test_ast_serialization():
    rule_string = "age > 30 AND salary > 50000"
    ast = RuleEngine.create_rule(rule_string)
    ast_dict = ast.to_dict()
    reconstructed_ast = ASTNode