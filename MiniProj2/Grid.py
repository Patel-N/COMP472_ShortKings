import numpy as np
from Car import Car
import copy
class Grid:
    def __init__(grid):
        rows, cols = (6, 6)
        
        # map = [["." for x in range(6)] for x in range(6)]
        map = [['.']* cols] * rows
        grid.map = map
        grid.cars = []
        grid.parent = {}


    #TO DO
    def getMoves(grid):
        moves = []
        for c in grid.cars:
            newMoves = grid.canCarMove(grid,c.name)
            if(not newMoves is None):
                moves.append(newMoves)
        return moves

    def canCarMove(grid, name):
         car = grid.getCarByName(grid,name)
         if(not Car(car).hasGas):
            return False
         start = Car (car).start
         end = Car(car).end
         moves = []
         if(Car(car).direction == 'vertical'):
             for i in range(len(grid.map)):
                if (map(start + [0,i]) == '.' ): # idk how to check genre le up/down of a specific car 
                    GridCopy = grid.deepcopy()
                    #create deep copy of grid
                    #move car in this new grid clone
                    #Grid.cars.move car
                    #reduce gas
                    #moves.append(newGrid)
                if (map(start - [0,i]) == '.' ):
                    GridCopy = grid.deepcopy()
                    #create deep copy of grid
                    #move car in this new grid clone
                    #Grid.cars.move car
                    #reduce gas
                    #moves.append(newGrid)
             return moves
         elif (Car(car).direction == 'horizontal'):
            for i in range(len(grid.map)):
                if (map(start + [i,0]) == '.' ): # idk how to check genre le up/down of a specific car 
                    GridCopy = grid.deepcopy()
                    #create deep copy of grid
                    #move car in this new grid clone
                    #Grid.cars.move car
                    #reduce gas
                    #moves.append(newGrid)
                if (map(start - [i,0]) == '.' ):
                    GridCopy = grid.deepcopy()
                    #create deep copy of grid
                    #move car in this new grid clone
                    #Grid.cars.move car
                    #reduce gas
                    #moves.append(newGrid)
            return moves
         return moves

            


    def getPath(grid, goal):
        path = [{goal}]
        step = Grid(goal).parent
        while True:
            path.append(step)
            if(Grid(step).parent is None):
                break
            step = Grid(step).parent
        path.reverse()
        return path
        

    def isGoalSpace(grid, nextStep):
       for c in nextStep.cars:
            if c.name == 'A':
                if (Car(c).end == [3,6] and Car(c).start == [3,5] ):
                    return True

    def getCarByName(grid, name):
        for c in grid.cars:
            if c.name == name:
                return c

    def printMap(grid):
        mapString = ''
        for row in grid.map:
            for col in row:
                mapString += col
            mapString += '\n'
        print(mapString)

    

    def parseStringToMap(grid, str):
        def split(word):
            return list(word)

        def splitString(a, n = 6):
            arr = [a[i:i+n] for i in range(0, len(a), n)]
            gameMap = [split(line) for line in arr]
            return gameMap
            
        grid.map = splitString(str)


        #find all the
        allSymbolOnGrid = list(set(np.array(grid.map).flatten()))
        
        if '.' in allSymbolOnGrid:
            allSymbolOnGrid.remove('.')
        
        for carVal in allSymbolOnGrid:
            car = Car(carVal)
            startFound = False
            for i in range(len(grid.map)):
                for j in range(len(grid.map[i])):
                    if car.name == grid.map[i][j] and not startFound:
                        car.start = [i, j]
                        startFound = True
                    elif car.name == grid.map[i][j]: 
                        car.end = [i, j]
            startFound = False

            car.direction = 'horizontal' if (car.start[0] == car.end[0]) else 'vertical'
            
            grid.cars.append(car)


    def setGasLevel(grid, gasValues):
        for gas in gasValues:
            targetCar = gas[0]
            gasQty = int(gas[1:])
            car = grid.getCarByName(targetCar)
            car.gas = gasQty