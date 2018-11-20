import pygame
import numpy
import math
from node import Node
from inputOutput import parseFile
from problem import Problem
from geometry import segmentCircleIntersection

DISPLAY_FIELD = 1
DISPLAY_GRAPH = 2


class Display:
    def __init__(self, graph, problem):
        self.graph = graph
        self.size = numpy.array([1500, 1000])
        self.problem = problem
        self.goalThickness = 5
        # Colors
        self.backgroundColor = (0, 0, 0)
        self.defColor = (0, 0, 255)
        self.atkColor = (255, 0, 0)
        self.edgeColor = (100, 100, 100)
        self.goalColor = (255, 255, 255)
        self.failureColor = (255, 0, 0)

    def getRatio(self):
        return 0.4 * min(self.size[0] / self.problem.field_limits[0, 1] -
                         self.problem.field_limits[0, 0],
                         self.size[1] / self.problem.field_limits[1, 1] - self.problem.field_limits[1, 0])

    def getImgCenter(self):
        return self.size / 2

    def getPixelFromField(self, posInField):
        offsetField = posInField - self.problem.getFieldCenter()
        offsetPixel = self.getRatio() * offsetField
        # Y axis is inverted  to get the Z-axis pointing outside of the screen
        offsetPixel[1] *= -1
        pixel = self.getImgCenter() + offsetPixel
        return [int(pixel[0]), int(pixel[1])]

    def drawDictNodes(self, screen):
        for node in self.graph.graphDict:
            if node.isAtk():
                pygame.draw.circle(screen, self.atkColor,
                                   self.getPixelFromField(
                                       (node.pos.x, node.pos.y)),
                                   int(self.problem.robot_radius * self.getRatio() / 2))
            else:
                pygame.draw.circle(screen, self.defColor, self.getPixelFromField(
                    (node.pos.x, node.pos.y)), int(self.problem.robot_radius * self.getRatio() / 2))

    def drawAdjacencyNodes(self, screen):
        for node in self.graph.getListNode():
            if node.isAtk():
                pygame.draw.circle(screen, self.atkColor,
                                   self.getPixelFromField(
                                       (node.pos.x, node.pos.y)),
                                   int(self.problem.robot_radius * self.getRatio() / 2))
            else:
                pygame.draw.circle(screen, self.defColor, self.getPixelFromField(
                    (node.pos.x, node.pos.y)), int(self.problem.robot_radius * self.getRatio() / 2))

    def drawSegmentInField(self, screen, color, pos1, pos2, thickness):
        start = self.getPixelFromField(pos1)
        end = self.getPixelFromField(pos2)
        pygame.draw.line(screen, color, start, end, thickness)

    def drawDictEdges(self, screen):
        for node in self.graph.graphDict:
            pos1 = (node.pos.x, node.pos.y)
            for edge in self.graph.graphDict[node]:
                pos2 = (edge.pos.x, edge.pos.y)
                self.drawSegmentInField(screen, self.edgeColor, pos1, pos2, 1)

    def drawAdjacencyEdges(self, screen):
        listNode = self.graph.getListNode()
        for nodeIndex in range(len(listNode)):
            node = listNode[nodeIndex]
            pos1 = (node.pos.x, node.pos.y)
            adjacencyMatrix = self.graph.getAdjacencyMatrix()
            for edgeIndex in range(len(adjacencyMatrix[nodeIndex])):
                if adjacencyMatrix[edgeIndex]:
                    edge = listNode[edgeIndex]
                    pos2 = (edge.pos.x, edge.pos.y)
                    self.drawSegmentInField(screen, self.edgeColor, pos1, pos2, 1)

    def drawKickRay(self, screen, robot_pos, kick_dir):
        # Getting closest goal to score
        kick_end = None
        best_dist = None
        for goal in self.problem.goals:
            kick_result = goal.kickResult(robot_pos, kick_dir)
            if not kick_result is None:
                goal_dist = numpy.linalg.norm(robot_pos - kick_result)
                if best_dist == None or goal_dist < best_dist:
                    best_dist = goal_dist
                    kick_end = kick_result
        if not kick_end is None:
            # Checking if kick is intercepted by one of the opponent and which
            # one is the first

            intercepted = False
            for defNode in self.graph.graphDict:
                if defNode.isAtk():
                    continue
                defPos = defNode.getPos()
                collide_point = segmentCircleIntersection(robot_pos, kick_end,
                                                          defPos, self.problem.robot_radius)
                if not collide_point is None:
                    kick_end = collide_point
                    intercepted = True
            # TODO
            color = self.failureColor
            if intercepted:
                color = self.edgeColor
            self.drawSegmentInField(screen, color, robot_pos, kick_end, 1)

    def drawKickRays(self, screen):
        for opponentIndex in range(self.problem.getNbOpponents()):
            opponent = self.problem.getOpponent(opponentIndex)
            kick_dir = 0
            while kick_dir < 2 * math.pi:
                self.drawKickRay(
                    screen, opponent, kick_dir)
                kick_dir += self.problem.theta_step

    def drawKickRaysAdj(self, screen):
        for opponent in self.graph.getListNode():
            kick_dir = 0
            while kick_dir < 2 * math.pi:
                self.drawKickRay(
                    screen, opponent, kick_dir)
                kick_dir += self.problem.theta_step

    def drawGoals(self, screen):
        for goal in self.problem.goals:
            self.drawSegmentInField(screen, self.goalColor, goal.posts[:, 0],
                                    goal.posts[:, 1], self.goalThickness)

    def drawDictField(self, screen):
        self.drawDictNodes(screen)
        self.drawGoals(screen)
        self.drawKickRays(screen)

    def drawAdjancencyField(self, screen):
        self.drawAdjacencyNodes(screen)
        self.drawGoals(screen)
        self.drawKickRaysAdj(screen)

    def drawDictGraph(self, screen):
        self.drawDictEdges(screen)
        self.drawDictNodes(screen)
        self.drawGoals(screen)

    def drawAdjacencyGraph(self, screen):
        self.drawAdjacencyEdges(screen)
        self.drawAdjacencyNodes(screen)
        self.drawGoals(screen)


    # If isField is set to True, draw the field from graph,
    # otherwise draw the graph (with edges instead of kicks)
    
    def run(self, display_type):
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        running = True

        f = self.drawAdjacencyGraph if display_type == DISPLAY_GRAPH else self.drawAdjancencyField
        if isinstance(self.graph, dict):
            f = self.drawDictGraph if display_type == DISPLAY_GRAPH else self.drawDictField

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            screen.fill(self.backgroundColor)
            f(screen)
            pygame.display.flip()