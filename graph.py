class Goal:
    def __init__(self, leftPost, rightPost, direction):
        self.leftPost = leftPost
        self.rightPost = rightPost
        self.direction = direction


class GraphWithDict:
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
        #     if node in self.graphDict:
        #         raise ValueError("NODE %s ALREADY IN GRAPH !!" % (node))
        if node not in self.graphDict:
            self.graphDict[node] = []

    def addEdge(self, node1, node2):
        self.addEdgeBetweenNodes(node1, node2)
        self.addEdgeBetweenNodes(node2, node1)

    def addEdgeBetweenNodes(self, node1, node2):
        if node1 in self.graphDict:
            if node2 not in self.graphDict[node1]:
                self.graphDict[node1].append(node2)
        else:
            self.graphDict[node1] = [node2]

    def listNodes(self):
        return list(self.graphDict.keys())

    def getAtkNodes(self):
        atkNodes = []
        for node in self.graphDict:
            if node.isAtk():
                atkNodes.append(node)
        return atkNodes

    def getDefNodes(self):
        defNodes = []
        for node in self.graphDict:
            if not node.isAtk():
                defNodes.append(node)
        return defNodes

    def listEdges(self):
        listEdges = []
        for node in self.graphDict:
            for edge in self.graphDict[node]:
                listEdges.append((node, edge))
        return listEdges

class GraphWithAdjencyMatrix:
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
        return self.listNode

    def getAdjacencyMatrix(self):
        return self.adjacencyMatrix

    def getListAtkNodes(self):
        res = list()
        for i in self.listIndexAtk:
            res.append(self.listNode[i])
        return res

    def getListDefNodes(self):
        res = self.listNode
        for i in self.listIndexAtk:
            del res[i]
        return res

    def addAtk(self, node):
        self.listIndexAtk.append(len(self.listNode))
        self.addNode(node)

    def addNode(self, node):
        self.listNode.append(node)
        for i in self.adjacencyMatrix:
            i.append(False)
        boolList = [False] * (len(self.adjacencyMatrix) + 1)
        self.adjacencyMatrix.append(boolList)

    def addEdge(self, node1, node2):
        indexNode1 = self.listNode.index(node1)
        indexNode2 = self.listNode.index(node2)
        self.adjacencyMatrix[indexNode1][indexNode2] = True
