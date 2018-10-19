import json

import math

from node import Point


class Goal:
    def __init__(self, leftPost, rightPost, direction):
        self.leftPost = leftPost
        self.rightPost = rightPost
        self.direction = direction


def buildGraph(file):
    jsonData = parseFile(file)
    print(intersection(line(Point(0.5, 0), Point(2, 0)), line(Point(4.5, 0.5), Point(4.5, -0.5))))
    return 0


def rotate(O, M, angle):
    angle *= math.pi / 180
    xM = M.x - O.x
    yM = M.y - O.y
    x = xM * math.cos(angle) + yM * math.sin(angle) + O.x
    y = - xM * math.sin(angle) + yM * math.cos(angle) + O.y
    return Point(round(x, 2), round(y, 2))


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
        return Point(x, y)
    else:
        return False


def parseFile(file):
    jsonFile = open(file)
    data = json.load(jsonFile)
    jsonFile.close()
    return data
