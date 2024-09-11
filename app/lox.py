import sys

class Lox:
    had_error = False

    @staticmethod
    def error(line: int, message: str) -> None:
        print(f"[line {line}] Error: {message}", file=sys.stderr)
        Lox.had_error = True
