import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x = " + str(self.x) + ", y = " + str(self.y)


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
    print(t)
    xt = (1 - t) * p1.x + t * p2.x
    yt = (1 - t) * p1.x + t * p2.y
    return Point(xt, yt)
