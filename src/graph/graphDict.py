''' Graph management module '''


class Goal(object):
    ''' Representation of a goal in field '''

    def __init__(self, leftPost, rightPost, direction):
        self.leftPost = leftPost
        self.rightPost = rightPost
        self.direction = direction


class GraphWithDict(object):
    ''' Representation of a graph with a dictionary '''

    def __init__(self, graphDict=None):
        if graphDict is None:
            graphDict = {}
        self.graphDict = graphDict

    def __str__(self):
        res = ""
        for node in self.graphDict:
            strNode = node.__str__()
            strNode += ": ["
            for neighbourNode in self.graphDict[node]:
                strNode += neighbourNode.__str__()
                strNode += ", "
            strNode += "]\n"
            res += strNode
        return res

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def addListNode(self, listNode):
        ''' Add a list of nodes in the graph '''
        for node in listNode:
            self.addNode(node)

    def addNode(self, node):
        ''' Add a node in the dictionary member '''
        if node not in self.graphDict:
            self.graphDict[node] = []
        else:
            print("node already in graph")
            print(node)

    def removeNode(self, node):
        listNeighbourNode = self.graphDict[node].copy()
        for neighbourNode in listNeighbourNode:
            self.graphDict[node].remove(neighbourNode)
            self.graphDict[neighbourNode].remove(node)
        del self.graphDict[node]

    def removeNodeAndNeighbourhood(self, node):
        listNeighbourNode = self.graphDict[node].copy()
        for neighbourNode in listNeighbourNode:
            self.removeNode(neighbourNode)
        del self.graphDict[node]

    def addEdge(self, node1, node2):
        ''' Add an edge between the two nodes '''
        self.addEdgeBetweenNodes(node1, node2)
        self.addEdgeBetweenNodes(node2, node1)

    def addEdgeBetweenNodes(self, node1, node2):
        ''' Add a node in the neighbourg list of a node '''
        if node1 in self.graphDict:
            if node2 not in self.graphDict[node1]:
                self.graphDict[node1].append(node2)
            else:
                print("node already in neighbourhood")
        else:
            print('node not in graph')


    def listNodes(self):
        ''' Retrieves the list of the nodes, corresponding of all key
        of the dictionary '''
        return list(self.graphDict.keys())

    def getAttacksList(self):
        ''' Retrieves only the keys of the dictionary corresponding of
        an oponent '''
        atkNodes = []
        for node in self.graphDict:
            if node.isAtk():
                atkNodes.append(node)
        return atkNodes

    def getDefendersList(self):
        ''' Retrieves only the keys of the dictionary corresponding of
        a defender '''
        defNodes = []
        for node in self.graphDict:
            if not node.isAtk():
                defNodes.append(node)
        return defNodes

    def getDefenderMaxDegree(self, markedNodeSet = set()):
        ''' Retrives the defender with the maximum degrees '''
        maxDegree = 0
        nodeMaxDegree = None
        for node in self.graphDict:
            if not node.isAtk() and node not in markedNodeSet:
                nodeDegree = len(self.graphDict[node])
                if  (nodeDegree > maxDegree):
                    maxDegree = nodeDegree
                    nodeMaxDegree = node
        return nodeMaxDegree


    def getNeighbourhood(self, node):
        return self.graphDict[node]

    def listEdges(self):
        ''' Retrieves a list of all edges in the graph '''
        listEdges = []
        for node in self.graphDict:
            for edge in self.graphDict[node]:
                listEdges.append((node, edge))
        return listEdges

    def copy(self):
        graphDict = self.graphDict.copy()
        for key in graphDict:
            graphDict[key] = graphDict[key][:]
        return GraphWithDict(graphDict)
