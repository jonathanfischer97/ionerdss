def strip_comment(line: str) -> str:
    """
    Removes comments from a line of code, preserving '#' characters that occur inside string literals.

    Parameters:
        line (str): A line of code that may include comments and string literals.

    Returns:
        str: The line with any trailing comment removed, unless the '#' occurs within a string.
    """
    in_string = False
    quote_char = None

    for i, char in enumerate(line):
        # Toggle string status when encountering unescaped quotes
        if char in ['"', "'"] and (i == 0 or line[i - 1] != '\\'):
            if not in_string:
                in_string = True
                quote_char = char
            elif char == quote_char:
                in_string = False
                quote_char = None

        # If '#' is found outside of a string, treat it as the start of a comment
        elif char == '#' and not in_string:
            return line[:i].strip()

    return line.strip()

