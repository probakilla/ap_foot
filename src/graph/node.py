''' Specific node representation of offender and defenders '''


class Node(object):
    ''' Representation of a node in a graph with a position and an angle
    Nodes with a None angle are considered as defenders '''
    EPSILON = 0.001

    def __init__(self, id, pos, angle=None):
        self.pos = pos
        self.angle = angle
        self.id = id

    def __str__(self):
        return "Node (pos: %s, angle: %s)" % (self.pos,
                                              self.angle)

    __repr__ = __str__

    def __key(self):
        ''' Key used to differentiate it from another '''
        return self.pos[0], self.pos[1], self.angle

    def __eq__(self, node):
        # Both defenders
        if self.isDef() and node.isDef():
            return self.pos[0] == node.pos[0] and self.pos[1] == node.pos[1]
        # Both attacker
        elif self.isAtk() and node.isAtk():
            return self.angle - node.angle < self.EPSILON and self.pos[0] == node.pos[0] and self.pos[1] == node.pos[1]
        return False

    def __hash__(self):
        return hash(self.__key())

    def getPos(self):
        ''' Getter on position '''
        return [self.pos[0], self.pos[1]]

    def isAtk(self):
        ''' Retrieves true if the angle is not None '''
        return self.angle is not None

    def isDef(self):
        ''' Retrieves true if the angle is None '''
        return self.angle is None
