#Michael Lawrence

import math

class Vertex:

    def __init__(self, name):
        self.name = name
        self.adjacent = {}
        self.prev = None
        self.distance = math.inf

    def addAdjacent(self, name, weight):
        self.adjacent[name] = weight
    
    def getAdjacent(self):
        return self.adjacent

    def setDistance(self, number):
        self.distance = number

    def getDistance(self):
        return self.distance

    def setPrevious(self, Vertex):
        self.prev = Vertex

    def getPrevious(self):
        return self.prev

    def getName(self):
        return self.name

    def getWeight(self, key):
        return self.adjacent[key]

    def printSelf(self):
        print(self.name)
        print(self.adjacent)


class Graph:

    def __init__(self):
        self.numV = 0
        self.vertices = {}

    def buildVertices(self):
        fin = open("cities.txt")
        line = fin.readline()
        while(line):
            self.numV += 1
            line = line[0:len(line) - 1]
            newVertex = Vertex(line)
            self.vertices[line] = newVertex
            line = fin.readline()

    def buildAdjacent(self):
        fin = open("routes.txt")
        line = fin.readline()
        while(line):
            line = line[1:len(line) - 2]
            city1, city2, weight = line.split(',')
            city1 = city1.strip()
            city2 = city2.strip()
            weight = weight.strip()
            self.vertices[city1].addAdjacent(city2, float(weight)) 
            self.vertices[city2].addAdjacent(city1, float(weight))
            line = fin.readline()

    def printVertices(self):
        for keys in self.vertices:
            self.vertices[keys].printSelf()

            

    def buildPair(self):
        #builds a list of pairs
        #this list will be sorted.
        fin = open("routes.txt")
        line = fin.readline()
        pairs = []
        while(line):
            #reads the pairs in from the file
            line = line[1:len(line) - 2]
            city1, city2, weight = line.split(',')
            city1 = city1.strip()
            city2 = city2.strip()
            weight = weight.strip()
            newPair = vertexPair(city1, city2, weight)
            pairs.append(newPair) 
            line = fin.readline()
        return pairs

    def add(self, city1, city2, weight):
        #adds a new vertex pair to a graph.
        newVertex = Vertex(city1)
        self.vertices[city1] = newVertex
        self.vertices[city1].addAdjacent(city2, weight)

    def Kruskal(self):
        #make a new graph for our MST
        minSpan = Graph()
        total = 0
        #make our disjoint sets
        sets = UnionFind()
        sets.build(self.vertices)
        #build a list of pairs in the old graph
        pairs = self.buildPair()
        #sort the vertex pairs
        pairs.sort(key = lambda x: float(x.weight), reverse = False)
        #now that the vertex pairs are sorted, we can simply
        #iterate through them least to greatest.
        for i in range(0, len(pairs)):
            root1 = sets.find(pairs[i].city1)
            root2 = sets.find(pairs[i].city2)
            #find the roots of the two disjoint sets
            if(root1 != root2):
                #if they are in different sets we can union them
                minSpan.add(pairs[i].city1, pairs[i].city2, pairs[i].weight)
                total += float(pairs[i].weight)
                sets.union(pairs[i].city1, pairs[i].city2)
        #print tree and distance
        minSpan.printVertices()
        print("The total distance is: {}".format(total))


class UnionFind:

    def __init__(self):
        #initialize map
        self.trees = {}
        self.children = {}

    def build(self, vertices):
        #set all roots to null
        for keys in vertices:
            self.trees[keys] = None
        #everthing is a root
        #roots have no children
        for keys in self.trees:
            self.children[keys] = []

    def find(self, start):
        #each node maps to its root
        #return the root
        if(self.trees[start] != None):
            return self.trees[start]
        else:
            return star

    def union(self, node1, node2):
        #get the 2 roots
        #based on starting pos
        if(self.trees[node1] == None):
            root1 = node1
            if(self.trees[node2] == None):
                root2 = node2
            else:
                root2 = self.trees[node2]
        elif(self.trees[node2] == None):
            root2 = node2
            if(self.trees[node1] == None):
                root1 = node1
            else:
                root1 = self.trees[node1]
        else:
            root1 = self.trees[node1]
            root2 = self.trees[node2]
        #move root and all its children
        #over to the new set
        self.trees[root2] = root1
        self.children[root1].append(root2)
        children = self.children[root2]
        for i in range (0, len(children)):
            self.children[root1].append(children[i])
            self.trees[children[i]] = root1
        self.children[root2].clear()


class vertexPair():
    #holds a pair of vertices
    def __init__(self, city1, city2, weight):
        self.city1 = city1
        self.city2 = city2
        self.weight = weight


if __name__ == '__main__':
    cities = Graph()
    cities.buildVertices()
    cities.Kruskal()
