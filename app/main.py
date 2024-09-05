from typing import Callable, Dict, List, Optional
import sys

# Define Token Types
class TokenType:
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    STAR = 'STAR'
    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    SLASH = 'SLASH'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    IDENTIFIER = 'IDENTIFIER'
    EOF = 'EOF'

    AND = 'AND'
    CLASS = 'CLASS'
    ELSE = 'ELSE'
    FALSE = 'FALSE'
    FOR = 'FOR'
    FUN = 'FUN'
    IF = 'IF'
    NIL = 'NIL'
    OR = 'OR'
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    SUPER = 'SUPER'
    THIS = 'THIS'
    TRUE = 'TRUE'
    VAR = 'VAR'
    WHILE = 'WHILE'

# Token class to represent individual tokens
class Token:
    def __init__(self, type: str, lexeme: str, literal: Optional[object], line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

# Lox class for handling errors
class Lox:
    had_error = False

    @staticmethod
    def error(line: int, message: str) -> None:
        print(f"[line {line}] Error: {message}", file=sys.stderr)
        Lox.had_error = True

# Scanner class to tokenize the input source code
class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error_occurred = False
        
        # Reserved words dictionary
        self.reserved_words = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

        # Token actions dictionary
        self.token_actions: Dict[str, Callable[[], None]] = {
            "(": lambda: self.add_token(TokenType.LEFT_PAREN),
            ")": lambda: self.add_token(TokenType.RIGHT_PAREN),
            "{": lambda: self.add_token(TokenType.LEFT_BRACE),
            "}": lambda: self.add_token(TokenType.RIGHT_BRACE),
            ",": lambda: self.add_token(TokenType.COMMA),
            ".": self.handle_dot,
            "-": lambda: self.add_token(TokenType.MINUS),
            "+": lambda: self.add_token(TokenType.PLUS),
            ";": lambda: self.add_token(TokenType.SEMICOLON),
            "*": lambda: self.add_token(TokenType.STAR),
            "!": lambda: self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG),
            "=": lambda: self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL),
            "<": lambda: self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS),
            ">": lambda: self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER),
            "/": self.handle_slash,
            '"': self.handle_string,
        }

    # Method to scan tokens from the source code
    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    # Method to scan a single token
    def scan_token(self) -> None:
        char = self.advance()

        if char in self.token_actions:
            self.token_actions[char]()
        elif char.isalpha() or char == "_":
            self.identifier()
        elif char.isdigit():
            self.number()
        elif char.isspace():
            if char == '\n':
                self.line += 1
        else:
            Lox.error(self.line, f"Unexpected character: {char}")
            self.error_occurred = True

    # Method to handle identifiers and reserved words
    def identifier(self) -> None:
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start:self.current]

        # Check if the identifier is a reserved word
        token_type = self.reserved_words.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)  # Literal is None for identifiers

    # Method to handle dot character
    def handle_dot(self) -> None:
        if self.peek().isdigit():
            self.number()
        else:
            self.add_token(TokenType.DOT)

    # Method to handle numbers
    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()  # Consume the '.'
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    # Helper method to check if a character is a digit
    def is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'

    # Method to peek at the next character without advancing
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    # Method to handle slashes (for comments or division)
    def handle_slash(self) -> None:
        if self.match("/"):
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
        else:
            self.add_token(TokenType.SLASH)

    def handle_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            Lox.error(self.line, "Unterminated string.")
            return  # Stop processing this token, don't add it

        self.advance()  # Consume the closing quote
        value = self.source[self.start + 1:self.current - 1]  # Trim the surrounding quotes
        self.add_token(TokenType.STRING, value)


    # Method to advance to the next character and return the current one
    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    # Method to match and consume the next character if it matches the expected one
    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    # Method to add a token to the list of tokens
    def add_token(self, type: str, literal: Optional[object] = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    # Method to peek at the current character without advancing
    def peek(self) -> str:
        return "\0" if self.is_at_end() else self.source[self.current]

    # Method to check if the scanner has reached the end of the source code
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

# Main function to handle command-line input and scanning
def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != 'tokenize':
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        sys.exit(64)

    filename = sys.argv[2]
    with open(filename, 'r') as f:
        source_code = f.read()

    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()

    # Print tokens in the format expected by the tester
    for token in tokens:
        token_type = token.type
        token_lexeme = token.lexeme
        if token_type == TokenType.STRING:
            literal = token.literal
            print(f'{token_type} "{token_lexeme}" {literal}')
        else:
            print(f'{token_type} {token_lexeme} null')

    # Check if an error was encountered
    if Lox.had_error:
        sys.exit(65)

# Ensure that this code only runs when the script is executed directly
if __name__ == "__main__":
    main()