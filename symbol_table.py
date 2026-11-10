class SymbolTable:

    def __init__(self):
        self.symbols = []

    def add(self, lexeme, data_type, scope, array_size=""):

        # Avoid duplicate declaration in same scope
        for symbol in self.symbols:
            if (
                symbol["Lexeme"] == lexeme
                and symbol["Scope"] == scope
            ):
                return

        self.symbols.append({
            "Lexeme": lexeme,
            "Type": data_type,
            "Scope": scope,
            "Array Size": array_size
        })

    def display(self):
        return self.symbols