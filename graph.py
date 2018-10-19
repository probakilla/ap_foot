import json

from node import Node, Point


class Goal:
    def __init__(self, leftPost, rightPost, direction):
        self.leftPost = leftPost
        self.rightPost = rightPost
        self.direction = direction


def buildGraph(file):
    jsonData = parseFile(file)
    return graph


def parseFile(file):
    jsonFile = open(file)
    data = json.load(jsonFile)
    jsonFile.close()
    return data
