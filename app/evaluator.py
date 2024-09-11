# evaluator.py
from typing import Union
from my_parser import Expr
from lox import Lox

class Evaluator:
    def evaluate(self, expr: Expr) -> Union[bool, None]:
        if isinstance(expr, Expr.Literal):
            return self.evaluate_literal(expr)
        raise ValueError(f"Unexpected expression type: {type(expr)}")

    def evaluate_literal(self, expr: Expr.Literal) -> Union[bool, None]:
        if expr.value is True:
            return True
        elif expr.value is False:
            return False
        elif expr.value is None:
            return None
        raise ValueError(f"Unexpected literal value: {expr.value}")
