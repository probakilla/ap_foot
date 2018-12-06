import math
import numpy as np


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def fromNumpy(cls, numpy):
        x = numpy[0]
        y = numpy[1]
        return cls(x, y)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __mul__(self, number):
        return Point(self.x * number, self.y * number)

    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        ValueError("Out of range index")

    def translate(self, distance):
        self.x += distance
        self.y += distance

    def multiplyByNumber(self, number):
        return Point(self.x * number, self.y * number)

    def divideByNumber(self, number):
        return Point(self.x / number, self.y / number)


def rotate(O, M, angle):
    angle *= math.pi / 180
    xM = M.x - O.x
    yM = M.y - O.y
    x = xM * math.cos(angle) + yM * math.sin(angle) + O.x
    y = - xM * math.sin(angle) + yM * math.cos(angle) + O.y
    return Point(round(x, 5), round(y, 5))


def line(p1, p2):
    A = (p1.y - p2.y)
    B = (p2.x - p1.x)
    C = (p1.x * p2.y - p2.x * p1.y)
    return A, B, -C


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return Point(round(x, 5), round(y, 5))
    else:
        return False


def calculateEquation(p1, p2):
    cd = (p2.y - p1.y) / (p2.x - p1.x)
    k = p1.y - (cd * p1.x)
    return {cd, k}


def newPointFromDistance(p1, p2, dt):
    d = math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))
    t = dt / d
    xt = (1 - t) * p1.x + t * p2.x
    yt = (1 - t) * p1.y + t * p2.y
    return Point(round(xt, 5), round(yt, 5))


def getDistancePts(p1, p2):
    return getDistance([p1.x, p1.y], [p2.x, p2.y])


def getDistance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


"""
Return None if there is no intersection between the line and the segment or
if the lines are coincident, otherwise, return the intersection point
"""


def segmentLineIntersection(seg_start, seg_end, line_p1, line_p2):
    # Line-segment intersection from points
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
    x1 = seg_start[0]
    y1 = seg_start[1]
    x2 = seg_end[0]
    y2 = seg_end[1]
    x3 = line_p1[0]
    y3 = line_p1[1]
    x4 = line_p2[0]
    y4 = line_p2[1]
    num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        # Line + segment are parallel or coincident
        return None
    t = num / den
    if t < 0 or t > 1:
        return None
    return np.array([x1 + t * (x2 - x1), y1 + t * (y2 - y1)])


"""
Return None if there is no intersection between the segment and the
circle. If there is an interesection, return the first intersection with the
circle.
"""


def segmentCircleIntersection(seg_start, seg_end, circle_center, circle_radius):
    # First intersect segment with the normal line passing through center of the circle
    seg_dir = seg_end - seg_start
    seg_dir = seg_dir / np.linalg.norm(seg_dir)
    normal_line_dir = np.array([-seg_dir[1], seg_dir[0]])
    normal_intersection = segmentLineIntersection(seg_start, seg_end,
                                                  circle_center, circle_center + normal_line_dir)
    # Intersection is outside of segment or too far from circle_center
    if normal_intersection is None:
        return None
    dist = np.linalg.norm(circle_center - normal_intersection)
    if dist > circle_radius:
        return None
    # Intersection is inside the circle, now going to the border in opposite direction of seg_dir
    offset_length = math.sqrt(circle_radius ** 2 - dist ** 2)  # Pythagore
    return normal_intersection - offset_length * seg_dir


def moveInLine(distance, translatedPoint, pointInLine):
    tmpoint = translatedPoint - pointInLine
    de = tmpoint.multiplyByNumber(distance).divideByNumber(
        getDistancePts(translatedPoint, pointInLine))
    return (translatedPoint - de)


def triangleArea(point1, point2, point3):
    ''' Retrieves the area of a triangle from given 3 points points should be
    from the class Point '''
    if (not isinstance(point1, Point) or
            not isinstance(point2, Point) or
            not isinstance(point3, Point)):
        ValueError("Point should be an instance of Point")

    area = (point1.x * (point2.y - point3.y) +
            point2.x * (point3.y - point1.y) +
            point3.x * (point1.y - point2.y))
    return area / 2
