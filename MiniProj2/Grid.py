import numpy as np
from typing import List
from Car import Car
import copy
class Grid:
    def __init__(grid):
        rows, cols = (6, 6)
        
        # map = [["." for x in range(6)] for x in range(6)]
        map = [['.']* cols] * rows
        grid.map = map
        grid.cars:List[Car]= []
        grid.parent = {}


    #TO DO
    def getMoves(grid) -> List[dict[Car, any]]:
        moves = []
        for c in grid.cars:
            print('Checking car move for -> ' + c.name)
            newMoves = grid.canCarMove(c.name)

            #Will only add    
            if newMoves:
                moves.append(newMoves)

        return moves


    def canCarMove(grid, name) -> dict:

        def addToMovementDic(dict:dict, key, value):
            if key in dict.keys():
                valsForKeys = dict[key]
                valsForKeys.append(value)
                dict[key] = valsForKeys
            else:
                dict[key] = [value]


        movementDict = dict()
        car = grid.getCarByName(name)
        if not car.hasGas():
            return movementDict
        start = car.start
        end = car.end
        map = grid.map
        
        if car.isVertical():
            #Check up
            #car is vertical start will be the upper part
            top_x = start[1]
            top_y = start[0]
            y = top_y - 1
            while y >= 0:
                # print(car.name, top_x, i, map[i][top_x])
                cell = map[y][top_x]
                #movement possible
                if( cell == '.' ):
                   moveCount = top_y - y 
                   movement = ['up', moveCount]
                   addToMovementDic(movementDict, car.name, movement)
                else:
                    break
                y -= 1

            #Check down
            #car is vertical start will be the bottom part
            bottom_x = end[1]
            bottom_y = end[0]
            y = bottom_y + 1
            while y < 6:
                cell = map[y][bottom_x]
                #movement possible
                if( cell == '.' ):
                    moveCount = y - bottom_y
                    movement = ['down', moveCount]
                    addToMovementDic(movementDict, car.name, movement)
                else:
                    break
                y += 1
            
        elif car.isHorizontal():

            #left 
            left_x = start[1]
            left_y = start[0]
            x = left_x - 1
            while x >= 0:
                cell = map[left_y][x]
                
                if cell == '.':
                    moveCount = left_x - x
                    movement = ['left', moveCount]
                    addToMovementDic(movementDict, car.name, movement)
                else:
                    break
                
                x -= 1

            #right
            right_x = end[1]
            right_y = end[0]
            x = x + 1
            
            while x < 6:
                cell = map[right_y][x]

                if cell == '.':
                    moveCount = x - right_x
                    movement = ['right', moveCount]
                    addToMovementDic(movementDict, car.name, movement)
                else:
                    break
                
                x += 1

        return movementDict

    def getPath(grid, goal): #what is goal?
        path = [{goal}] #?? what is path, is it a deep copy of the grid?
        step = Grid(goal).parent #??
        while True:
            path.append(step)
            if(Grid(step).parent is None):
                break
            step = Grid(step).parent
        path.reverse()
        return path
        
    #the 2nd if condition could be wrong, flip start and end
    def isGoalSpace(grid) -> bool:
       for c in grid.cars:
            if c.name == 'A':
                if (c.end == [2,5]): #I THINK THIS IS WRONG, YOU COULD HAVE A 3 WIDE CAR, AND IF A CAR OTHER THAN 'A' is on [3,5] it goes out of the grid
                    return True

    def getCarByName(grid, name) -> Car:
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

        def getCarName(car:Car):
            return car.name
            
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

        #Sort cars by alphabetical order
        grid.cars = sorted(grid.cars, key=getCarName)


    def setGasLevel(grid, gasValues):
        for gas in gasValues:
            targetCar = gas[0]
            gasQty = int(gas[1:])
            car = grid.getCarByName(targetCar)
            car.gas = gasQty