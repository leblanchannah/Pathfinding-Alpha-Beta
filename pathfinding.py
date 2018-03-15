###Pathfinding###

import heapq
import copy
from math import sqrt

 #Greedy algorithm


 #A* algorithm  

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
                for i in range(len(soln.greedy)):
                    for j in range(len(soln.greedy[0])):
                        out.write(soln.greedy[i][j] + " ")
                    out.write("\n")
                out.write("\n")
                for i in range(len(soln.astar)):
                    for j in range(len(soln.astar[0])):
                        out.write(soln.astar[i][j] + " ")
                    out.write("\n")
                out.write("\n")
            grid = []
            start = ()
            goal = ()
            count = 0
        else:
            row = list(line)
            elements = len(row)
            grid.append(row[:elements-1]) #removing end \n char
            for section in range(elements):
                if row[section] == 'G':
                    #(row,column)
                    goal = (count,section)
                elif row[section] == 'S':
                    start = (count,section)
            count += 1
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
    def neighbours(self,current):
        row = current[1][0]
        col = current[1][1]
        around = []
        if row != 0: #cant move up
            if self.grid[row-1][col] != 'X':
                around.append((row-1,col))
            if self.mode == 'B' and col != 0:
                if self.grid[row-1][col-1] != 'X':
                    around.append((row-1,col-1))
            if self.mode == 'B' and col != self.columns:
                if self.grid[row-1][col+1] != 'X':
                    around.append((row-1,col+1))
        if row != self.rows:  #cant move down
            if self.grid[row+1][col] != 'X':
                around.append((row+1,col))
            if self.mode == 'B' and col != 0:
                if self.grid[row+1][col-1] != 'X':
                    around.append((row+1,col-1))
            if self.mode == 'B' and col != self.columns:
                if self.grid[row+1][col+1] != 'X':
                    around.append((row+1,col+1))
        if col != 0: #cant move left
            if self.grid[row][col-1] != 'X':
                around.append((row,col-1))
        if col != self.columns: #cant move right
            if self.grid[row][col+1] != 'X':
                around.append((row,col+1))
        #returns list of tuples (row,col) of legal moves 
        return around
        
    # reconstructs path from search
    def greedyReconstruct(self, cameFrom):
        current = self.goal
        path = [current]
        while current != self.start:
            current = cameFrom[current]
            path.append(current)
        path.reverse()
        return path

    def greedySearch(self):
        #priority queue https://docs.python.org/2/library/heapq.html
        # h = []
        # heappush(h, (5, 'write code'))
        frontier = []
        heapq.heappush(frontier, (0,self.start))
        cameFrom = {}
        cameFrom['S'] = None
        while not frontier == []:
            current = heapq.heappop(frontier)
            heapq.heapify(frontier)
            if current[1] == self.goal:
                break
            neighbours = self.neighbours(current)
            for next in neighbours:
                if next not in cameFrom:
                    priority = self.hFunEuclidean(self.goal,next)
                    heapq.heappush(frontier, (priority,next))
                    cameFrom[next] = current[1]
        path = self.greedyReconstruct(cameFrom)
        return path



    def aStarSearch(self):
        frontier = []
        heapq.heappush(frontier, (0,self.start))
        cameFrom = {}
        csf = {}  #cost so far
        cameFrom['S'] = None
        csf[self.start] = 0
        while not frontier == []:
            current = heapq.heappop(frontier)
            heapq.heapify(frontier)
            if current[1] == self.goal:
                break
            neighbours = self.neighbours(current)
            for next in neighbours:
                # new Cost = csf[current] + graph.cost(current,next)
                # all costs are == 1
                newCost = csf[current[1]] + 1
                if next not in csf or newCost < csf[next]:
                    csf[next] = newCost
                    priority = newCost + self.hFunEuclidean(self.goal,next)
                    heapq.heappush(frontier, (priority,next))
                    cameFrom[next] = current[1]
        path = self.greedyReconstruct(cameFrom)
        return path




### Heuristic Functions ###

    def hFunEuclidean(self, a, b):
        return sqrt(pow(b[0]-a[0], 2) + pow(b[1] - a[1], 2))

    def hFunManhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def hFunChebyshev(a, b):
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