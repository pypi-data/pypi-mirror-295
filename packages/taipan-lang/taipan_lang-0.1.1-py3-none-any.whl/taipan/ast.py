from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from taipan.lexer import Token, TokenKind
from taipan.symbol_table import SymbolTable
from taipan.utils import Location

type Expression = Identifier | Number | BinaryExpression | UnaryExpression
type Statement = Block | If | While | Input | Print | Declaration | Assignment


@dataclass(kw_only=True, frozen=True, repr=False)
class Node:
    location: Location

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass(kw_only=True, frozen=True, repr=False)
class Identifier(Node):
    name: str


@dataclass(kw_only=True, frozen=True, repr=False)
class Literal[T](Node):
    value: T


@dataclass(kw_only=True, frozen=True, repr=False)
class Number(Literal[float]):
    pass


@dataclass(kw_only=True, frozen=True, repr=False)
class String(Literal[str]):
    pass


class ArithmeticOperator(StrEnum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"

    @staticmethod
    def expression_from_token(token: Token) -> ArithmeticOperator | None:
        match token.kind:
            case TokenKind.PLUS:
                return ArithmeticOperator.ADD
            case TokenKind.MINUS:
                return ArithmeticOperator.SUBTRACT
            case _:
                return None

    @staticmethod
    def term_from_token(token: Token) -> ArithmeticOperator | None:
        match token.kind:
            case TokenKind.MULTIPLICATION:
                return ArithmeticOperator.MULTIPLY
            case TokenKind.DIVISION:
                return ArithmeticOperator.DIVIDE
            case TokenKind.MODULO:
                return ArithmeticOperator.MODULO
            case _:
                return None


@dataclass(kw_only=True, frozen=True, repr=False)
class BinaryExpression(Node):
    left: Expression
    right: Expression
    operator: ArithmeticOperator


class UnaryOperator(StrEnum):
    POSITIVE = "+"
    NEGATIVE = "-"

    @staticmethod
    def from_token(token: Token) -> UnaryOperator | None:
        match token.kind:
            case TokenKind.PLUS:
                return UnaryOperator.POSITIVE
            case TokenKind.MINUS:
                return UnaryOperator.NEGATIVE
            case _:
                return None


@dataclass(kw_only=True, frozen=True, repr=False)
class UnaryExpression(Node):
    value: Identifier | Number
    operator: UnaryOperator


class ComparisonOperator(StrEnum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS = "<"
    LESS_EQUAL = "<="
    GREATER = ">"
    GREATER_EQUAL = ">="

    @staticmethod
    def from_token(token: Token) -> ComparisonOperator | None:
        match token.kind:
            case TokenKind.EQUAL:
                return ComparisonOperator.EQUAL
            case TokenKind.NOT_EQUAL:
                return ComparisonOperator.NOT_EQUAL
            case TokenKind.LESS:
                return ComparisonOperator.LESS
            case TokenKind.LESS_EQUAL:
                return ComparisonOperator.LESS_EQUAL
            case TokenKind.GREATER:
                return ComparisonOperator.GREATER
            case TokenKind.GREATER_EQUAL:
                return ComparisonOperator.GREATER_EQUAL
            case _:
                return None


@dataclass(kw_only=True, frozen=True, repr=False)
class Comparison(Node):
    left: Expression | Comparison
    right: Expression
    operator: ComparisonOperator


@dataclass(kw_only=True, frozen=True, repr=False)
class Block(Node):
    statements: list[Statement] = field(default_factory=list)
    symbol_table: SymbolTable = field(default_factory=SymbolTable)


@dataclass(kw_only=True, frozen=True, repr=False)
class Program(Node):
    block: Block


@dataclass(kw_only=True, frozen=True, repr=False)
class If(Node):
    condition: Comparison
    block: Block


@dataclass(kw_only=True, frozen=True, repr=False)
class While(Node):
    condition: Comparison
    block: Block


@dataclass(kw_only=True, frozen=True, repr=False)
class Input(Node):
    identifier: Identifier


@dataclass(kw_only=True, frozen=True, repr=False)
class Print(Node):
    value: Expression | String


@dataclass(kw_only=True, frozen=True, repr=False)
class Declaration(Node):
    identifier: Identifier
    expression: Expression | None


@dataclass(kw_only=True, frozen=True, repr=False)
class Assignment(Node):
    identifier: Identifier
    expression: Expression


@dataclass
class AST:
    root: Program
