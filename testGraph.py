import unittest
import copy
import random
from graph import GraphWithDict
from node import Node
from algo import remainsUndominatedAttacker, minDominatingSet

XMINPOS = -10.0
XMAXPOS = 10.0
YMAXPOS = 10.0
YMINPOS = -10.0


class TestGraphMethods(unittest.TestCase):

    def buildRandomGraph(self, lenght, nbMaxNeighboor):
        g = GraphWithDict()
        nbAtk = random.randint(1, lenght)
        nbDef = lenght - nbAtk
        for i in range(nbAtk):
            pos = (random.uniform(XMINPOS, XMAXPOS),
                   random.uniform(YMINPOS, YMAXPOS))
            angle = random.uniform(0.0, 360.0)
            node = Node(pos, angle)
            g.addNode(node)
        for j in range(nbDef):
            pos = (random.uniform(XMINPOS, XMAXPOS),
                   random.uniform(YMINPOS, YMAXPOS))
            node = Node(pos)
            g.addNode(node)
        for node in g.graphDict:
            if g.graphDict[node] == []:
                possibleNeighboor = random.sample(
                    g.graphDict.keys(), random.randint(1, nbMaxNeighboor))
                for neighboor in possibleNeighboor:
                    if neighboor != node:
                        if isinstance(node, Node) and isinstance(neighboor, Node):
                            g.addEdge(node, neighboor)
                        if isinstance(node, Node):
                            g.addEdge(node, neighboor)
        return g

    def testAddNode(self):
        graphToTest = GraphWithDict()
        graphExpected = GraphWithDict({"A": []})
        graphToTest.addNode("A")
        self.assertEqual(graphToTest, graphExpected)

    def testAddEdge(self):
        return

    def isDominatingSet(self, graph, dominatingSet):
        return not remainsUndominatedAttacker(graph.graphDict, dominatingSet)

    def testRemoveNode(self):
        return

    def testBuildGraph(self):
        return

    def testMinDominatingSet(self):
        AtkA = Node((1, 0), 0.42)
        AtkB = Node((2, 0), 0.69)
        AtkC = Node((3, 0), 0.45)
        DefA = Node((0, 1))
        DefB = Node((0, 2))
        DefC = Node((0, 3))
        graphDict = {
            AtkA: [DefA, DefB],
            AtkB: [DefA, DefC],
            DefA: [AtkA, AtkB],
            AtkC: [DefB, DefC],
            DefB: [AtkA, AtkC],
            DefC: [AtkB, AtkC]
        }
        g = GraphWithDict(graphDict)
        dominatingSet = minDominatingSet(g, 2)
        expectedDominatingSet = {DefA, DefC}  # Can be any couple of defenders
        self.assertEqual(dominatingSet, expectedDominatingSet)

        g.addEdge(DefA, DefB)
        g.addEdge(DefB, DefC)
        g.addEdge(DefA, DefC)
        
        dominatingSet = minDominatingSet(g, 999)
        self.assertIsNone(dominatingSet)
        
        g = self.buildRandomGraph(60, 20)
        dominatingSet = minDominatingSet(g, 10)
        if dominatingSet is not None:
            self.assertTrue(self.isDominatingSet(g, dominatingSet))

    def testRemainsUndominateAttacker(self):
        return
