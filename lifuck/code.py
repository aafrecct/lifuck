from sys import stdin, stdout

class Code:

    class BadFunctionDeclaration(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    def __init__(self, iterable, tape, input_file):
        self.code = iterable
        self.tape = tape
        self.input_file = input_file

        self.loopc = 0
        self.loopb = None
        self.funcc = 0
        self.funcs = []

    def _step(self, char):
        if self.funcc:
            match char:
                case '(':
                    raise self.BadFunctionDeclaration("Nested functions are not supported.")
                case ')':
                    self.funcc -= 1
                case _:
                    self.funcs[-1].add(char)
        elif self.loopc:
            self.loopb.add(char)
            match char:
                case '(':
                    raise self.BadFunctionDeclaration("Functions can't be declared inside loops.")
                case '[':
                    self.loopc += 1
                case ']':
                    self.loopc -= 1
                    if self.loopc == 0:
                        self.loopb.code = self.loopb.code[:-1]
                        self.loopb.run()
                        self.loopb = None
        else:
            match char:
                case '+':
                    self.tape.add()
                case '-':
                    self.tape.sub()
                case '>':
                    self.tape.right()
                case '<':
                    self.tape.left()
                case '.':
                    v = self.tape.get()
                    if v in range(32, 128):
                        print(chr(v), end='')
                    else:
                        print(str(v), end=' ')

                case ',':
                    v = next(self.input_file)
                    try:
                        self.tape.set(int(v))
                    except ValueError:
                        self.tape.set(ord(v[0]))
                case '[':
                    self.loopb = Loop(self.tape, self.input_file)
                    self.loopc += 1
                case '(':
                    self.funcs.append(Func(self.tape, self.input_file))
                    self.funcc += 1
                case '*':
                    i = self.tape.get()
                    if 0 <= i < len(self.funcs):
                        self.funcs[i].run()

    def run(self):
        for char in self.code:
            self._step(char)
        print()


class Loop(Code):

    def __init__(self, tape, input_file=stdin):
        super().__init__("", tape, input_file)

    def add(self, char):
        self.code += char

    def run(self):
        while not self.tape.at_zero():
            for char in self.code:
                self._step(char)


class Func(Code):
    def __init__(self, tape, input_file=stdin):
        super().__init__("", tape, input_file)

    def add(self, char):
        self.code += char

    def run(self):
        for char in self.code:
            self._step(char)
