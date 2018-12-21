import json

from graph.node import Node

JSON_EXT = ".json"


def parseFile(file):
    with open(file, 'r') as jsonFile:
        data = json.load(jsonFile)
    return data


def graphToJson(graph, fileName):
    if not fileName[-5:] == JSON_EXT:
        raise Exception(fileName + " is not a json file !")
    with open(fileName, 'w') as jsonFile:
        data = {"DominatingSet": []}
        encoder = NodeEncoder()
        for node in graph:
            data["DominatingSet"].append(encoder.encode(node))
        json.dump(data, jsonFile)


class NodeEncoder(json.JSONEncoder):
    def default(self, node):
        if isinstance(node, Node):
            return [node.pos[0], node.pos[1]]
        else:
            super().default(self, node)
