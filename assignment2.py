###Pathfinding###

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

    def printGrid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                print(self.grid[i][j], end=' ')
            print()


def main():
    solveGrids("pathfinding_a.text","")

main()