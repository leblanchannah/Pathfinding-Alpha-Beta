


class Graph:
    def __init__(self, nodesInput, edgesInput):
        self.nodes = self.parseNodes(nodesInput)     # dictionary where the key is the node (ie. "A"), and the value is "MIN" or "MAX"
        self.edges = self.parseEdges(edgesInput)     # set of tuples representing edges

    def parseNodes(self, nodesInput):
        nodes = {}
        nodesList = nodesInput.split("),")
        for node in nodesList:
            temp = node.split(",")
            letter = temp[0].split("(")[1]
            minMax = temp[1].split(")")[0]
            nodes[letter] = minMax
        return nodes

    def parseEdges(self, edgesInput):
        edges = set()
        edgesList = edgesInput.split("),")
        for edge in edgesList:
            temp = edge.split(",")
            node1 = temp[0].split("(")[1]
            node2 = temp[1].split(")")[0]
            edges.add((node1, node2))
        return edges




def main():
    nodes = "{(A,MAX),(B,MIN),(C,MIN),(D,MAX),(E,MAX),(F,MAX),(G,MAX)}"
    edges = "{(A,B),(A,C),(B,D),(B,E),(C,F),(C,G),(D,4),(D,3),(E,2),(E,7),(F,3),(F,2),(G,2),(G,8)}"
    g = Graph(nodes, edges)

main()