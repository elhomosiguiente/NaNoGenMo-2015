#!/usr/bin/env python
# encoding: utf-8
"""
Makes an audiobook of Phone It In.

Requires OS X's say command, also sox and ffmpeg.
"""
from __future__ import print_function, unicode_literals
import codecs
import os

INFILE = "phoned-mucletters.txt"


def run(cmd):
    print(cmd)
    os.system(cmd.encode('utf-8'))

voice1 = "Alex"
voice2 = "Daniel"
print(voice1)
print(voice2)

voice = voice1
line_no = 0
chapter_no = 0
to_join = ""
chapter_format = INFILE.replace(".txt", "") + "-chapter{0:04d}.mp3"

with codecs.open(INFILE, 'r', encoding='utf8') as infile:
    for line in infile:
        line = line.strip()
        print(line)
        if not line:
            continue

        line_no += 1
        line = line.lstrip("- ")
        basename = "line{0:04d}".format(line_no)

        # Say it!
        cmd = 'say -v {0} "{1}" -o {2}.aiff'.format(voice, line, basename)
        run(cmd)

        # Switch voices for next time
        if voice == voice1:
            voice = voice2
        else:
            voice = voice1

        to_join += " " + basename + ".aiff"

        # Because sox can't open a lot of files
        if line_no % 250 == 0:
            chapter_no += 1
            output = chapter_format.format(chapter_no)
            cmd = "sox " + to_join + " " + output
            run(cmd)
            to_join = ""
            cmd = "rm *.aiff"
            run(cmd)

# Leftovers
chapter_no += 1
output = chapter_format.format(chapter_no)
cmd = "sox " + to_join + " " + output
run(cmd)
cmd = "rm *.aiff"
run(cmd)

# End of file
