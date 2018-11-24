''' Specific node representation of offender and defenders '''

class Node(object):
    ''' Representation of a node in a graph with a position and an angle.
    Nodes with a None angle are considered as defenders '''
    def __init__(self, pos, angle=None):
        self.pos = pos
        self.angle = angle

    def __str__(self):
        return "Node (pos: %s, angle: %s)" % (self.pos,
                                              self.angle)

    __repr__ = __str__

    def __key(self):
        ''' Key used to differentiate it from another '''
        return self.pos, self.angle

    def __eq__(self, node):
        return self.angle == node.angle and self.pos == node.pos

    def __hash__(self):
        return hash(self.__key())

    def getPos(self):
        ''' Getter on position '''
        return [self.pos.x, self.pos.y]

    def isAtk(self):
        ''' Retrieves true if the angle is not None '''
        return self.angle != None