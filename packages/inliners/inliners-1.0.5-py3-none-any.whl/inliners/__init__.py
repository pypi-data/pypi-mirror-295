import string as _str
import sys as _sys

import click as _click
import getoptify as _getoptify


def parse(string: str, /) -> list:
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


@_getoptify.command(
    shortopts="hV",
    longopts=["help", "version"],
    allow_argv=True,
    gnu=True,
)
@_click.command(add_help_option=False)
@_click.help_option("-h", "--help")
@_click.version_option(None, "-V", "--version")
@_click.argument("string")
def main(*args):
    """parse string into list"""
    for line in parse(*args):
        _click.echo(line)


if __name__ == "__main__":
    main()
