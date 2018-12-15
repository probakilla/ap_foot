''' Graph with an adjacency matrix '''


class GraphAdjacency(object):
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
            for indexNeighbour in range(len(self.adjacencyMatrix[indexNode])):
                if self.adjacencyMatrix[indexNode][indexNeighbour]:
                    strNode += self.listNode[indexNeighbour].__str__()
            strNode += "]\n"
        return strNode

    def getListNode(self):
        """
            Ensure that this graph has same methods than graphDict
        """
        return self.listNode

    def getAttacksList(self):
        """
            Retrieves only the ofenders from the list
        """
        res = list()
        for i in self.listIndexAtk:
            res.append(self.listNode[i])
        return res

    def getDefendersList(self):
        """
            Retrieves only the defenders from the list
        """
        res = list(self.listNode)
        for i in self.listIndexAtk[::-1]:
            del res[i]
        return res

    # Bien trop lent
    def getNeighbourhood(self, node):
        listNeighbourNode = list()
        indexNode = self.listNode.index(node)
        for indexNeighbourNode in self.adjacencyMatrix[indexNode]:
            if self.adjacencyMatrix[indexNode][indexNeighbourNode]:
                listNeighbourNode.append(self.listNode[indexNeighbourNode])
        return listNeighbourNode

    def addNode(self, node):
        ''' Append a node in the list '''
        self.listNode.append(node)
        for i in self.adjacencyMatrix:
            i.append(False)
        boolList = [False] * (len(self.adjacencyMatrix) + 1)
        self.adjacencyMatrix.append(boolList)
        if node.isAtk():
            self.listIndexAtk.append(len(self.listNode))

    def addEdge(self, node1, node2):
        ''' Set the correct boolean in the matrix to true '''
        indexNode1 = self.listNode.index(node1)
        indexNode2 = self.listNode.index(node2)
        self.adjacencyMatrix[indexNode1][indexNode2] = True
        self.adjacencyMatrix[indexNode2][indexNode1] = True
