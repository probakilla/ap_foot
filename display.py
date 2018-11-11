import pygame
import numpy
import math
from node import AtkNode
from inputOutput import parseFile
from problem import Problem
from geometry import segmentCircleIntersection


class Display:
    def __init__(self, graph, isNodesOnEdges, problem):
        self.graph = graph
        self.size = numpy.array([1000, 500])
        self.isNodesOnEdges = isNodesOnEdges
        self.problem = problem
        self.goalThickness = 5
        # Colors
        self.backgroundColor = (0, 0, 0)
        self.defColor = (0, 0, 255)
        self.atkColor = (100, 100, 100)
        self.edgeColor = (0, 255, 0)
        self.goalColor = (150, 150, 150)
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

    def drawNodes(self, screen):
        for node in self.graph.graphDict:
            if isinstance(node, AtkNode):
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

    def drawEdges(self, screen):
        for node in self.graph.graphDict:
            pos1 = (node.pos.x, node.pos.y)
            for edge in self.graph.graphDict[node]:
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
            for defNode in self.graph.getDefNodes():
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
        for node in self.graph.getAtkNodes():
            kick_dir = 0
            while kick_dir < 2 * math.pi:
                self.drawKickRay(
                    screen, node.getPos(), kick_dir)
                kick_dir += self.problem.theta_step

    def drawGoals(self, screen):
        for goal in self.problem.goals:
            self.drawSegmentInField(screen, self.goalColor, goal.posts[:, 0],
                                    goal.posts[:, 1], self.goalThickness)

    def drawField(self, screen):
        self.drawNodes(screen)
        self.drawGoals(screen)
        self.drawKickRays(screen)

    def drawGraph(self, screen):
        if not self.isNodesOnEdges:
            self.drawEdges(screen)
            self.drawNodes(screen)
            self.drawGoals(screen)
        else:
            self.drawNodes(screen)
            self.drawEdges(screen)
            self.drawGoals(screen)

    # If isField is set to True, draw the field from graph,
    # otherwise draw the graph (with edges instead of kicks)
    def run(self, isField):
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            screen.fill(self.backgroundColor)
            if isField:
                self.drawField(screen)
            else:
                self.drawGraph(screen)
            pygame.display.flip()
