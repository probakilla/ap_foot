"""
    Represents a rectangle in the field.
"""

from algo.triangle import Triangle
from algo.geometry import getDistance

class Rectangle(object):
    EPSILON = 0.01

    def __init__(self, topLeft, topRight, botLeft, botRight):
        self.topLeft = topLeft
        self.topRight = topRight
        self.botLeft = botLeft
        self.botRight = botRight

    def __str__(self):
        return "[A: " + str(self.topLeft) + " B: " + str(self.topRight) + \
        " C: " + str(self.botRight) + " D: " + str(self.botLeft) + "]"

    def pointInRectangle(self, point):
        """
            Checks if a point is in the rectangle.
            :param point: The point to check
        """
        return self.topLeft[0] <= point[0] <= self.botRight[0] and \
                self.topLeft[1] >= point[1] >= self.botRight[1]

    def getArea(self):
        width = abs(getDistance(self.topRight, self.topLeft))
        height = abs(getDistance(self.topRight, self.botLeft))
        return height * width