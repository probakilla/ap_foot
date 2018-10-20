import json

from geometry import rotate, line, intersection, Point


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

    return False


def parseFile(file):
    jsonFile = open(file)
    data = json.load(jsonFile)
    jsonFile.close()
    return data
