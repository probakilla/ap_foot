import json

from node import Node, Point


def buildGraph(file):
    jsonData = open(file)
    data = json.load(jsonData)
    graph = {}
    for opp in data["opponents"]:
        opp = ""
    jsonData.close()
    return graph
