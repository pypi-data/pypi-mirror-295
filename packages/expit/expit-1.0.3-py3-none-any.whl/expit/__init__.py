import math as _math

import wonderparse as _wp


def function(x: float):
    try:
        p = _math.exp(-x)
    except OverflowError:
        p = float("+inf")
    return 1 / (1 + p)


def main(args=None):
    _wp.easymode.simple_run(
        args=args,
        program_object=function,
        prog="expit",
    )


if __name__ == "__main__":
    main()
