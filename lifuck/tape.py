from sys import stderr

class Tape:

    class BadMoveException(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class ValueOutOfRange(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    def __init__(self, initial_state=None, min=None, max=None):
        self.min = min
        self.max = max
        self.l = [i for i in initial_state if
                  self._in_range(i)] if initial_state else [0]
        self.i = 0

        # Check if all the elements were within the range, reset if not.
        if initial_state and len(self.l) != len(initial_state):
            self.l = [0]
            print("The initial state didn't follow the min and max values given.\n"
                  "Tape created with initial state [0].",
                  file=stderr)

    def _in_range(self, value):
        return not (self.max and value > self.max) or (self.min and value < self.min)

    def right(self):
        self.i += 1
        if self.i == len(self.l):
            self.l.append(0)

    def left(self):
        self.i -= 1
        if self.i < 0:
            raise self.BadMoveException("Index can't go below 0")

    def add(self):
        if self.max and self.l[self.i] >= self.max:
            self.l[self.i] = self.min if self.min else 0
        else:
            self.l[self.i] += 1

    def sub(self):
        if self.min and self.l[self.i] <= self.min:
            self.l[self.i] = self.max if self.max else 0
        else:
            self.l[self.i] -= 1

    def get(self):
        return self.l[self.i]

    def set(self, value):
        if (self.max and value > self.max) or (self.min and value < self.min):
            raise self.ValueOutOfRange()
        else:
            self.l[self.i] = value

    def at_zero(self):
        return self.l[self.i] == 0

    def __str__(self):
        return f"[ {'  '.join([('> ' * (i == self.i))+ str(n) + (' <' * (i == self.i)) for i, n in enumerate(self.l)])} ]"
