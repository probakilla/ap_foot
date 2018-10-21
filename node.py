BLACK = 0
WHITE = 1

class AtkNode:
    def __init__(self, pos, color, angle):
        self.pos = pos
        self.color = color
        self.angle = angle

    def __str__(self):
        return "pos: %s, color: %s, angle: %s" % (self.pos, self.color, self.angle)

    __repr__ = __str__

    def __key(self):
        return (self.pos, self.angle)

    def __eq__(self, y):
        if (not isinstance(y, AtkNode)):
            return False
        return self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())


class DefNode:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def __str__(self):
        return "pos: %s, color: %s" % (self.pos, self.color)

    __repr__ = __str__

    def __key(self):
        return (self.pos)

    def __eq__(self, y):
        if (not isinstance(y, DefNode)):
            return False
        return self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())
