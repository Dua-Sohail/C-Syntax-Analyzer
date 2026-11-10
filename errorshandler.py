def syntax_error(message, line):
    return f"Syntax Error: {message} at line {line}"


def identifier_expected(line):
    return syntax_error("Identifier expected", line)


def semicolon_expected(line):
    return syntax_error("Semicolon expected", line)


def opening_parenthesis_expected(line):
    return syntax_error("Opening parenthesis expected", line)


def closing_parenthesis_expected(line):
    return syntax_error("Closing parenthesis expected", line)


def opening_brace_expected(line):
    return syntax_error("Opening brace expected", line)


def closing_brace_expected(line):
    return syntax_error("Closing brace expected", line)


def opening_bracket_expected(line):
    return syntax_error("Opening bracket expected", line)


def closing_bracket_expected(line):
    return syntax_error("Closing bracket expected", line)


def expression_expected(line):
    return syntax_error("Expression expected", line)


def condition_expected(line):
    return syntax_error("Condition expected", line)


def assignment_operator_expected(line):
    return syntax_error("Assignment operator expected", line)


def type_expected(line):
    return syntax_error("Type specifier expected", line)


def value_expected(line):
    return syntax_error("Value expected", line)