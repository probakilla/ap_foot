''' Different algorithms for building graph from a given problem '''

import numpy as np
from algo.geometry import Point
from algo.geometry import segmentCircleIntersection
from algo.geometry import getDistance
from algo.triangle import Triangle
from graph.graph import GraphWithDict
from graph.graph import GraphWithAdjacencyMatrix
from graph.node import Node
from matplotlib.patches import Circle

ADJACENCY = 1
DICT = 2
DICT_OLD = 3


def buildGraph(problem, buildWith):
    if buildWith == DICT_OLD:
        return buildGraphWithDict(problem)

    nodes = generateDefenders(problem)
    graph = GraphWithDict() if buildWith == DICT else GraphWithAdjacencyMatrix()

    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        shootings = []
        for g in problem.goals:
            for theta in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = g.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), theta)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})
                    if buildWith == ADJACENCY:
                        graph.addAtk(atkNode)

        ofender_circle = Circle(ofender, problem.robot_radius)
        for defender in nodes:
            if not ofender_circle.contains_point(defender):
                listInterceptedShoot = []
                for shoot in shootings:
                    shootInterception = segmentCircleIntersection(
                        ofender, shoot["intersect"], defender, problem.robot_radius)
                    if shootInterception is not None:
                        listInterceptedShoot += [shoot]
                if len(listInterceptedShoot) > 0:
                    defNode = Node(Point(defender[0], defender[1]))
                    graph.addNode(defNode)
                    for interceptedShoot in listInterceptedShoot:
                        graph.addEdge(interceptedShoot["atk"], defNode)
    return graph


def generateDefenders(problem):
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(), problem.pos_step):
            nodes.append([i, j])
    return nodes

def generateDefendersTriangle(problem):
    nodes = list()
    triangleList = list()
    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)
        opponentPos = Point(ofender[0], ofender[1])
        for goal in problem.goals:
            post1 = Point(goal.posts[:, 0][0], goal.posts[:, 0][1] - 1)
            post2 = Point(goal.posts[:, 1][0], goal.posts[:, 1][1] + 1)
            triangleList.append(Triangle(opponentPos, post1, post2))

    maxOrdinate = problem.field_limits[1][1]
    minOrdinate = problem.field_limits[1][0]
    abscissa = problem.field_limits[0][1]
    minAbscissa = min(problem.opponents[0])
    point = Point(abscissa, maxOrdinate)
    while point.x > minAbscissa:
        point.y = maxOrdinate
        while point.y > minOrdinate:
            for triangle in triangleList:
                if triangle.isInTriangle(point):
                    nodes.append(Point(point.x, point.y))
                    break
            point.y -= problem.pos_step

        point.x -= problem.pos_step
    return nodes

def buildGraphWithDict(problem):
    nodes = generateDefenders(problem)
    graph = GraphWithDict()

    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        for goal in problem.goals:
            shootings = []
            for t in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = goal.kickResult(ofender, t)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), t)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

            for shooting in shootings:
                graph.addNode(shooting["atk"])
                for node in nodes:
                    if getDistance(node, shooting["intersect"]) < getDistance(ofender, shooting["intersect"]):
                        shootIntersection = segmentCircleIntersection(
                            ofender, shooting["intersect"], node, problem.robot_radius)
                        if shootIntersection is not None:
                            defNode = Node(Point(node[0], node[1]))
                            graph.addNode(defNode)
                            graph.addEdge(shooting["atk"], defNode)

    return graph


def buildGraphTriangles(problem):
    ''' Build an instance of GraphWithDict, this function may not work if the
    goal isn't vertically placed on the field. This algorithm draws 3 triangles
    from the goals posts and each oponent position, and make a 'grid' of
    defenders in each triangle '''

    graph = GraphWithDict()
    # Building a list of triangles
    nodes = list()
    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        for goal in problem.goals:
            shootings = []
            for theta in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = goal.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), theta)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

            for shooting in shootings:
                graph.addNode(shooting["atk"])
                for node in nodes:
                    if (getDistance((node.x, node.y), shooting["intersect"]) <
                        getDistance(ofender, shooting["intersect"])):
                        shootIntersection = segmentCircleIntersection(
                            ofender, shooting["intersect"], np.array((node.x, node.y)), problem.robot_radius)
                        if shootIntersection is not None:
                            defNode = Node(Point(node.x, node.y))
                            graph.addNode(defNode)
                            graph.addEdge(shooting["atk"], defNode)
    return graph
