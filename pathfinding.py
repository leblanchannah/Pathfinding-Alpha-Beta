###Pathfinding###

import copy
from math import sqrt
 #Greedy algorithm

def solveGrids(inFile, outFile, mode):
    #each grid is separated by an empty line
    #read in problems one by one
    #as reading input, note goal=G and start=S
    f = open(inFile,"r")
    out = open(outFile,"w") 
    count = 0
    grid = []
    start = ()
    goal = () 
    for line in f:
        if line in ('\n'):
            if grid != []:
                soln = GridMap(grid,start,goal,mode)
                out.write("Greedy\n")
                for i in range(len(soln.greedy)):
                    for j in range(len(soln.greedy[0])):
                        out.write(soln.greedy[i][j] + "")
                    out.write("\n")
                out.write("A*\n")
                for i in range(len(soln.astar)):
                    for j in range(len(soln.astar[0])):
                        out.write(soln.astar[i][j] + "")
                    out.write("\n")

            grid = []
            start = ()
            goal = ()
            count = 0
        else:
            row = list(line) # parse row into a list
            elements = len(row)
            grid.append(row[:elements-1]) #removing end \n char
            for section in range(elements): # for square in row 
                if row[section] == 'G':
                    goal = (count,section)
                elif row[section] == 'S':
                    start = (count,section)
            count += 1
    if grid != []:
        soln = GridMap(grid,start,goal,mode)
        out.write("Greedy\n")
        for i in range(len(soln.greedy)):
            for j in range(len(soln.greedy[0])):
                out.write(soln.greedy[i][j] + "")
            out.write("\n")
        out.write("A*\n")
        for i in range(len(soln.astar)):
            for j in range(len(soln.astar[0])):
                out.write(soln.astar[i][j] + "")
            out.write("\n")
    f.close()
    out.close()




class GridMap:
    def __init__(self,grid,start,goal,mode):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.columns = len(grid[0])
  
        ## up,down,right,left moves allowed - mode A
        if mode == 'a':
            self.mode = 'A'
        else:
            self.mode = 'B'
        self.path = self.greedySearch()
        self.greedy = self.editGraph()
        self.path = self.aStarSearch()
        self.astar = self.editGraph()
        return None

    #editGraphs adds solution to grid, uses 'P' to show path
    #returns grid
    def editGraph(self):
        # deep copy to clone 2d lists
        temp_grid = copy.deepcopy(self.grid)
        temp_path = copy.deepcopy(self.path)
        temp_path.remove(self.goal)
        temp_path.remove(self.start)
        for move in temp_path:
            temp_grid[move[0]][move[1]] = 'P'
        return temp_grid

    #neighbours determines the possible moves for the search 
    def neighbors(self,current):
        row = current[1][0]
        col = current[1][1]
        around = []
        if col != 0: #left move allowed
            if self.grid[row][col-1] != 'X':
                around.append((row,col-1))
        if col != self.columns: #right move allowed
            if self.grid[row][col+1] != 'X':
                around.append((row,col+1))
        if row != 0: #up move allowed
            if self.grid[row-1][col] != 'X':
                around.append((row-1,col))
            if self.mode == 'B' and col != 0:
                if self.grid[row-1][col-1] != 'X':
                    around.append((row-1,col-1))
            if self.mode == 'B' and col != self.columns:
                if self.grid[row-1][col+1] != 'X':
                    around.append((row-1,col+1))
        if row != self.rows:  #down move allowed
            if self.grid[row+1][col] != 'X':
                around.append((row+1,col))
            if self.mode == 'B' and col != 0:
                if self.grid[row+1][col-1] != 'X':
                    around.append((row+1,col-1))
            if self.mode == 'B' and col != self.columns:
                if self.grid[row+1][col+1] != 'X':
                    around.append((row+1,col+1))
        
        #returns list of tuples (row,col) of legal moves 
        return around
        
    # reconstructs path from search
    def greedyReconstruct(self, cameFrom):
        current = self.goal
        path = []
        while current != self.start:
            path.append(current)
            current = cameFrom[current]
        path.append(self.start)
        path.reverse()
        return path

    def greedySearch(self):
        frontier = []
        frontier.insert(0,(0,self.start))
        cameFrom = {}
        cameFrom['S'] = None
        while frontier:
            #heapq.heappop should return the smallest item on the list
            current = frontier.pop(0)
            if current[1] == self.goal:
                break
            for next in self.neighbors(current):
                if next not in cameFrom:
                    priority = self.hFunChebyshev(next,self.goal)
                    frontier.append((priority,next))
                    cameFrom[next] = current[1]
            frontier = sorted(frontier,key=lambda x:x[0])
        path = self.greedyReconstruct(cameFrom)
        return path



    def aStarSearch(self):
        frontier = []
        frontier.insert(0,(0,self.start))
        cameFrom = {}
        csf = {}  #cost so far
        cameFrom['S'] = None
        csf[self.start] = 0
        while frontier:
            current = frontier.pop(0)
            if current[1] == self.goal:
                break 
            for next in self.neighbors(current):
                # new Cost = csf[current] + graph.cost(current,next)
                # all costs are == 1
                newCost = csf[current[1]] + 1
                if next not in csf or newCost < csf[next]:
                    csf[next] = newCost
                    priority = newCost + self.hFunChebyshev(next,self.goal)
                    frontier.append((priority,next))
                    cameFrom[next] = current[1]
            frontier = sorted(frontier,key=lambda x:x[0])
        path = self.greedyReconstruct(cameFrom)
        return path




### Heuristic Functions ###

    def hFunEuclidean(self, a, b):
        return sqrt(pow((b[0]+1)-(a[0]+2), 2) + pow((b[1]+1) - (a[1]+1), 2))

    def hFunManhattan(self,a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def hFunChebyshev(self,a, b):
        return max(abs(b[0]-a[0]),abs(b[1]-a[1]))

    ### Debugging and Stats ###
    def printGrid(self,graph):
        for i in range(self.rows):
            for j in range(self.columns):
                print(graph[i][j], end=' ')
            print()
        print()


def main():
    solveGrids("pathfinding_a.txt","pathfinding_a_out.txt","a")
    solveGrids("pathfinding_a.txt","pathfinding_b_out.txt","b")
main()