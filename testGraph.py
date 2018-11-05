import unittest
import copy
from graph import Graph
from node import BLACK, WHITE, AtkNode, DefNode
from algo import DSAP


class TestGraphMethods(unittest.TestCase):

    def testAddNode(self):
        graphToTest = Graph()
        graphExpected = Graph({"A": []})
        graphToTest.addNode("A")
        self.assertEqual(graphToTest, graphExpected)

    def testAddEdge(self):
        return

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
        dominatingSet = DSAP (g, 2, [])
        expectedDominatingSet = [DefA, DefC] #Can be any couple of defenders
        self.assertEqual (dominatingSet, expectedDominatingSet)

        g.addEdge (DefA, DefB)
        g.addEdge (DefB, DefC)
        g.addEdge (DefA, DefC)

        dominatingSet = DSAP (g, 2, [])
        self.assertIsNone (dominatingSet)

    def testRemainsUndominateAttacker(self):
        return
