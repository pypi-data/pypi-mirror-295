import wonderparse as _wp

from . import _run
from ._run import *


def main(args=None):
    _wp.easymode.simple_run(
        args=args,
        program_object=_run,
        prog="utils_seq",
    )


if __name__ == "__main__":
    main()
