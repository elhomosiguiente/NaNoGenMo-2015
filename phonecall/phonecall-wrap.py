#!/usr/bin/env python
# encoding: utf-8
"""
Phone It In.

Wrap output from phonecall.py
"""
from __future__ import print_function, unicode_literals
import argparse
import textwrap


def load_file(the_filename):
    with open(the_filename, 'r') as f:
        lines = [line.decode('unicode-escape') for line in f]
    return lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wrap output from phonecall.py.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--infile', default="/tmp/phonecall2e.txt",
        help="Input file")
    args = parser.parse_args()

    lines = load_file(args.infile)
    for line in lines:
        print(textwrap.fill(line, width=80,
                            initial_indent='',
                            subsequent_indent='  '))


# End of file
