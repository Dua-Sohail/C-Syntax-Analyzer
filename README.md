# C Syntax Analyzer and Symbol Table

A Python-based syntax analyzer and symbol table generator developed for the Compiler Construction course.

## Features

- Performs top-down syntax analysis
- Parses C-style program syntax
- Identifies functions and main function
- Handles variable declarations
- Handles array declarations
- Handles assignments
- Recognizes arithmetic expressions
- Handles `if / else` statements
- Handles `while` loops
- Handles `for` loops
- Handles `return` statements
- Generates a symbol table
- Tracks variable and function scopes
- Detects syntax errors
- Reports errors with line numbers
- Provides syntax error recovery
- Generates parser output

## Project Structure

- `main.py` - Main program
- `parser.py` - Syntax analysis and parsing logic
- `symbol_table.py` - Symbol table generation
- `errorshandler.py` - Syntax error handling
- `tokens.py` - Token definitions
- `input.txt` - Token input from Phase I
- `output.txt` - Generated symbol table and syntax errors

## How to Run

```bash
python main.py