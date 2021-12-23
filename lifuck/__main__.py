"""
A brainfuck interpreter with extra syntax that allows for procedure declaration
and calling, or "brainfuck with functions".

Usage:
    lyfuck file -[flags]

Flags:
    -h --help: Displays this message.
    -c --max=i: Sets the maximum value of each cell to i.
    -b --min=i: Sets the minimum value of each cell to i.
    -r --range=i: Sets the minimun cell value to -i and the maximum to i.
    -n --nonneg: Sets the minimum cell value to 0
    -i --input=file: Sets the input to the file specified
    -t --tape=tape: If passed the string representation of a list, will initialize
        the tape with the given values.
"""

from tape import Tape
from code import Code
from sys import argv, stdin, stderr


def file_chars(file):
    if type(file) is str:
        with open(file, 'r') as fd:
            for line in fd:
                for char in line:
                    yield char
    elif file == stdin:
        for line in file:
            for char in line:
                yield char

flag_dict = {'help': 'h',
             'max': 'c',
             'min': 'b',
             'range' : 'r',
             'nonneg': 'n',
             'input': 'i',
             'tape': 't'}


flags = {}
file = False
prev = ' '
for arg in argv[1: ]:
    if prev in 'cbrit':
        flags[prev] = arg
    elif arg[0] == '-':
        if arg[1] == '-':
            arg = arg[2:].split('=')
            if len(arg) == 2:
                flags[flag_dict.get(arg[0], 'h')] = arg[1]
            else:
                flags[flag_dict.get(arg[0], 'h')] = ''
        else:
            for f in arg[1:]:
                if f in 'cbrit':
                    prev = f
                else:
                    flags[f] = ''
    else:
        if not file:
            file = file_chars(arg)
        else:
            print(f"Extra argument {arg} is not understood. Use -h for help.", file=stderr)
            exit(1)

try:
    f = sorted(flags.keys(), key=lambda x: 'hcbrnit'.index(x))
except:
    print("Argument format not correct. Check for '--' if using the full name of flag.", file=stderr)
    exit(3)

initape = [0]
minv = None
maxv = None
inputfile = file_chars(stdin)
for c in f:
    match c:
        case 'h':
            print(locals()['__doc__'])
            exit(0)
        case 'c':
            maxv = int(flags['c'])
        case 'b':
            minv = int(flags['b'])
        case 'r':
            minv = -int(flags['r'])
            maxv = int(flags['r'])
        case 'n':
            minv = max(minv, 0)
        case 'i':
            inputfile = file_chars(flags['r'])
        case 't':
            e = eval(flags['r'])
            if type(e) == list:
                initape = e
            else:
                print("Invalid initial tape format.", file=stderr)
                exit(2)

if not file:
    print("File not given.", file=stderr)
    exit(4)

tape = Tape(initape, minv, maxv)
Code(file, tape, inputfile).run()
print(tape)
