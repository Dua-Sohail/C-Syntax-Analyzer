from parser import Parser


def read_tokens(filename):
    tokens = []

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()

            if len(parts) < 3 or parts[0] in ("TOKEN",) or parts[0].startswith("-"):
                continue

            try:
                line_no = int(parts[-1])
            except ValueError:
                continue

            tokens.append((
                parts[0],
                " ".join(parts[1:-1]),
                line_no
            ))

    return tokens


def write_output(errors, symbols):
    with open("output.txt", "w") as file:
        file.write("SYMBOL TABLE\n")
        file.write("----------------------------------------\n")
        file.write("Lexeme\tType\tScope\tArray Size\n")

        for s in symbols:
            file.write(
                f"{s['Lexeme']}\t{s['Type']}\t"
                f"{s['Scope']}\t{s['Array Size']}\n"
            )

        file.write("\nSYNTAX ERRORS\n")
        file.write("----------------------------------------\n")

        if errors:
            file.write("\n".join(errors) + "\n")
        else:
            file.write("No syntax errors found.\n")


def main():
    tokens = read_tokens("input.txt")
    errors, symbols = Parser(tokens).parse()

    write_output(errors, symbols)

    print("Phase II parsing completed.")
    print(f"Syntax Errors: {len(errors)}")
    print(f"Symbols: {len(symbols)}")


if __name__ == "__main__":
    main()