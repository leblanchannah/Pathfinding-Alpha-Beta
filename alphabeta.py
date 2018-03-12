
import math
import sys

class Graph:
    def __init__(self, nodesInput, edgesInput):
        self.root = None
        self.numLeavesExamined = 0
        self.nodes = self.parseNodes(nodesInput)     # dictionary where the key is the node (ie. "A"), and the value is "MIN" or "MAX"
        self.edges = self.parseEdges(edgesInput)     # dictionary of lists representing edges
        self.score = self.alphaBeta(self.root, -sys.maxsize-1, sys.maxsize)
        print("Score: " + str(self.score) + "; Leaf Nodes Examined: " + str(self.numLeavesExamined))

    def parseNodes(self, nodesInput):
        nodes = {}
        nodesList = nodesInput.split("),")
        i = 0
        for node in nodesList:
            temp = node.split(",")
            letter = temp[0].split("(")[1]
            minMax = temp[1].split(")")[0]
            nodes[letter] = minMax
            if i == 0:
                self.root = letter
            i += 1
        print(nodes)
        return nodes

    def parseEdges(self, edgesInput):
        edges = {}
        edgesList = edgesInput.split("),")
        for edge in edgesList:
            temp = edge.split(",")
            node1 = temp[0].split("(")[1]
            node2 = temp[1].split(")")[0]
            edges.setdefault(node1,[]).append(node2)
        print(edges)
        return edges

    def alphaBeta(self, current, alpha, beta):
        currentMinMax = self.nodes[current]
        currentEdges = self.edges[current]
        print(current)
        #print(currentMinMax)
        #print(currentEdges)
        isMax = False                       # MIN
        if currentMinMax == 'MAX':
            isMax = True
        hasLeaves = self.hasLeaves(currentEdges)
        if hasLeaves:
            leaves = [int(x) for x in currentEdges if x.isdigit() and x is not None]
            if isMax:
                max = 0
                for leaf in leaves:
                    self.numLeavesExamined += 1
                    if leaf > beta:
                        self.edges[current] = []
                        return beta
                    if leaf > max:
                        max = leaf
                return max
            else:
                min = sys.maxsize
                for leaf in leaves:
                    self.numLeavesExamined += 1
                    if leaf < alpha:
                        self.edges[current] = []
                        return alpha
                    if leaf < min:
                        min = leaf
                return min
        if isMax:
            for child in currentEdges:
                #print(child)
                value = self.alphaBeta(child, alpha, beta)
                if value > alpha:
                    alpha = value
                if alpha >= beta:
                    self.edges[current] = []
                    return alpha
            return alpha
        else:
            for child in currentEdges:
                value = self.alphaBeta(child, alpha, beta)
                if value < beta:
                    beta = value
                if alpha >= beta:
                    self.edges[current] = []
                    return beta
            return beta

    def hasLeaves(self, edges):
        for child in edges:
            if child.isdigit():
                return True
        return False

def main():
    nodes = "{(A,MAX),(B,MIN),(C,MIN),(D,MAX),(E,MAX),(F,MAX),(G,MAX)}"
    edges = "{(A,B),(A,C),(B,D),(B,E),(C,F),(C,G),(D,4),(D,3),(E,2),(E,7),(F,3),(F,2),(G,2),(G,8)}"
    g = Graph(nodes, edges)

main()