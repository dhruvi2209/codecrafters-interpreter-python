import sys
from runtime_error import RuntimeError

class Lox:
    had_error = False
    had_runtime_error = False

    @staticmethod
    def error(line: int, message: str) -> None:
        print(f"[line {line}] Error: {message}", file=sys.stderr)
        Lox.had_error = True

    @staticmethod
    def runtime_error(error: RuntimeError) -> None:
        print(f"{error}\n[line {error.line}]", file=sys.stderr)
        Lox.had_runtime_error = True
