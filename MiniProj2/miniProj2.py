from Car import Car
from Grid import Grid
import queue as Q
from PriorityQueue import PriorityQueue as pq
from PriorityQueue import State as State
import copy
from typing import List


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
    print(initialState.grid.cars)
    #Start search
    while True:
        #Check if no more options are left to be explored
        # print('OPEN size:', len(OPEN.queue) )
        # print('GoalState size:', len(goalStates) )

        if OPEN.isEmpty():
            if len(goalStates) == 0:
                print("No solution")
            else:
                print(len(goalStates))
                bestPathState = findGoalStateWithLowestCost(goalStates)
                print('Final state:')
                break

        #get leftMost state
        leftMostState = OPEN.get()

        CLOSED.append(leftMostState)
        #Check if goal state achieved for AA if yes, add to completedArray
    
        leftMostGrid = leftMostState.grid
        allMovements = leftMostGrid.getMoves()

        for soloMovement in allMovements:
            for car, moves in soloMovement.items():
                car = Car(car)
                #iterate through all possible moves for a car
                for move in moves:

                    #Update the grid
                    subState = doMovement(leftMostState, car.name, move)

                    #Update the cost
                    newCost = leftMostState.cost + 1
                    subState.cost = newCost

                    #would calculate heuristic here???
                    stateWithSameGridAsSubstate = checkForSameGridInOpen(OPEN, subState)
                    
                    #check if movement results into winning if not do state add to queue evaluation
                    if subState.grid.isGoalSpace():
                        print("final map:")
                        subState.grid.printMap()
                        goalStates.append(subState)

                    #add new subState if not same grid is found in the OPEN queue
                    elif stateWithSameGridAsSubstate is None: #would probably evaluate if same state already in OPEN but compare cost
                        OPEN.insert(subState)
                        #Check if substate has car possible for exit
                        subState.grid.removeExitCar()
                    else: 
                        #if same grid found with lower cost, we ignore the new substate
                        #if same grid but higher cost, we add new one and discard the more expensive state from OPEN
                        if subState.cost < stateWithSameGridAsSubstate.cost:
                            #remove state from queue
                            OPEN.getState(stateWithSameGridAsSubstate)
                            OPEN.insert(subState)
                        #Check if substate has car possible for exit
                        subState.grid.removeExitCar()


def GBFS_HOne(grid : Grid):
    OPEN = Q.PriorityQueue() #For UCS, we want a priority queue based on cost
    CLOSED = []
    goalStates = []

    #Initial State
    
    starting_heuristic = grid.heuristicOne()
    initialState = State(cost = starting_heuristic, grid = grid)

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
            #PRINT ANSWER / # of steps
            break
        #handle exploration
        else:
            leftMostGrid = leftMostState.grid
            allMovements = leftMostGrid.getMoves()

        
        for soloMovement in allMovements:
            for car, moves in soloMovement.items():
                car = Car(car)
                #iterate through all possible moves for a car
                for move in moves:
                    subState = doMovement(leftMostState, car.name, move)

                    #Update the cost
                    subState.cost = subState.grid.heuristicOne()

                    #would calculate heuristic here???

                    if(True): #would probably evaluate if same state already in OPEN but compare cost
                        OPEN.insert(subState)
        
                
def findGoalStateWithLowestCost(goalStates:List[State]):
    lowestCostState = goalStates[0]
    for x in goalStates:
        if x.cost < lowestCostState.cost:
            lowestCostState = x
    
    return lowestCostState

def checkForSameGridInOpen(OPEN: pq, subState:State) -> State:
    
    for stateInQueue in OPEN.queue:
        if(subState.grid.map == stateInQueue.grid.map):
            return stateInQueue
    
    return None
    
def isGridInClose(newState:State, CLOSED:List[State]):
    for x in CLOSED:
        if x.grid.map == newState.grid.map and newState.cost < 

def doMovement(parent:State, carName, movement) -> State:
    #Create new state
    newState = State()


    #Deepcopy of the grid + do movement and set movement(dict)
    newGrid = copy.deepcopy(parent.grid)
    newGrid = updateGrid(newGrid, carName, movement)
    
    # print('Old')
    # parent.grid.printMap()
    # print('New')
    # newGrid.printMap()

    # Set variables
    newState.grid = newGrid
    newState.parent = parent
    newState.movement = movement
    
    return newState


def updateGrid(grid:Grid, carName, movement) -> Grid:
    #Get car from grid
    selectedCar = grid.getCarByName(carName)
    moveCount = int(movement[1])

        
    carLength = selectedCar.getCarLength()
    i = 0

    #Update board and car
    if movement[0] == 'up':
        #update car position but not in grid
        selectedCar.start[0] -= moveCount
        selectedCar.end[0] -= moveCount

        while i < carLength:
            #using new start index
            grid.map[selectedCar.start[0] + i][selectedCar.start[1]] = selectedCar.name
            i += 1
        
        while moveCount != 0:
            grid.map[selectedCar.end[0] + moveCount][selectedCar.start[1]] = '.'
            moveCount -= 1
        

    elif movement[0] == 'down':
        selectedCar.start[0] += moveCount
        selectedCar.end[0] += moveCount
        
        while i < carLength:
            #using new start index, update the lower cells
            grid.map[selectedCar.start[0] + i][selectedCar.start[1]] = selectedCar.name
            i += 1
        
        while moveCount != 0:
            #using new start index, update the upper cells
            grid.map[selectedCar.start[0] - moveCount][selectedCar.start[1]] = '.'
            moveCount -= 1

    elif movement[0] == 'left':
        #update car position but not in grid
        selectedCar.start[1] -= moveCount
        selectedCar.end[1] -= moveCount

        while i < carLength:
            #using new start index, update the right sided cells
            grid.map[selectedCar.start[0]][selectedCar.start[1] + i] = selectedCar.name
            i += 1

        while moveCount != 0:
            #using new start index, update the upper cells
            grid.map[selectedCar.start[0]][selectedCar.end[1] + moveCount] = '.'
            moveCount -= 1

    elif movement[0] == 'right':
        #update car position but not in grid
        selectedCar.start[1] += moveCount
        selectedCar.end[1] += moveCount

        while i < carLength:
            #using new start index, update the right sided cells
            grid.map[selectedCar.start[0]][selectedCar.start[1] + i] = selectedCar.name
            i += 1

        while moveCount != 0:
            #using new start index, update the upper cells
            grid.map[selectedCar.start[0]][selectedCar.start[1] - moveCount] = '.'
            moveCount -= 1
    
    #Update remaining gas
    selectedCar.useGas(moveCount)
    return grid
    
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

    y = grid.heuristicOne()
    print(y)
    
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