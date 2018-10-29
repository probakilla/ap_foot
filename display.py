import pygame
import numpy
from node import AtkNode, DefNode
from inputOutput import parseFile


class Display:
    def __init__(self, graph, isNodesOnEdges, filePath):
        self.initFromFile(filePath)
        self.graph = graph
        self.size = numpy.array([1000, 500])
        self.isNodesOnEdges = isNodesOnEdges

        # Colors
        self.backgroundColor = (0, 0, 0)
        self.defColor = (0, 0, 255)
        self.atkColor = (255, 0, 0)
        self.edgeColor = (150, 150, 150)

    def initFromFile(self, filePath):
        data = parseFile(filePath)
        self.fieldWidth = numpy.array(data["field_limits"])
        self.robotWidth = data["robot_radius"]

    def getFieldCenter(self):
        return (self.fieldWidth[:, 1] + self.fieldWidth[:, 0]) / 2

    def getRatio(self):
        return 0.4 * min(self.size[0] / self.fieldWidth[0, 1] - self.fieldWidth[0, 0],
                         self.size[1] / self.fieldWidth[1, 1] - self.fieldWidth[1, 0])

    def getImgCenter(self):
        return self.size / 2

    def getPixelFromField(self, posInField):
        ratio = self.getRatio()
        offsetField = posInField - self.getFieldCenter()
        offsetPixel = self.getRatio() * offsetField
        # Y axis is inverted to get the Z-axis pointing outside of the screen
        offsetPixel[1] *= -1
        pixel = self.getImgCenter() + offsetPixel
        return [int(pixel[0]), int(pixel[1])]

    def drawNodes(self, screen):
        for node in self.graph.graphDict:
            if isinstance(node, AtkNode):
                pygame.draw.circle(screen, self.atkColor, self.getPixelFromField(
                    (node.pos.x, node.pos.y)), int(self.robotWidth * self.getRatio() / 2))
            else:
                pygame.draw.circle(screen, self.defColor, self.getPixelFromField(
                    (node.pos.x, node.pos.y)), int(self.robotWidth * self.getRatio() / 2))

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

    def draw(self, screen):
        if not self.isNodesOnEdges:
            self.drawEdges(screen)
            self.drawNodes(screen)
        else:
            self.drawNodes(screen)
            self.drawEdges(screen)

    def run(self):
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
            self.draw(screen)
            pygame.display.flip()
