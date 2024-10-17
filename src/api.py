from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from src.database import get_db, Rule
from src.rule_engine import RuleEngine
from src.ast_node import ASTNode
from pydantic import BaseModel

router = APIRouter()


class RuleCreate(BaseModel):
    name: str
    rule_string: str


class RuleCombine(BaseModel):
    rule_names: List[str]


class RuleEvaluate(BaseModel):
    rule_name: str
    data: Dict[str, Any]


@router.post("/rules")
def create_rule(rule: RuleCreate, db: Session = Depends(get_db)):
    """Create a new rule and store it in the database."""
    try:
        ast = RuleEngine.create_rule(rule.rule_string)
        db_rule = Rule(name=rule.name, ast=ast.to_dict())
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return {"message": "Rule created successfully", "id": db_rule.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rules/combine")
def combine_rules(rule_combine: RuleCombine, db: Session = Depends(get_db)):
    """Combine multiple rules into a single rule."""
    rules = db.query(Rule).filter(Rule.name.in_(rule_combine.rule_names)).all()
    if len(rules) != len(rule_combine.rule_names):
        raise HTTPException(status_code=404, detail="One or more rules not found")

    rule_strings = [RuleEngine._ast_to_string(ASTNode.from_dict(rule.ast)) for rule in rules]
    combined_ast = RuleEngine.combine_rules(rule_strings)

    combined_rule = Rule(name=f"Combined_{'_'.join(rule_combine.rule_names)}", ast=combined_ast.to_dict())
    db.add(combined_rule)
    db.commit()
    db.refresh(combined_rule)

    return {"message": "Rules combined successfully", "id": combined_rule.id}


@router.post("/rules/evaluate")
def evaluate_rule(rule_evaluate: RuleEvaluate, db: Session = Depends(get_db)):
    """Evaluate a rule against provided data."""
    rule = db.query(Rule).filter(Rule.name == rule_evaluate.rule_name).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    ast = ASTNode.from_dict(rule.ast)
    result = RuleEngine.evaluate_rule(ast, rule_evaluate.data)
    return {"result": result}
