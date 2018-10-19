class AtkNode:
    def __init__(self, pos, color, angle):
        self.pos = pos
        self.color = color
        self.angle = angle


class DefAtk:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x = " + str(self.x) + ", y = " + str(self.y)
