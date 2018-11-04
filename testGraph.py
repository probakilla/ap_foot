import unittest
from graph import Graph
from node import BLACK, AtkNode, DefNode
from algo import searchDominatingSet

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

    def testSearchDominatingSet(self):
        AtkA = AtkNode ((1, 0))
        AtkB = AtkNode ((2, 0))
        AtkC = AtkNode ((3, 0))
        DefA = DefNode ((0, 1))
        DefB = DefNode ((0, 2))
        DefC = DefNode ((0, 3))
        graphDict = {
            AtkA: [DefA, DefB],
            AtkB: [DefA, DefC],
            AtkC: [DefB, DefC],
            DefA: [AtkA, AtkB],
            DefB: [AtkA, AtkC],
            DefC: [AtkB, AtkC]
        }
        g = Graph (graphDict)
        dominatingSet = searchDominatingSet (g, 3)
        expectedDominatingSet = [DefA, DefC] #Can be any couple of defenders
        self.assertEqual (dominatingSet, expectedDominatingSet)

    def testRemainsUndominateAttacker(self):
        return
