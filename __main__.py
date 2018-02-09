""" Run sequence of programs.

Each program (except first) receives the output of the previous program on its standard input.
There are several ways of passing data between programs.

"""

import argparse
from .interface.TextInterface import TextInterface


def _launch():
    parser = argparse.ArgumentParser(
        prog='python -m pipeline',
        description=__doc__
    )
    parser.add_argument('-k', '--keep-going', action='store_true', default=False)

    parser.add_argument('filename')

    args = parser.parse_args()

    iface = TextInterface(args.keep_going, args.filename)
    iface.cmdloop()

if __name__ == '__main__':
    _launch()
