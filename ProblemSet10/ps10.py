# 6.00x Problem Set 10
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Read each line from mit_map.txt
# add Nodes and Edge according each line

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    f = open(mapFilename)
    g = WeightedDigraph()
    nodes = []
    for line in f:
        n, dest, distance, outdoor = line.split()
        nn = Node(str(n))
        ndest = Node(str(dest))
        if nn not in nodes:
            nodes.append(nn)
            g.addNode(nn)
        if ndest not in nodes:
            nodes.append(ndest)
            g.addNode(ndest)
        g.addEdge(WeightedEdge(nn, ndest, distance, outdoor))
    return g
        
"""
mitMap = load_map("mit_map.txt")
print mitMap
print isinstance(mitMap, Digraph)
print isinstance(mitMap, WeightedDigraph)
g = open('outputGraph.txt', 'w')
g.write(str(mitMap.nodes))
g.write('\n')
g.write(str(mitMap.edges))
g.close()
"""


#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# Find all paths from start to end
# and choose the shortest path that also satisfies all contraints
#
def outputPath(nodePath):
    output = []
    for n in nodePath:
        if isinstance(n, Node):
            output.append(str(n.getName()))
        else:
            output.append(n)
    return output


def find_all_paths(digraph, start, end, path=[]):    
    start = Node(start)
    end = Node(end)
    path = path + [start]
    if start == end:
        return [path]

    all_paths = []
    for node in digraph.childrenOf(start):
        if node not in path:
            all_paths += find_all_paths(digraph, node, end, path)

    return all_paths


def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    all_paths = find_all_paths(digraph, start, end, path=[])
    shortest_path = None
    shortest_dist = 0.0
    for path in all_paths:
        totalDist = 0
        totalOutdoor = 0
        for node1, node2 in zip(path[:-1], path[1:]):
            for child_node, (w1, w2) in digraph.edges[node1]:
                if child_node == node2:
                    totalDist += w1
                    totalOutdoor += w2
        if totalDist <= maxTotalDist and totalOutdoor <= maxDistOutdoors:
            if shortest_path is None or totalDist < shortest_dist:
                shortest_path = path
                shortest_dist = totalDist
    if shortest_path is not None:
        return outputPath(shortest_path)
    raise ValueError


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
class ShortestPath(object):
    def __init__(self, path, dist, distOutdoor):
        self.path = path
        self.dist = dist
        self.distOutdoor = distOutdoor
    def getPath(self):
        return self.path
    def getDist(self):
        return self.dist
    def getDistOutdoor(self):
        return self.distOutdoor

shortest_class = ShortestPath([], 0.0, 0.0)

def DFS(digraph, start, end, maxTotalDist, maxDistOutdoors, path=[], totalDist = 0.0, totalOutdoor = 0.0):    
    start = Node(start)
    end = Node(end)
    path = path + [start]
    print path
    if start == end:
        return path

    shortest = None
    shortestDist = 0.0
    shortestOutdoor = 0.0
    for node in digraph.childrenOf(start):
        if node not in path:
            newPath = DFS(digraph, node, end, maxTotalDist, maxDistOutdoors, path, totalDist, totalOutdoor)

            if newPath is None:
                continue

            totalDist = 0
            totalOutdoor = 0
            for node1, node2 in zip(newPath[:-1], newPath[1:]):
                for child_node, (w1, w2) in digraph.edges[node1]:
                    if child_node == node2:
                        totalDist += w1
                        totalOutdoor += w2

            if shortest is None or totalDist <= shortestDist:
                if totalDist <= maxTotalDist and totalOutdoor <= maxDistOutdoors:
                    shortest = newPath
                    shortestDist = totalDist
                    shortestOutdoor = totalOutdoor
    shortest_class = ShortestPath(shortest, shortestDist, shortestOutdoor)
    return shortest_class.getPath()


def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    result = DFS(digraph, start, end, maxTotalDist, maxDistOutdoors)
    store_dist = shortest_class.getDist()
    store_distOutdoor = shortest_class.getDistOutdoor()
    if result is not None and store_dist <= maxTotalDist and store_distOutdoor <= maxDistOutdoors:
        return outputPath(result)
    raise ValueError


#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    # Test cases
    mitMap = load_map("mit_map.txt")
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges


    LARGE_DIST = 1000000

    # Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

    # Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

    # Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

    # Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

    # Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

    # Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

    # Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
  
    try:
        directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
  
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    # Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'
  
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr
