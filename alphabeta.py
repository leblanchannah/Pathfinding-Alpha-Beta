# Assignment 2 - Pathfinding and Alpha-Beta Pruning - CISC 352
# Spencer Edwards - 13srte
# Hannah LeBlanc - 12hml4

#
# “I confirm that this submission is my own work and is consistent with
# the Queen's regulations on Academic Integrity.”
#

import sys

# A class used to create and traverse a graph using the MiniMax algorithm combined
# with alpha-beta pruning, given specifically formatted sets of nodes and edges.
class Graph:
    # Class constructor
    # nodesInput is a string that is just the untouched line of the nodes set read from the file
    # edgesInput is a string that is just the untouched line of the edges set read from the file
    def __init__(self, nodesInput, edgesInput):
        self.root = None
        self.numLeavesExamined = 0          # Counter for number of leaf nodes examined
        self.nodes = self.parseNodes(nodesInput)     # dictionary where the key is the node (ie. "A"), and the value is "MIN" or "MAX"
        self.edges = self.parseEdges(edgesInput)     # dictionary of lists representing edges
        self.score = self.alphaBeta(self.root, -sys.maxsize-1, sys.maxsize)

    # A function that takes the string of the nodes set read from the file
    # Parses the string and forms a dictionary of nodes
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
        return nodes

    # A function that takes the string of the edges set read from the file
    # Parses the string and forms a dictionary of edges
    def parseEdges(self, edgesInput):
        edges = {}
        edgesList = edgesInput.split("),")
        for edge in edgesList:
            temp = edge.split(",")
            node1 = temp[0].split("(")[1]
            node2 = temp[1].split(")")[0]
            edges.setdefault(node1,[]).append(node2)
        return edges

    # Function that traverses the graph using the MiniMax algorithm in tandem with
    # alpha-beta pruning.
    def alphaBeta(self, current, alpha, beta):
        currentMinMax = self.nodes[current]     # Is current node min or max
        currentEdges = self.edges[current]      # List of children of current node
        isMax = False                           # False is MIN, True is MAX
        if currentMinMax == 'MAX':
            isMax = True
        hasLeaves = self.hasLeaves(currentEdges)    # True means current node has leaves for children
        if hasLeaves:
            # Cast leaves to integers (leaves are integer values but represented as strings)
            leaves = [int(x) for x in currentEdges if x.isdigit() and x is not None]
            if isMax:
                # MAX node
                max = 0
                for leaf in leaves:
                    self.numLeavesExamined += 1
                    if leaf > beta:
                        # Cut-off search
                        self.edges[current] = []
                        return beta
                    if leaf > max:
                        max = leaf
                return max
            else:
                # MIN node
                min = sys.maxsize
                for leaf in leaves:
                    self.numLeavesExamined += 1
                    if leaf < alpha:
                        # Cut-off search
                        self.edges[current] = []
                        return alpha
                    if leaf < min:
                        min = leaf
                return min
        if isMax:
            # MAX node
            # Recursively call alphaBeta search on all children of current node
            for child in currentEdges:
                value = self.alphaBeta(child, alpha, beta)
                if value > alpha:
                    alpha = value
                if alpha >= beta:
                    # Cut-off search below current node
                    self.edges[current] = []
                    return alpha
            return alpha
        else:
            # MIN node
            for child in currentEdges:
                # Recursively call alphaBeta search on all children of current node
                value = self.alphaBeta(child, alpha, beta)
                if value < beta:
                    beta = value
                if alpha >= beta:
                    # Cut-off search below current node
                    self.edges[current] = []
                    return beta
            return beta

    # Helper function that returns True if a node has one or more leaves as children,
    # False if it does not
    def hasLeaves(self, edges):
        for child in edges:
            if child.isdigit():
                return True
        return False

# Function that reads in graphs from a file, and writes output to a file
# Creates a Graph class for each graph and extracts relevant information
def solvePrunes():
    f = open("alphabeta.txt", "r")
    out = open("alphabeta_out.txt", "w")
    graphNumber = 0
    for line in f:
        if line == '\n':
            continue
        graphNumber += 1
        parts = line.split(" ")
        nodes = parts[0]
        edges = parts[1]
        g = Graph(nodes, edges)
        s = "Graph " + str(graphNumber) + ": Score: " + str(g.score) + "; Leaf Nodes Examined: "\
            + str(g.numLeavesExamined) + "\n"
        out.write(s)
    f.close()
    out.close()

# Runs the show
def main():
    solvePrunes()

main()