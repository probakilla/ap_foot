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
            for neighboorNode in self.graphDict[node]:
                strNode += neighboorNode.__str__()
                strNode += ", "
            strNode += "]\n"
            res += strNode
        return res

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def addNode(self, node):
        ''' Add a node in the dictionary member '''
        if node not in self.graphDict:
            self.graphDict[node] = []

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
            self.graphDict[node1] = [node2]

    def listNodes(self):
        ''' Retrieves the list of the nodes, corresponding of all key
        of the dictionary '''
        return list(self.graphDict.keys())

    def getAtkNodes(self):
        ''' Retrieves only the keys of the dictionary corresponding of
        an oponent '''
        atkNodes = []
        for node in self.graphDict:
            if node.isAtk():
                atkNodes.append(node)
        return atkNodes

    def getDefNodes(self):
        ''' Retrieves only the keys of the dictionary corresponding of
        a defender '''
        defNodes = []
        for node in self.graphDict:
            if not node.isAtk():
                defNodes.append(node)
        return defNodes

    def listEdges(self):
        ''' Retrieves a list of all edges in the graph '''
        listEdges = []
        for node in self.graphDict:
            for edge in self.graphDict[node]:
                listEdges.append((node, edge))
        return listEdges


class GraphWithAdjacencyMatrix(object):
    ''' A representation of a graph with a list of nodes and a two
    dimension list of booleans representing a adjacency matrix '''
    def __init__(self):
        self.listNode = list()
        self.listIndexAtk = list()
        self.adjacencyMatrix = list(list())

    def __str__(self):
        strNode = ""
        for indexNode in range(len(self.listNode)):
            strNode += self.listNode[indexNode].__str__()
            strNode += ": ["
            for indexNeighboor in range(len(self.adjacencyMatrix[indexNode])):
                if self.adjacencyMatrix[indexNode][indexNeighboor]:
                    strNode += self.listNode[indexNeighboor].__str__()
            strNode += "]\n"
        return strNode

    def getListNode(self):
        ''' getter on listNode '''
        return self.listNode

    def getAdjacencyMatrix(self):
        ''' Getter on the matrix '''
        return self.adjacencyMatrix

    def getListAtkNodes(self):
        ''' Retrieves a list containing only the oponents '''
        res = list()
        for i in self.listIndexAtk:
            res.append(self.listNode[i])
        return res

    def getListDefNodes(self):
        ''' Retrieves a list containing only the defenders '''
        res = self.listNode
        for i in self.listIndexAtk:
            del res[i]
        return res

    def addAtk(self, node):
        ''' Add a node in the list and its corresponding index in a list
        used to find him in the list '''
        self.listIndexAtk.append(len(self.listNode))
        self.addNode(node)

    def addNode(self, node):
        ''' Append a node in the list '''
        self.listNode.append(node)
        for i in self.adjacencyMatrix:
            i.append(False)
        boolList = [False] * (len(self.adjacencyMatrix) + 1)
        self.adjacencyMatrix.append(boolList)

    def addEdge(self, node1, node2):
        ''' Set the correct boolean in the matrix to true '''
        indexNode1 = self.listNode.index(node1)
        indexNode2 = self.listNode.index(node2)
        self.adjacencyMatrix[indexNode1][indexNode2] = True