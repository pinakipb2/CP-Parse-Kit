def number_to_letter(n, alpha="small"):
    if alpha == "capital":
        return chr(ord("A") + n - 1)
    else:
        return chr(ord("a") + n - 1)


def add_newline_if_missing(input_str):
    if not input_str.endswith("\n"):
        input_str += "\n"
    return input_str
