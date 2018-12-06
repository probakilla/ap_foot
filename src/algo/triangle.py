''' This file helps to manage a triangle in the field '''

from algo.geometry import Point


class Triangle(object):
    ''' This class contains 3 points that should be an instance of the Point
    class '''

    def __init__(self, point1, point2, point3):
        Triangle.checkCorrectType(point1, point2, point3)
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

    def __str__(self):
        return "[A: " + str(self.point1) + " B: " + str(self.point2) + \
               " C: " + str(self.point3) + "]"

    def isInTriangle(self, toCheckPoint):
        ''' Retrieves true if toCheckPoint lies in this triangle, toCheckPoint
        should be an instance of Point '''
        if not isinstance(toCheckPoint, Point):
            ValueError("The point given should be an instance of Point")
        area1 = Triangle.triangleArea(toCheckPoint, self.point1, self.point2)
        area2 = Triangle.triangleArea(toCheckPoint, self.point2, self.point3)
        area3 = Triangle.triangleArea(toCheckPoint, self.point1, self.point3)
        return abs((abs(area1) + abs(area2) + abs(area3)) - self.getArea()) < 0.001

    def getArea(self):
        ''' Retrieves the area of the triangle '''
        return self.triangleArea(self.point1, self.point2, self.point3)

    @staticmethod
    def triangleArea(point1, point2, point3):
        ''' Retrieves the area of a triangle from 3 instances of the class
        Point '''
        Triangle.checkCorrectType(point1, point2, point3)
        area = (point1.x * (point2.y - point3.y) +
                point2.x * (point3.y - point1.y) +
                point3.x * (point1.y - point2.y))
        return area / 2

    @staticmethod
    def checkCorrectType(point1, point2, point3):
        ''' Check if the three points are instances of Point class '''
        if (not isinstance(point1, Point) or
                not isinstance(point2, Point) or
                not isinstance(point3, Point)):
            ValueError("Points should be an instance of Point")
