from Car import Car
from Grid import Grid
import queue as Q
from PriorityQueue import PriorityQueue as pq
from PriorityQueue import State as State
import copy


def UniformCostSearch(grid):
    OPEN = Q.PriorityQueue() #For UCS, we want a priority queue based on cost
    OPEN.put((1,grid))
    CLOSED = []
    numberOfSteps = 0 #I don't get #ofSteps
    while True:
        if(OPEN.empty()):
            print(f"No Solution for {grid.printMap()}")
            break
        numberOfSteps += 1
        nextStep = OPEN.get()
        print(nextStep)
        CLOSED.append(nextStep)

        #Check for solution state
        if(nextStep.isGoalSpace(nextStep)):
            path = nextStep.getPath(nextStep)
            return path, numberOfSteps
        
        children = Grid (nextStep).getMoves(grid)


def neil_UniformCostSearch(grid):
    OPEN = pq()
    CLOSED = []
    goalStates = []

    #Initial State
    initialState = State(cost = 0, grid = grid)

    OPEN.insert(initialState)
    
    #Start search
    while True:
        #Check if no more options are left to be explored
        if OPEN.isEmpty():
            #I THINK THAT THERE ARE LARGER EDGE CASES TO BE HANDLED
            print("No solution")
            # print(f"No Solution for {grid.printMap()}")
            break

        #get leftMost state
        leftMostState = OPEN.get()
        CLOSED.append(leftMostState)
        #Check if goal state achieved for AA if yes, add to completedArray
        if leftMostState.grid.isGoalSpace():
            goalStates.append(leftMostState)
            #what else needs to be done o.o
        #handle exploration
        else:
            leftMostGrid = leftMostState.grid
            allMovements = leftMostGrid.getMoves()

        print(allMovements)
        for soloMovement in allMovements:
            for car, moves in soloMovement.items():
                car = Car(car)
                #iterate through all possible moves for a car
                for move in moves:
                    subState = doMovements(leftMostState, car.name, move)

                    break
                #would calculate heuristic here???

        # break

def doMovements(parent:State, carName, movement):
    #Create new state
    newState = State()

    # Refer to previous state as parent
    newState.parent = parent

    #Deepcopy of the grid + do movement and set movement(dict)
    newGrid = copy.deepcopy(parent.grid)
    updateGrid(newGrid, carName, movement)


def updateGrid(grid:Grid, carName, movement):
    #Get car from grid
    selectedCar = grid.getCarByName(carName)
    moveCount = int(movement[1])

    car_top_x = selectedCar.start[1]
    car_top_y = selectedCar.start[0]
    car_bottom_x = selectedCar.end[1]
    car_bottom_y = selectedCar.end[0]

    car_left_x = selectedCar.start[1]
    car_left_y = selectedCar.start[0]
    car_right_x = selectedCar.end[1]
    car_right_y = selectedCar.end[0]
    
    verticalCarLength = car_bottom_y - car_top_y + 1
    horizontalCarLength = car_right_x - car_left_x + 1

    #Update board and car
    if movement[0] == 'up':
        selectedCar.start[0] -= moveCount
        selectedCar.end[0] -= moveCount

        #need to rethink board update logic

        # while moveCount != 0:
        #     #Update cells with '.'
        #     grid.map[car_bottom_y][car_bottom_x] = '.'

        #     moveCount -= 1
        
        # #Update cells with car value
        # bottomCarIndex = selectedCar.end[0]
        # while verticalCarLength != 0:
        #     grid.map[bottomCarIndex][selectedCar.end[1]] = carName

        #     bottomCarIndex -= 1
        #     verticalCarLength -= 1

    elif movement[0] == 'down':
        selectedCar.start[0] += moveCount
        selectedCar.end[0] += moveCount

        # while moveCount != 0:
        #     #Update cells with '.'
        #     grid.map[car_bottom_y][car_bottom_x] = '.'

        #     moveCount -= 1
        
        # #Update cells with car value
        # bottomCarIndex = selectedCar.end[0]
        # while verticalCarLength != 0:
        #     grid.map[bottomCarIndex][selectedCar.end[1]] = carName

        #     bottomCarIndex -= 1
        #     verticalCarLength -= 1

    # elif movement[0] == 'left':

    # elif movement[0] == 'right':

    print(carName, movement)
    grid.printMap()
    


def getPuzzlesFromFile(filePath):
    f = open(filePath, 'r')
    validPuzzles = []
    for line in f:
        if not line.startswith("#") and line.strip():
            validPuzzles.append(line.replace('\n','').strip())

    return validPuzzles

def setupGame(gameInput):
    grid = Grid()
    grid.parseStringToMap(gameInput.pop(0))
    if len(gameInput) != 0:
        grid.setGasLevel(gameInput)

    return grid

def solvePuzzle(puzzleString):
    gameInput = puzzleString.split(' ')
    print(gameInput)
    grid = setupGame(gameInput)
    grid.printMap()
    
    # for x in grid.cars:
    #    print(x, '\n')
       
    # UniformCostSearch(grid)
    neil_UniformCostSearch(grid)

validPuzzles = getPuzzlesFromFile('./Sample/sample-input.txt')

for puzzle in validPuzzles:
    solvePuzzle(puzzle)
    break



"""
1) Setup grid
2) Parse file
3) Loop through all examples
    a) for each example run UCS, GBFS, A*
    b) generate files



UCS:

1) Start with root node 0 with initial Grid
2) go down first level do all potential moves for each car
3) Move to next

"""