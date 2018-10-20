BLACK = 0
WHITE = 1

class AtkNode:
    def __init__(self, pos, color, angle):
        self.pos = pos
        self.color = color
        self.angle = angle


class DefNode:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
