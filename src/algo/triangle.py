''' This file helps to manage a triangle in the field '''


class Triangle(object):
    EPSILON = 0.001
    ''' This class contains 3 points that should be an instance of the Point
    class '''

    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.area = self.triangleArea(self.point1, self.point2, self.point3)

        self.a = 1 / (-point2[1] * point3[0] + point1[1] * (-point2[0] + point3[0]) + point1[0] * (
                    point2[1] - point3[1]) + point2[0] * point3[1])

    def __str__(self):
        return "[A: " + str(self.point1) + " B: " + str(self.point2) + \
               " C: " + str(self.point3) + "]"

    def isInTriangle(self, toCheckPoint):
        ''' Retrieves true if toCheckPoint lies in this triangle, toCheckPoint
        should be an instance of Point '''

        '''area1 = Triangle.triangleArea(toCheckPoint, self.point1, self.point2)
        area2 = Triangle.triangleArea(toCheckPoint, self.point2, self.point3)
        area3 = Triangle.triangleArea(toCheckPoint, self.point1, self.point3)
        return abs((area1 + area2 + area3) - self.area) < self.EPSILON'''
        return self.PointInsideTriangle2(toCheckPoint, self.point1, self.point2, self.point3)

    def PointInsideTriangle2(self, pt, p0, p1, p2):
        '''checks if point pt(2) is inside triangle tri(3x2). @Developer'''

        s = self.a * (p2[0] * p0[1] - p0[0] * p2[1] + (p2[1] - p0[1]) * pt[0] + (p0[0] - p2[0]) * pt[1])
        if s < 0:
            return False
        else:
            t = self.a * (p0[0] * p1[1] - p1[0] * p0[1] + (p0[1] - p1[1]) * pt[0] + (p1[0] - p0[0]) * pt[1])
        return (t > 0) and (1 - s - t > 0)

    @staticmethod
    def triangleArea(point1, point2, point3):
        ''' Retrieves the area of a triangle from 3 instances of the class
        numpy array '''
        area = (point1[0] * (point2[1] - point3[1]) +
                point2[0] * (point3[1] - point1[1]) +
                point3[0] * (point1[1] - point2[1]))
        return abs(area / 2.)
