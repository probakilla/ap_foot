class Node:
    def __init__(self, pos, angle=None):
        self.pos = pos
        self.angle = angle

    def __str__(self):
        return "Node (pos: %s, angle: %s)" % (self.pos,
                                              self.angle)

    __repr__ = __str__

    def __key(self):
        return self.pos, self.angle

    def __eq__(self, y):
        return (self.angle == y.angle and self.pos == y.pos)

    def __hash__(self):
        return hash(self.__key())

    def getPos(self):
        return [self.pos.x, self.pos.y]

    def isAtk(self):
        return self.angle != None
