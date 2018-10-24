import json

from node import DefNode, AtkNode

JSON_EXT = ".json"


def parseFile(file):
    with open(file, 'r') as jsonFile:
        data = json.load(jsonFile)
    return data


def graphToJson(graph, fileName):
    if not isinstance(graph, dict):
        raise Exception("Not a graph !")
    if not fileName[-5:] == JSON_EXT:
        raise Exception(fileName + " is not a json file !")
    with open(fileName, 'w') as jsonFile:
        data = {"Posisions": []}
        encoder = NodeEncoder()
        for node in graph:
            data["Posisions"].append(encoder.encode(node))
        json.dump(data, jsonFile)


class NodeEncoder(json.JSONEncoder):
    def default(self, node):
        if isinstance(node, AtkNode) or isinstance(node, DefNode):
            return [node.pos.x, node.pos.y]
        else:
            super().default(self, node)
