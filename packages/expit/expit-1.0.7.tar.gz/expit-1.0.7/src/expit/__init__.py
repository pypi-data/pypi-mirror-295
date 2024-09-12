import math as _math

import click as _click


def function(x: float):
    try:
        p = _math.exp(-x)
    except OverflowError:
        p = float("+inf")
    return 1 / (1 + p)


@_click.command(add_help_option=False)
@_click.help_option("-h", "--help")
@_click.version_option(None, "-V", "--version")
@_click.argument("x", type=float)
def main(x: float):
    """applies the expit function to x"""
    _click.echo(function(x))


if __name__ == "__main__":
    main()
