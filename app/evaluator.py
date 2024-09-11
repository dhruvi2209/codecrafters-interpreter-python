# evaluator.py
from typing import Union
from my_parser import Expr
from lox import Lox
from my_parser import Expr


class Evaluator:
    def evaluate(self, expr: Expr) -> Union[str, None]:
        if isinstance(expr, Expr.Literal):
            return self.evaluate_literal(expr)
        raise ValueError(f"Unexpected expression type: {type(expr)}")

    def evaluate_literal(self, expr: Expr.Literal) -> Union[str, None]:
        if expr.value is True:
            return "true"
        elif expr.value is False:
            return "false"
        elif expr.value is None:
            return "nil"
        raise ValueError(f"Unexpected literal value: {expr.value}")
