#!/usr/bin/env python
# encoding: utf-8
"""
Phone It In.
An entry for National Novel Generation Month (NaNoGenMo) 2015.
The plot: someone needs a computer program but the network's down,
so a second person has to tediously read it out over the telephone.
Hilarity ensues.
"""
from __future__ import print_function, unicode_literals
import argparse
import inflect  # pip install inflect
import pronouncing  # pip install pronouncing
from random import choice, random
import re

# from pprint import pprint


def print_it(text):
    """ Windows cmd.exe cannot do Unicode so encode first """
#     print(text.encode('utf-8'))
    print(text)


def percent_chance(percent):
    return random() < percent / 100.0


def load_file(the_filename):
    try:
        with open(the_filename, 'r') as f:
            lines = [
                line.decode('utf-8') for line in f]
    except IOError:
        lines = []
    return lines


def start_call():
    print("""- Hello?
- Oh, hi, is that Bob?
- Yeah, who's this?
- It's Dan.
- Oh, hi Dan. Did you get my email?
- Yup, I've got the program for you. But the problem is our network's dead.
- You're kidding?
- Nope.
- But I need that listing now...
- Sure thing, let me read it out to you.
- Erm, okay then...
- Got a pen?
- Hang on... Yep, go for it.
- Right, here goes...
""")


def end_call():
    print("""- OK, that's the end.
- That's it?
- Yup.
- All of it?
- Yes.
- Phew, what a relief! I'm not going to do that again!
- Yeah, me neither.
- Alright, thanks again, see you later Dan.
- Cheers Bob, bye then!
- But I might call you back if it doesn't compile. Is that ok Dan? Dan...?? Dan?! Dan! DAN!
""")


def leading_spaces(line):
    line = line.rstrip("\n")
    return len(line) - len(line.lstrip())


START_TEMPLATES = [
    "OK so it begins with {0} {1}.",
    "The next line begins with {0} {1}.",
    "So we've got {0} {1} at the start.",
    "Then {0} {1}.",
    "{0} {1}.",
]

UH_WHAT = [
    "- Uh, what?",
    "- Sorry, missed that bit.",
    "- Can you repeat that?",
    "- You what?",
    "- Come again?",
    "- Repeat that.",
    "- Say that again.",
    "- Sorry, what?",
]

GOT_IT = [
    "- Got it.",
    "- Yup.",
    "- Mhmm.",
    "- Alright.",
    "- Aha.",
    "- Yes.",
    "- Carry on.",
    "- Keep going.",
]

I_SAID = [
    "- I said: ",
    "- That was: ",
    "- ",
    "- It went: ",
    "- It was: ",
]


START = ["open ", "opening ", "start ", "starting "]
CLOSE = ["close ", "closing ", "end ", "ending "]
PARENTHESIS = ["round bracket,", "parenthesis,"]
BRACE = ["curly bracket,", "brace,"]
CHEVRON = ["angle bracket,", "chevron,"]

SINGLE_QUOTE = [
    "single quote",
    "single quote",
    "single quote",
    "quote\n- What kind of quote?\n- Single,",
    "quote\n- What kind of quote?\n- Single quote,",
    "quote\n- What kind of quote?\n- A single quote,",
    "quote\n- What kind of quote?\n- A single quote.\n- OK, please remember "
    "what kind, we've gone through this.\n- Yeah, sorry.",
]
DOUBLE_QUOTE = [
    "double quote",
    "double quote",
    "double quote",
    "quote\n- What kind of quote?\n- Double,",
    "quote\n- What kind of quote?\n- Double quote,",
    "quote\n- What kind of quote?\n- A double quote,",
    "quote\n- What kind of quote?\n- A double quote.\n- Right, remember to "
    "tell me which one.\n- Right, yeah, sorry.",
]
FORWARD_SLASH = [
    "forward slash",
    "forward slash",
    "forward slash",
    "slash\n- What kind of slash?\n- Forward",
    "slash\n- What kind of slash?\n- Forward slash",
    "slash\n- What kind of slash?\n- A forward slash,",
    "slash\n- What kind of slash?\n- Newcastle to Bristol,",
    "slash\n- What kind of slash?\n- A forward slash,",
    "slash\n- What kind of slash?\n- A forward slash.\n- Right, remember to "
    "tell me which one.\n- Oh yeah.",
]
BACKWARD_SLASH = [
    "backward slash",
    "backward slash",
    "backward slash",
    "slash\n- What kind of slash?\n- Backward",
    "slash\n- What kind of slash?\n- Backward slash",
    "slash\n- What kind of slash?\n- A backward slash,",
    "slash\n- What kind of slash?\n- Manchester to London,",
    "slash\n- What kind of slash?\n- A backward slash,",
    "slash\n- What kind of slash?\n- A backward slash.\n- OK, remember "
    "there's a difference.\n- Righto.",
]


def spacify(text):
    return " " + text + " "


def remove_duplicate_spaces(text):
    return re.sub(' +', ' ', text)


def upper_case_letters(text):
    l = [char for char in text if char.isupper()]
    if len(l) == 0:
        return None
    elif len(l) == 1:
        return "".join(l)
    else:
        return ", ".join(l[:-1]) + " and " + l[-1] + ", "


def upcase_first_letter(text):
    return text[0].upper() + text[1:]


def fullstop_at_end(text):
    text = text.rstrip(" ")
    if text[:-1] == ".":
        return text
    else:
        return text + "."


def you_what(out):
    """Chance of not hearing it"""
    if out:
        if percent_chance(50):
            print(choice(UH_WHAT))
            print_it(choice(I_SAID) + out.lstrip("- "))
        elif percent_chance(60):
            # Ask again about a word
            missed = choice(out.split())
            rhymes = pronouncing.rhymes(missed)
            if rhymes:
                print(choice([
                    "- Did you say {0}?",
                    "- Whas that {0}?",
                    "- Er, did you just say {0}?",
                    "- Hang on, was that {0}?",
                    ]).format(choice(rhymes)))
                print(choice([
                    "- No, ",
                    "- Nope, ",
                    "- Nah, ",
                ]) + choice([
                    "I said ",
                    "it was ",
                    "that was ",
                ]) + missed + ".")

    if percent_chance(60):
        you_what(out)


def do_line(line):
    out = None
    spaces = leading_spaces(line)
    if spaces:
        n = leading_spaces(line)
        out = choice(START_TEMPLATES).format(
            p.number_to_words(n), p.plural("space", n))
        line = line[spaces:]
        print("- " + out)

    you_what(out)
    if out:
        print(choice(GOT_IT))

    words = line.rstrip("\n").split(" ")
    new_words = []
    for word in words:

        # print(word)

        new_word = ""
        for char in word:
            if char == ",":
                new_word += spacify("comma")
            elif char == "?":
                new_word += spacify("question mark,")
            elif char == '.':
                new_word += spacify(choice(["dot", "fullstop", "period"]))
            elif char == '-' or char == "—":
                new_word += spacify(choice(["dash", "hyphen", "minus"]))
            elif char == "'":
                new_word += spacify(choice(SINGLE_QUOTE))
            elif char == '"' or char == "“" or char == "”":
                new_word += spacify(choice(DOUBLE_QUOTE))
            elif char == "#":
                new_word += spacify(choice([
                    "hash,",
                    "pound,",
                    "hash symbol,",
                    "pound symbol,",
                    "hashtag,",
                    "hashtag.\n- Don't call it a hashtag.\n- OK. "]))
            elif char == "=":
                new_word += spacify(choice([
                    "equals", "equal", "equal sign", "equals sign"]))
            elif char == "!":
                new_word += spacify("exclamation mark")
            elif char == "/":
                new_word += spacify(choice(FORWARD_SLASH))
            elif char == "\\":
                new_word += spacify(choice(BACKWARD_SLASH))
            elif char == '+':
                new_word += spacify("plus")
            elif char == ':':
                new_word += spacify("colon")
            elif char == "_":
                new_word += spacify("underscore")
            elif char == "0":
                new_word += spacify(choice(["zero", "oh"]))
            elif char == "1":
                new_word += spacify("one")
            elif char == "2":
                new_word += spacify("two")
            elif char == "3":
                new_word += spacify("three")
            elif char == "4":
                new_word += spacify("four")
            elif char == "5":
                new_word += spacify("five")
            elif char == "6":
                new_word += spacify("six")
            elif char == "7":
                new_word += spacify("seven")
            elif char == "8":
                new_word += spacify("eight")
            elif char == "9":
                new_word += spacify("nine")
            elif char == "(":
                new_word += spacify(choice(START) + choice(PARENTHESIS))
            elif char == ")":
                new_word += spacify(choice(CLOSE) + choice(PARENTHESIS))
            elif char == "[":
                new_word += spacify(choice(START) + choice(BRACE))
            elif char == "]":
                new_word += spacify(choice(CLOSE) + choice(BRACE))
            elif char == "<":
                new_word += spacify(choice(
                    ["less than", choice(START) + choice(CHEVRON)]))
            elif char == ">":
                new_word += spacify(choice([
                    "greater than", choice(CLOSE) + choice(CHEVRON)]))
            else:
                new_word += char

        if word.isupper():
            new_word = choice([
                "{0} all in caps",
                "{0} all capitals",
                "{0} in caps",
                "then capitalised {0}",
                "then upper case {0}",
                "then {0} all in caps"]).format(new_word.lower())
        else:
            uppers = upper_case_letters(word)
            if uppers:
                # Mixed case
                new_word += choice([
                    " with capital ", " with upper case ", " with big "]
                    ) + uppers

        word = new_word

        new_words.append(word)

    out = " space ".join(new_words) + choice([
        " and a new line",
        " then a new line",
        " then new line",
        " and then a new line"])

    out = remove_duplicate_spaces(out)
    out = upcase_first_letter(out)
    out = fullstop_at_end(out)
    out = "- " + out.lstrip(" ")

    print_it(out)

    you_what(out)
    if out:
        print(choice(GOT_IT))


def do_call(lines):
    for line in lines:
        do_line(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a dialogue of a program listing read out over "
                    "the telephone.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--infile', default="phonecall.py",
        help="Input file")
    args = parser.parse_args()

    # "Unit tests"
    assert upper_case_letters("abc") is None
    assert upper_case_letters("#") is None
    assert upper_case_letters("# abc") is None
    assert upper_case_letters("Abc") == "A"
    assert upper_case_letters("ABc") == "A and B, "
    assert upper_case_letters("ABC") == "A, B and C, "

    p = inflect.engine()

    lines = load_file(args.infile)
#     print(len(lines))
#     print(lines)
    start_call()
    do_call(lines)
    end_call()

# End of file
