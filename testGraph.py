import unittest
import copy
import random
from graph import Graph
from node import BLACK, WHITE, AtkNode, DefNode
from algo import DSAP, remainsUndominateAttacker

XMINPOS = -10.0
XMAXPOS = 10.0
YMAXPOS = 10.0
YMINPOS = -10.0


class TestGraphMethods(unittest.TestCase):

    def buildRandomGraph(self, lenght, nbMaxNeighboor):
        g = Graph()
        nbAtk = random.randint(1, lenght)
        nbDef = lenght - nbAtk
        for i in range(nbAtk):
            pos = (random.uniform(XMINPOS, XMAXPOS),
                   random.uniform(YMINPOS, YMAXPOS))
            angle = random.uniform(0.0, 360.0)
            node = AtkNode(pos, angle)
            g.addNode(node)
        for j in range(nbDef):
            pos = (random.uniform(XMINPOS, XMAXPOS),
                   random.uniform(YMINPOS, YMAXPOS))
            node = DefNode(pos)
            g.addNode(node)
        for node in g.graphDict:
            if g.graphDict[node] == []:
                possibleNeighboor = random.sample(
                    g.graphDict.keys(), random.randint(1, nbMaxNeighboor))
                for neighboor in possibleNeighboor:
                    if neighboor != node:
                        if isinstance(node, AtkNode) and isinstance(neighboor, DefNode):
                            g.addEdge(node, neighboor)
                        if isinstance(node, DefNode):
                            g.addEdge(node, neighboor)
        return g

    def testAddNode(self):
        graphToTest = Graph()
        graphExpected = Graph({"A": []})
        graphToTest.addNode("A")
        self.assertEqual(graphToTest, graphExpected)

    def testAddEdge(self):
        return

    def isDominatingSet(self, graph, dominatingSet):
        graphCpy = copy.deepcopy(graph)
        for node in dominatingSet:
            if node not in graphCpy.graphDict:
                return False
            graphCpy.removeNodeAndWhiteColorNeighboor(node)

        return not remainsUndominateAttacker(graphCpy.graphDict)

    def testRemoveNode(self):
        return

    def testBuildGraph(self):
        return

    def testDSAP(self):
        AtkA = AtkNode((1, 0))
        AtkB = AtkNode((2, 0))
        AtkC = AtkNode((3, 0))
        DefA = DefNode((0, 1))
        DefB = DefNode((0, 2))
        DefC = DefNode((0, 3))
        graphDict = {
            AtkA: [DefA, DefB],
            AtkB: [DefA, DefC],
            DefA: [AtkA, AtkB],
            AtkC: [DefB, DefC],
            DefB: [AtkA, AtkC],
            DefC: [AtkB, AtkC]
        }
        g = Graph(graphDict)
        dominatingSet = DSAP(g, 2, [])
        expectedDominatingSet = [DefA, DefC]  # Can be any couple of defenders
        self.assertEqual(dominatingSet, expectedDominatingSet)

        g.addEdge(DefA, DefB)
        g.addEdge(DefB, DefC)
        g.addEdge(DefA, DefC)
        dominatingSet = DSAP(g, 999, [])
        self.assertIsNone(dominatingSet)

        g = self.buildRandomGraph(60, 20)
        dominatingSet = DSAP(g, 10)
        if dominatingSet is not None:
            self.assertTrue(self.isDominatingSet(g, dominatingSet))

    def testRemainsUndominateAttacker(self):
        return
