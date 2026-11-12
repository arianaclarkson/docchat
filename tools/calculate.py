
"""Safely evaluate basic arithmetic expressions."""

import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(expression):

    """Calculate arithmetic without executing Python code.

    >>> calculate("2 + 3 * 4")
    '14'
    >>> calculate("(10 - 2) / 4")
    '2.0'
    >>> calculate("-5")
    '-5'
    >>> calculate("2 ** 3")
    '8'
    >>> calculate("hello")
    'Invalid expression'
    >>> calculate("sum([1, 2])")
    'Invalid expression'
    >>> calculate("")
    'Invalid expression'
    >>> calculate("2 / 0")
    'Invalid expression'
    >>> calculate("2 +")
    'Invalid expression'
    >>> from unittest.mock import patch
    >>> with patch('tools.calculate.ast.parse', return_value=ast.Expression(body=ast.Constant(value='x'))):
    ...     calculate('1')
    'Invalid expression'
    >>> with patch('tools.calculate.ast.parse', return_value=ast.Expression(body=ast.BinOp(left=ast.Constant(2), op=ast.BitOr(), right=ast.Constant(3)))):
    ...     calculate('1')
    'Invalid expression'
    >>> with patch('tools.calculate.ast.parse', return_value=ast.Expression(body=ast.UnaryOp(op=ast.Invert(), operand=ast.Constant(2)))):
    ...     calculate('1')
    'Invalid expression'
    >>> with patch('tools.calculate.ast.parse', return_value=ast.Expression(body=ast.Name(id='x', ctx=ast.Load()))):
    ...     calculate('1')
    'Invalid expression'
    >>> with patch('tools.calculate.ast.parse', side_effect=OverflowError):
    ...     calculate('1')
    'Invalid expression'
    """

    def evaluate(node):
        """Recursively evaluate an arithmetic syntax tree node."""
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError()

        if isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError()
            return operation(
                evaluate(node.left),
                evaluate(node.right),
            )

        if isinstance(node, ast.UnaryOp):
            operation = OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError()
            return operation(evaluate(node.operand))

        raise ValueError()

    try:
        if not expression or any(
            char not in "0123456789.+-*/%() "
            for char in expression
        ):
            return "Invalid expression"

        result = evaluate(ast.parse(expression, mode="eval").body)
        return str(result)
    except (SyntaxError, ValueError, ZeroDivisionError,
            OverflowError, TypeError):
        return "Invalid expression"
