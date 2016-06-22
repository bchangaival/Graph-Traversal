from networkx import *
import matplotlib.pyplot as plt
import random as ran

class Agent(object):
    def __init__(self, position, agentID = 0):
        self.position = position
        self.agentID = agentID
    def getPosition(self):
        return self.position
    def neighborMove(self, neighborList, graph):
        pass
    def randomMove(self):
        pass
    def leavePheromone(self):
        pass
    def choosePath(self):
        pass
    def antInteract(self, graph, newClusterList, currentClusterList, agentList):
        pass
    
def calculateModularity():
    pass

def humannetGraphParsing():
    #create the empty graph
    humanNet = Graph()
    #read the node content
    nodeContent = open("nodes.txt", "r").readlines()
    nodesGeneID = dict((key, None) for key in range(len(nodeContent)))
    nodesSymbol = dict((key, None) for key in range(len(nodeContent)))
    nodeID = [n for n in range(len(nodeContent))]
    for line in nodeContent:
        tempLine = line.split('\t')
        nodesGeneID[int(tempLine[0])] = tempLine[1]
        nodesSymbol[int(tempLine[0])] = tempLine[2]
    humanNet.add_nodes_from(nodeID)
    set_node_attributes(humanNet, 'GENEID', nodesGeneID)
    set_node_attributes(humanNet, 'GENESYMBOL', nodesSymbol)
    #read the edge content
    edgeContent = open("edges.txt","r").readlines()
    for line in edgeContent:
        tempLine = line.split('\t')
        humanNet.add_edge(int(tempLine[1]), int(tempLine[2]))
    return humanNet
    
def testSmallWorldProperty(graph):
    averageDegree = (2*(number_of_edges(graph)))/number_of_nodes(graph)
    nodeNumber = number_of_nodes(graph)
    print "Original Graph APL: ", average_shortest_path_length(graph)
    print "Original Graph CC: ", average_clustering(graph)
    
    totalLength = 0
    randomGraphCC = 0
    iteration  = 30
    for i in range(iteration):
        print "Iteration: ",i
        randomGraph = watts_strogatz_graph(nodeNumber, averageDegree, 1)
        totalLength += average_shortest_path_length(randomGraph)
        randomGraphCC += average_clustering(randomGraph)
    print "random Graph APL: ", totalLength/float(iteration)
    print "Random Graph CC: ", randomGraphCC/float(iteration)

def extractLargestGraph(graph):
    subgraphs = []
    largestGraph = graph
    if not is_connected(graph):
        subgraphs = connected_component_subgraphs(graph)
        largestGraph = subgraphs[0]
        for graph in subgraphs:
            if number_of_nodes(graph) > number_of_nodes(largestGraph):
                largestGraph = graph
    return largestGraph
    
def drawgraph(graph):
    draw_networkx(graph, pos = spring_layout(graph))
    plt.show()

def generateAgent(nodeNumber, agentList, agentNumber):
    clusterID = 0
    duplicateCount = 0
    for i in range(agentNumber):
        duplicate = True
        while duplicate == True:
            duplicateCount = 0
            randomIndex = ran.randint(0, nodeNumber-1)
            for item in agentList:
                if randomIndex == item.getPosition():
                    duplicateCount += 1
            if duplicateCount == 0:
                agent = Agent(randomIndex,clusterID)
                agentList.append(agent)
                duplicate = False
                if i < int(math.ceil(nodeNumber*0.2)) -1:
                    clusterID += 1

if __name__ == "__main__":
    # Parsing Graphs
    humanGraph = humannetGraphParsing()
    interestedGraph = extractLargestGraph(humanGraph)
    
    #check if the Graph has small world property
    # testSmallWorldProperty(interestedGraph)
    
    #initialize the agent
    nodeNumber = number_of_nodes(interestedGraph)
    agentNumber = 50
    agentList = []
    generateAgent(nodeNumber, agentList, agentNumber)
    
    
    