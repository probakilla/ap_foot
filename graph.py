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

    jsongoals = jsonData["goals"][0]["posts"]
    gp1 = Point(jsongoals[0][0], jsongoals[0][1])
    gp2 = Point(jsongoals[1][0], jsongoals[1][1])
    goal_line = line(gp1, gp2)

    theta_step = jsonData["theta_step"]

    for p in jsonData["opponents"]:
        opos = Point(p[0], p[1])
        g = Point(gp1.x, gp1.y)
        while g.y < gp2.y:
            g = rotate(opos, g, theta_step)

            p_intersect = intersection(line(opos, g), goal_line)
            print(Point(p_intersect.x, p_intersect.y))
        break

    return 0


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


def parseFile(file):
    jsonFile = open(file)
    data = json.load(jsonFile)
    jsonFile.close()
    return data
