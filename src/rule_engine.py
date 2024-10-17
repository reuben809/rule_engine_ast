import re
from typing import Dict, Any, List, Union
from src.ast_node import ASTNode


class RuleEngine:
    @staticmethod
    def create_rule(rule_string: str) -> ASTNode:
        """
        Create an AST from a rule string.

        Args:
            rule_string (str): The rule string to parse.

        Returns:
            ASTNode: The root node of the AST.

        Raises:
            ValueError: If the rule string is invalid.
        """
        tokens = RuleEngine._tokenize(rule_string)
        return RuleEngine._parse_expression(tokens)

    @staticmethod
    def _tokenize(rule_string: str) -> List[str]:
        """Tokenize the rule string."""
        return re.findall(r'\(|\)|AND|OR|[^()\s]+', rule_string)

    @staticmethod
    def _parse_expression(tokens: List[str]) -> ASTNode:
        """Parse tokens into an AST."""
        if len(tokens) == 1:
            return RuleEngine._parse_condition(tokens[0])

        if tokens[0] == '(':
            depth = 1
            for i, token in enumerate(tokens[1:], 1):
                if token == '(':
                    depth += 1
                elif token == ')':
                    depth -= 1
                    if depth == 0:
                        left = RuleEngine._parse_expression(tokens[1:i])
                        if i + 1 < len(tokens):
                            operator = tokens[i + 1]
                            right = RuleEngine._parse_expression(tokens[i + 2:])
                            return ASTNode(operator, left, right)
                        return left

        raise ValueError(f"Invalid rule: {' '.join(tokens)}")

    @staticmethod
    def _parse_condition(condition: str) -> ASTNode:
        """Parse a single condition into an ASTNode."""
        parts = condition.split()
        if len(parts) == 3:
            return ASTNode('CONDITION', value=condition)
        raise ValueError(f"Invalid condition: {condition}")

    @staticmethod
    def combine_rules(rules: List[str]) -> ASTNode:
        """
        Combine multiple rules into a single AST.

        Args:
            rules (List[str]): List of rule strings to combine.

        Returns:
            ASTNode: The root node of the combined AST.
        """
        if not rules:
            return None
        if len(rules) == 1:
            return RuleEngine.create_rule(rules[0])

        combined = RuleEngine.create_rule(rules[0])
        for rule in rules[1:]:
            combined = ASTNode('AND', combined, RuleEngine.create_rule(rule))

        return combined

    @staticmethod
    def evaluate_rule(node: ASTNode, data: Dict[str, Any]) -> bool:
        """
        Evaluate a rule against provided data.

        Args:
            node (ASTNode): The root node of the AST to evaluate.
            data (Dict[str, Any]): The data to evaluate against.

        Returns:
            bool: The result of the evaluation.

        Raises:
            ValueError: If an invalid node type is encountered.
        """
        if node.type in ('AND', 'OR'):
            left = RuleEngine.evaluate_rule(node.left, data)
            right = RuleEngine.evaluate_rule(node.right, data)
            return left and right if node.type == 'AND' else left or right
        elif node.type == 'CONDITION':
            return RuleEngine._evaluate_condition(node.value, data)
        else:
            raise ValueError(f"Invalid node type: {node.type}")

    @staticmethod
    def _evaluate_condition(condition: str, data: Dict[str, Any]) -> bool:
        """Evaluate a single condition against provided data."""
        attribute, operator, value = condition.split()
        if attribute not in data:
            return False

        if operator == '=':
            return str(data[attribute]) == value
        elif operator == '>':
            return float(data[attribute]) > float(value)
        elif operator == '<':
            return float(data[attribute]) < float(value)
        else:
            raise ValueError(f"Invalid operator: {operator}")
