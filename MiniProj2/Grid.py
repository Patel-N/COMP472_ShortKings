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
            # print('Checking car move for -> ' + c.name)
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
        if not car.hasGas() or not car.isOnGrid:
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
                cell = map[y][top_x]
                #movement possible
                if( cell == '.' ):
                   moveCount = top_y - y 
                   movement = ['up', moveCount, car.name]
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
                    movement = ['down', moveCount, car.name]
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
                    movement = ['left', moveCount, car.name]
                    addToMovementDic(movementDict, car.name, movement)
                else:
                    break
                
                x -= 1

            #right
            right_x = end[1]
            right_y = end[0]
            x = right_x + 1
            while x < 6:
                cell = map[right_y][x]
                if cell == '.':
                    moveCount = x - right_x
                    movement = ['right', moveCount, car.name]
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
        
    def getCarByName(grid, name) -> Car:
        for c in grid.cars:
            if c.name == name:
                return c
    
    def isGoalSpace(grid) -> bool:
        c = grid.getCarByName('A')
        # print(c.start)
        # print(c.end)
        if (c.end == [2,5]): 
            return True
        else:
            return False


    def printMap(grid) -> str:
        mapString = ''
        for row in grid.map:
            for col in row:
                mapString += col
            mapString += '\n'
        print(mapString)
        return mapString

    def getAllCarFuel(grid):
        allCars = grid.cars
        stringToBuild = ''

        i = 1
        for x in allCars:
            stringToBuild += x.name + ':' + str(x.gas)
            if i != len(allCars):
                stringToBuild += ', '
            i += 1

        return stringToBuild

    def getSingleLineMap(grid) -> str:
        mapLoop = [ y for x in grid.map for y in x]
        return ''.join(map(str,mapLoop))

    def removeExitCar(grid):
        if grid.map[2][4] != '.' and grid.map[2][4] == grid.map[2][5]:
            carAtExit = grid.getCarByName(grid.map[2][5])
            print('Removing car -> ', carAtExit.name)
            carAtExit.start = None
            carAtExit.end = None
            carAtExit.isOnGrid = False
            grid.map[2][4] = '.'
            grid.map[2][5] = '.'
    

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
                    #keep iterating through the map until the last placement is found
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

    def heuristicOne(grid):
        value = 0
        x = 5
        blockingCars = []
        while x > 0 :
                cell = grid.map[2][x]
                if cell == 'A':
                    x = 0
                    break
                elif not cell ==  '.':
                    if (cell not in blockingCars):
                        blockingCars.append(cell)
                        value +=1
                
                x -= 1
        return value

    def heuristicTwo(grid):
        value = 0
        x = 5
        while x > 0 :
                cell = grid.map[2][x]
                if cell == 'A':
                    x = 0
                    break
                elif not cell ==  '.':
                    value +=1
                
                x -= 1
        return value

    def heuristicThree(grid):
        multipler = 5 #Hard coded
        value = 0
        x = 5
        while x > 0 :
                cell = grid.map[2][x]
                if cell == 'A':
                    x = 0
                    break
                elif not cell ==  '.':
                    value +=1
                
                x -= 1
        return value * multipler