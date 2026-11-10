from symbol_table import SymbolTable
from errorshandler import syntax_error


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.symbol_table = SymbolTable()
        self.scope = "Global"

    # ---------- Basic ----------

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek(self, n=1):
        i = self.pos + n
        return self.tokens[i] if i < len(self.tokens) else None

    def advance(self):
        if self.current():
            self.pos += 1

    def match(self, value):
        if self.current() and self.current()[1] == value:
            self.advance()
            return True
        return False

    def error(self, message, line):
        self.errors.append(syntax_error(message, line))

    def skip_line(self):
        if not self.current():
            return

        line = self.current()[2]

        while self.current() and self.current()[2] == line:
            self.advance()

    # ---------- Main ----------

    def parse(self):
        while self.current():
            token = self.current()

            if token[1] in ("int", "char", "void"):
                if (
                    self.peek()
                    and self.peek()[0] == "IDENTIFIER"
                    and self.peek(2)
                    and self.peek(2)[1] == "("
                ):
                    self.function()
                elif token[1] in ("int", "char"):
                    self.declaration()
                else:
                    self.advance()
            else:
                self.advance()

        return self.errors, self.symbol_table.display()

    # ---------- Function ----------

    def function(self):
        type_token = self.current()
        line = type_token[2]
        data_type = type_token[1]

        self.advance()

        if not self.current() or self.current()[0] != "IDENTIFIER":
            self.error("Identifier expected", line)
            self.skip_line()
            return

        name = self.current()[1]

        self.symbol_table.add(name, "Function", "Global")
        self.advance()

        if not self.match("("):
            self.error("Opening parenthesis expected", line)
            self.skip_line()
            return

        # Only parse parameters belonging to this header line
        if self.current() and self.current()[2] == line:
            if self.current()[1] != ")":
                self.parameters()

        if not self.match(")"):
            self.error("Closing parenthesis expected", line)
            return

        if not self.match("{"):
            self.error("Opening brace expected", line)
            return

        old_scope = self.scope
        self.scope = "Main" if name == "main" else name

        while self.current() and self.current()[1] != "}":
            self.statement()

        if self.current():
            self.advance()
        else:
            self.error("Closing brace expected", line)

        self.scope = old_scope

    # ---------- Parameters ----------

    def parameters(self):
        while self.current():
            token = self.current()

            if token[1] not in ("int", "char"):
                self.error("Type specifier expected", token[2])
                self.skip_line()
                return

            data_type = token[1].capitalize()
            self.advance()

            if not self.current() or self.current()[0] != "IDENTIFIER":
                self.error(
                    "Identifier expected",
                    self.current()[2] if self.current() else 0
                )
                return

            self.symbol_table.add(
                self.current()[1],
                data_type,
                self.scope
            )

            self.advance()

            if not self.match(","):
                break

    # ---------- Statements ----------

    def statement(self):
        token = self.current()

        if not token:
            return

        value = token[1]

        if value in ("int", "char"):
            self.declaration()
        elif value == "if":
            self.if_statement()
        elif value == "while":
            self.while_statement()
        elif value == "for":
            self.for_statement()
        elif value == "return":
            self.return_statement()
        elif value == "{":
            self.block()
        elif value == ";":
            self.advance()
        elif token[0] == "IDENTIFIER":
            self.assignment()
        else:
            self.advance()

    # ---------- Declaration ----------

    def declaration(self):
        data_type = self.current()[1].capitalize()
        line = self.current()[2]
        self.advance()

        while self.current():
            token = self.current()

            if token[0] != "IDENTIFIER":
                self.error("Identifier expected", token[2])
                self.skip_line()
                return

            name = token[1]
            self.advance()
            size = ""

            if self.match("["):
                if not self.current() or self.current()[0] != "INTEGER":
                    self.error("Array size expected", line)
                    self.skip_line()
                    return

                size = self.current()[1]
                self.advance()

                if not self.match("]"):
                    self.error("Closing bracket expected", line)
                    self.skip_line()
                    return

            self.symbol_table.add(
                name, data_type, self.scope, size
            )

            if self.match("="):
                if not self.expression():
                    self.error("Expression expected", line)
                    self.skip_line()
                    return

            if not self.match(","):
                break

        if not self.match(";"):
            self.error("Semicolon expected", line)
            self.skip_line()

    # ---------- Assignment ----------

    def assignment(self, no_semicolon=False):
        line = self.current()[2]
        self.advance()

        if self.match("["):
            if not self.expression():
                self.error("Expression expected", line)
                return

            if not self.match("]"):
                self.error("Closing bracket expected", line)
                return

        if self.match("=") or self.match("+=") or self.match("-="):
            if not self.expression():
                self.error("Expression expected", line)
                return

        elif not (self.match("++") or self.match("--")):
            self.error("Assignment operator expected", line)
            self.skip_line()
            return

        if not no_semicolon and not self.match(";"):
            self.error("Semicolon expected", line)
            self.skip_line()

    # ---------- Expressions ----------

    def expression(self):
        if not self.term():
            return False

        while self.current() and self.current()[1] in ("+", "-"):
            self.advance()

            if not self.term():
                return False

        return True

    def term(self):
        if not self.factor():
            return False

        while self.current() and self.current()[1] in ("*", "/", "%"):
            self.advance()

            if not self.factor():
                return False

        return True

    def factor(self):
        token = self.current()

        if not token:
            return False

        if token[0] in ("INTEGER", "CHAR", "STRING"):
            self.advance()
            return True

        if token[0] == "IDENTIFIER":
            self.advance()

            if self.match("["):
                if not self.expression():
                    return False

                if not self.match("]"):
                    self.error(
                        "Closing bracket expected",
                        token[2]
                    )
                    return False

            return True

        if token[1] == "(":
            line = token[2]
            self.advance()

            if not self.expression():
                return False

            if not self.match(")"):
                self.error("Closing parenthesis expected", line)
                return False

            return True

        return False

    # ---------- Conditions ----------

    def condition(self):
        if not self.expression():
            return False

        if self.current() and self.current()[1] in (
            "==", "!=", "<", ">", "<=", ">="
        ):
            self.advance()
            return self.expression()

        return True

    # ---------- If / While ----------

    def if_statement(self):
        self.control_statement("if")

        if self.current() and self.current()[1] == "else":
            self.advance()
            self.statement_or_block()

    def while_statement(self):
        self.control_statement("while")

    def control_statement(self, keyword):
        line = self.current()[2]
        self.advance()

        if not self.match("("):
            self.error("Opening parenthesis expected", line)
            self.skip_line()
            return

        if not self.condition():
            self.error("Condition expected", line)
            self.skip_line()
            return

        if not self.match(")"):
            self.error("Closing parenthesis expected", line)
            self.skip_line()
            return

        self.statement_or_block()

    # ---------- For ----------

    def for_statement(self):
        line = self.current()[2]
        self.advance()

        if not self.match("("):
            self.error("Opening parenthesis expected", line)
            self.skip_line()
            return

        if self.current() and self.current()[1] in ("int", "char"):
            self.declaration()
        elif self.current() and self.current()[0] == "IDENTIFIER":
            self.assignment(True)

        if not self.condition():
            self.error("Condition expected", line)
            self.skip_line()
            return

        if not self.match(";"):
            self.error("Semicolon expected", line)
            self.skip_line()
            return

        if self.current() and self.current()[0] == "IDENTIFIER":
            self.assignment(True)
        else:
            self.expression()

        if not self.match(")"):
            self.error("Closing parenthesis expected", line)
            self.skip_line()
            return

        self.statement_or_block()

    # ---------- Return ----------

    def return_statement(self):
        line = self.current()[2]
        self.advance()

        if self.current() and self.current()[1] != ";":
            if not self.expression():
                self.error("Expression expected", line)
                self.skip_line()
                return

        if not self.match(";"):
            self.error("Semicolon expected", line)
            self.skip_line()

    # ---------- Blocks ----------

    def block(self):
        line = self.current()[2]

        if not self.match("{"):
            self.error("Opening brace expected", line)
            return

        while self.current() and self.current()[1] != "}":
            self.statement()

        if self.current():
            self.advance()
        else:
            self.error("Closing brace expected", line)

    def statement_or_block(self):
        if self.current() and self.current()[1] == "{":
            self.block()
        else:
            self.statement()