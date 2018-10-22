import unittest
from graph import Graph

class TestGraphMethods (unittest.TestCase):
    
    def testAddNode (self):
        graphToTest = Graph ()
        graphExpected = Graph ({"A" : []})
        graphToTest.addNode ("A")
        self.assertEqual (graphToTest, graphExpected)

    def testAddEdge (self):
        return
    
    def testRemoveNode (self):
        return
    
    def testBuildGraph (self):
        return

    def testSearchDominatingSet (self):
        return
    
    def testRemainsUndominateAttacker (self):
        return