"""
    Different algorithms to generate defenders
"""

import numpy as np
from algo.triangle import Triangle
from algo.rectangle import Rectangle


def generateDefenders(problem):
    """
        Brute force algorithm to generate defenders (on all field).
    """
    nodes = []
    no_zones = list()
    for goal in problem.goals:
        no_zones.append(generateRectangleZone(goal))
    for i in np.arange((problem.getFieldCenter()[0] -
                        problem.getFieldWidth() / 2),
                       problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] -
                            problem.getFieldHeight() / 2),
                           problem.getFieldHeight(), problem.pos_step):
            for rect in no_zones:
                if not rect.pointInRectangle([i, j]):
                    nodes.append([i, j])
    return nodes


def generateDefendersTriangle(problem):
    """
        Generate only defenders in front of the oponents in a triangle shape
        :param problem: An instance of the problem
    """
    nodes = list()
    no_zones = list()
    triangleList = list()
    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)
        for goal in problem.goals:
            post1 = np.array([goal.posts[:, 0][0],
                              goal.posts[:, 0][1]])
            post2 = np.array([goal.posts[:, 1][0],
                              goal.posts[:, 1][1]])
            post1, post2 = increaseDistance(post1, post2, problem.pos_step)
            triangleList.append(Triangle(ofender, post1, post2))
            no_zones.append(generateRectangleZone(goal))

    maxOrdinate = problem.field_limits[1][1]
    minOrdinate = problem.field_limits[1][0]
    maxAbscissa = problem.field_limits[0][1]
    minAbscissa = problem.field_limits[0][0]
    point = np.array([maxAbscissa, maxOrdinate])
    while point[0] > minAbscissa:
        point[1] = maxOrdinate
        while point[1] > minOrdinate:
            for triangle in triangleList:
                if triangle.isInTriangle(point):
                    if not belongsToOneRect(no_zones, point):
                        nodes.append(np.array([point[0], point[1]]))
                        break
            point[1] -= problem.pos_step
        point[0] -= problem.pos_step
    return nodes


def increaseDistance(point1, point2, distance):
    if point1[1] > point2[1]:
        point1[1] += distance
        point2[1] -= distance
    else:
        point2[1] += distance
        point1[1] -= distance
    return (point1, point2)


def generateRectangleZone(goal):
    topLeft = np.array([min(goal.no_zone[0]), max(goal.no_zone[1])])
    topRight = np.array([max(goal.no_zone[0]), max(goal.no_zone[1])])
    botLeft = np.array([min(goal.no_zone[0]), min(goal.no_zone[1])])
    botRight = np.array([max(goal.no_zone[0]), min(goal.no_zone[1])])
    return Rectangle(topLeft, topRight, botLeft, botRight)


def belongsToOneRect(rectList, point):
    for rect in rectList:
        if rect.pointInRectangle(point):
            return True
    return False
