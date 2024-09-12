import string as _str
import sys as _sys

import wonderparse as _wp


def parse(
    string: "The string to be parsed.",
    /,
) -> list:
    """Parse a string to create a list of strings."""
    ans = list()
    quoting = False
    current = "w"
    for character in string:
        previous = current
        if (character in _str.whitespace) and (not quoting):
            current = "w"
            continue
        if character != '"':
            current = "l"
            if (previous == "l") or quoting:
                ans[-1] += character
            else:
                ans.append(character)
            continue
        current = "q"
        if quoting:
            quoting = False
            continue
        quoting = True
        if previous != "q":
            ans.append("")
        else:
            ans[-1] += character
    if quoting:
        raise ValueError("Unclosed quotation.")
    return ans


def main(args=None):
    parser = _wp.parser.by_object(parse, prog="inliners")
    ns = parser.parse_args(args)
    funcInput = _wp.process_namespace.by_object(parse, namespace=ns)
    try:
        ans = _wp.execution.by_object(parse, funcInput=funcInput)
    except Exception as err:
        raise SystemExit(f"Parsing with inliners failed: {err}")
    for line in ans:
        print(line)


if __name__ == "__main__":
    main()
