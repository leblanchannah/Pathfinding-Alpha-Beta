###Pathfinding###

import heapq
from math import sqrt

 #Greedy algorithm


 #A* algorithm  

def solveGrids(inFile, outFile):
    #each grid is separated by an empty line
    #read in problems one by one
    #as reading input, note goal=G and start=S
    f = open("pathfinding_a.txt","r") 
    count = 0
    grid = []
    start = ()
    goal = () 
    for line in f:
        if line in ('\n'): #should add or next line is eof
            if grid != []:
                GridMap(grid,start,goal)
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




class GridMap:
    def __init__(self,grid,start,goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.columns = len(grid[0])
  
        ## up,down,right,left moves allowed - mode A
        self.mode = 'A'
        self.greedySearch()


        ## up,down,diagonal,left,right moves allowed - mode B
        self.mode = 'B'


    def neighbours(self,current):
        row = current[1][0]
        col = current[1][1]
        around = []
        if row != 0: #cant move up
            around.append((row-1,col))
            if self.mode == 'B' and col != 0:
                around.append((row-1,col-1))
            if self.mode == 'B' and col != self.columns:
                around.append((row-1,col+1))
        if row == self.rows:  #cant move down
            around.append((row+1,col))
            if self.mode == 'B' and col != 0:
                around.append((row+1,col-1))
            if self.mode == 'B' and col != self.columns:
                around.append((row+1,col+1))
        if col != 0: #cant move left
            around.append((row,col-1))
        if col != self.columns: #cant move right
            around.append((row,col+1))
        print(around)
        return around
        


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
            if current[1] == self.goal:
                break
            neighbours = self.neighbours(current)
            for next in neighbours:
                priority = self.hFunEuclidean(self.goal,next)
                heapq.heappush(frontier, (priority,next))
                cameFrom[next] = current
        print(cameFrom)



    #def aStarSearch(self):




### Heuristic Functions ###

    def hFunEuclidean(self, a, b):
        return sqrt(pow(b[0]-a[0], 2) + pow(b[1] - a[1], 2))

# def hFunManhattan(a, b):
#     return abs(a.x - b.x) + abs(a.y - b.y)

# def hFunChebyshev(a, b):
#     return max(abs(b.x-a.x),abs(b.y-a.y))

    ### Debugging and Stats ###
    def printGrid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                print(self.grid[i][j], end=' ')
            print()


def main():
    solveGrids("pathfinding_a.text","")

main()