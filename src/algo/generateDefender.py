"""
    Different algorithms to generate defenders
"""

import numpy as np
from algo.triangle import Triangle


def generateDefenders(problem):
    """
        Brute force algorithm to generate defenders (on all field).
    """
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] -
                        problem.getFieldWidth() / 2),
                       problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] -
                            problem.getFieldHeight() / 2),
                           problem.getFieldHeight(), problem.pos_step):
            nodes.append([i, j])
    return nodes


def generateDefendersTriangle(problem):
    """
        Generate only defenders in front of the oponents in a triangle shape
        :param problem: An instance of the problem
    """
    nodes = list()
    triangleList = list()
    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)
        for goal in problem.goals:
            post1 = np.array([goal.posts[:, 0][0],
                              goal.posts[:, 0][1] - problem.pos_step])
            post2 = np.array([goal.posts[:, 1][0],
                              goal.posts[:, 1][1] + problem.pos_step])
            triangleList.append(Triangle(ofender, post1, post2))

    maxOrdinate = problem.field_limits[1][1]
    minOrdinate = problem.field_limits[1][0]
    abscissa = problem.field_limits[0][1]
    minAbscissa = min(problem.opponents[0])
    point = np.array([abscissa, maxOrdinate])
    while point[0] > minAbscissa:
        point[1] = maxOrdinate
        while point[1] > minOrdinate:
            for triangle in triangleList:
                if triangle.isInTriangle(point):
                    nodes.append(np.array([point[0], point[1]]))
                    break
            point[1] -= problem.pos_step
        point[0] -= problem.pos_step
    return nodes
