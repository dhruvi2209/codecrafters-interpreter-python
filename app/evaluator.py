from typing import Union
from my_parser import Expr

class Evaluator:
    def evaluate(self, expr: Expr) -> Union[float, str, None]:
        if isinstance(expr, Expr.Literal):
            return self.evaluate_literal(expr)
        elif isinstance(expr, Expr.Grouping):
            return self.evaluate(expr.expression)
        else:
            raise ValueError(f"Unexpected expression type: {type(expr)}")

    def evaluate_literal(self, expr: Expr.Literal) -> Union[float, str, None]:
        if expr.value is True:
            return "true"
        elif expr.value is False:
            return "false"
        elif expr.value is None:
            return "nil"
        elif isinstance(expr.value, float):
            # Format float values as needed
            if expr.value.is_integer():
                return str(int(expr.value))
            return str(expr.value)
        elif isinstance(expr.value, str):
            return expr.value
        else:
            raise ValueError(f"Unexpected literal value: {expr.value}")
