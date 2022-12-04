from Car import Car
from Grid import Grid
import queue as Q
from PriorityQueue import PriorityQueue as pq
from PriorityQueue import State as State
import copy
from typing import List
from OutputPrinter import *
import time
import os
import shutil

def UniformCostSearch(grid):
    OPEN = pq()
    CLOSED = []
    goalStates = []
    searchDetails = ''
    stateSearchCount = 0

    #Initial State
    initialState = State(cost = 0, grid = grid)
    subState = None

    OPEN.insert(initialState)
    searchDetails += initialState.getStateSearchDetail() + '\n'
    start_time = time.time()

    #Start search
    while True:
        #Check if no more options are left to be explored
        # print('OPEN size:', len(OPEN.queue) )
        # print('GoalState size:', len(goalStates) )

        #SUCCESS
        if len(goalStates) > 0:
            final_time = time.time() - start_time
            return subState, searchDetails, final_time, stateSearchCount

        #FAILURE
        if OPEN.isEmpty():
            final_time = time.time() - start_time
            return initialState, searchDetails, final_time, stateSearchCount

        #get leftMost state
        leftMostState = OPEN.get()

        CLOSED.append(leftMostState)
        #Check if goal state achieved for AA if yes, add to completedArray
    
        leftMostGrid = leftMostState.grid
        allMovements = leftMostGrid.getMoves()

        for soloMovement in allMovements:

            if len(goalStates) != 0:
                break

            for car, moves in soloMovement.items():
                car = Car(car)
                #iterate through all possible moves for a car
                for move in moves:

                    #Update the grid
                    subState = doMovement(leftMostState, car.name, move, searchDetails)
                    

                    #Update the cost
                    prevG = leftMostState.g
                    newG = prevG + 1
                    subState.g = newG

                    #UCS cost is always edge cost --> g
                    subState.f = newG
                    subState.cost = newG
                    
                    #Update searchDetails
                    searchDetails += subState.getStateSearchDetail() + '\n'
                    
                    #CHECK IF IN CLOSED
                    openStateWithSameGridAsSubstate = checkForSameGridInOpen(OPEN, subState)
                    closedStateWithSameGridAsSubstate = checkForSameGridInClosed(CLOSED, subState)
                    
                    #check if movement results into winning if not do state add to queue evaluation
                    if subState.grid.isGoalSpace():
                        goalStates.append(subState)
                        break

                    #add new subState if not same grid is found in the OPEN queue
                    elif openStateWithSameGridAsSubstate is None and closedStateWithSameGridAsSubstate is None: #would probably evaluate if same state already in OPEN but compare cost
                        
                        # Count the amount of state change done
                        stateSearchCount += 1

                        OPEN.insert(subState)
                        #Check if substate has car possible for exit
                        subState.grid.removeExitCar()
                    else: 
                        #if same grid found with lower cost, we ignore the new substate
                        #if same grid but higher cost, we add new one and discard the more expensive state from OPEN
                        
                        if openStateWithSameGridAsSubstate is not None and subState.cost < openStateWithSameGridAsSubstate.cost:
                            # Count the amount of state change done
                            stateSearchCount += 1


                            #remove state from queue
                            OPEN.getState(openStateWithSameGridAsSubstate)
                            OPEN.insert(subState)

                        #Check if substate has car possible for exit
                        subState.grid.removeExitCar()


def GBFS(grid, heuristic):
    OPEN = pq()
    CLOSED = []
    goalStates = []
    searchDetails = ''
    stateSearchCount = 0
    #Initial State
    starting_heuristic = grid.heuristic(heuristic)
    initialState = State(cost = starting_heuristic, grid = grid)
    subState = None

    OPEN.insertH(initialState)
    start_time = time.time()
    searchDetails += subState.getStateSearchDetail() + '\n'
    
    #Start search
    while True:
        #Check if no more options are left to be explored
        # print('OPEN size:', len(OPEN.queue) )
        # print('GoalState size:', len(goalStates) )
        
         
        #SUCCESS
        if len(goalStates) > 0:
            final_time = time.time() - start_time
            return subState, searchDetails, final_time, stateSearchCount

        #FAILURE
        if OPEN.isEmpty():
            if len(goalStates) == 0:
                final_time = time.time() - start_time
                return subState, searchDetails, final_time, stateSearchCount
       
        #get leftMost state
        leftMostState = OPEN.get()

        CLOSED.append(leftMostState)
        #Check if goal state achieved for AA if yes, add to completedArray
    
        leftMostGrid = leftMostState.grid
        allMovements = leftMostGrid.getMoves()

        for soloMovement in allMovements:

            if len(goalStates) != 0:
                break

            for car, moves in soloMovement.items():
                car = Car(car)
                #iterate through all possible moves for a car
                for move in moves:

                    #Update the grid
                    subState = doMovement(leftMostState, car.name, move, searchDetails)

                    #Update the cost
                    
                    
                    newCost = leftMostState.cost + 1
                    subState.cost = newCost
                    subState.h = subState.grid.heuristic(heuristic)
                    
                    #Update searchDetails
                    searchDetails += subState.getStateSearchDetail() + '\n'

                    #would calculate heuristic here???
                    stateWithSameGridAsSubstate = checkForSameGridInOpen(OPEN, subState)
                    closedStateWithSameGridAsSubstate = checkForSameGridInClosed(CLOSED, subState)
                    
                    #check if movement results into winning if not do state add to queue evaluation
                    if subState.grid.isGoalSpace():
                        goalStates.append(subState)
                        break

                    #add new subState if not same grid is found in the OPEN queue
                    elif stateWithSameGridAsSubstate is None and closedStateWithSameGridAsSubstate is None: #would probably evaluate if same state already in OPEN but compare cost
                        OPEN.insertH(subState)
                        stateSearchCount += 1
                        #Check if substate has car possible for exit
                        subState.grid.removeExitCar()
                    else: 
                        #if same grid found with lower cost, we ignore the new substate
                        #if same grid but higher cost, we add new one and discard the more expensive state from OPEN
                        if stateWithSameGridAsSubstate is not None and subState.cost < stateWithSameGridAsSubstate.cost:
                            #remove state from queue
                            stateSearchCount += 1
                            OPEN.getState(stateWithSameGridAsSubstate)
                            OPEN.insertH(subState)
                        #Check if substate has car possible for exit
                        subState.grid.removeExitCar()


def A(grid, heuristic):
    OPEN = pq()
    CLOSED = []
    goalStates = []
    searchDetails = ''
    stateSearchCount = 0
    #Initial State
    starting_heuristic = grid.heuristic(heuristic)
    initialState = State(cost = starting_heuristic, grid = grid)
    subState = None

    OPEN.insertG(initialState)
    start_time = time.time()

    #Start search
    while True:
        #Check if no more options are left to be explored
        # print('OPEN size:', len(OPEN.queue) )
        # print('GoalState size:', len(goalStates) )
        
         
        #SUCCESS
        if len(goalStates) > 0:
            final_time = time.time() - start_time
            return subState, searchDetails, final_time, stateSearchCount

        #FAILURE
        if OPEN.isEmpty():
            if len(goalStates) == 0:
                final_time = time.time() - start_time
                return subState, searchDetails, final_time, stateSearchCount
       
        #get leftMost state
        leftMostState = OPEN.get()

        CLOSED.append(leftMostState)
        #Check if goal state achieved for AA if yes, add to completedArray
    
        leftMostGrid = leftMostState.grid
        allMovements = leftMostGrid.getMoves()

        for soloMovement in allMovements:

            if len(goalStates) != 0:
                break

            for car, moves in soloMovement.items():
                car = Car(car)
                #iterate through all possible moves for a car
                for move in moves:

                    #Update the grid
                    subState, details = doMovement(leftMostState, car.name, move, searchDetails)
                    searchDetails += details + '\n'

                    #Update the cost
                    
                    
                    newCost = leftMostState.cost + 1
                    subState.cost = newCost
                    subState.h = subState.grid.heuristic(heuristic)
                    

                    #would calculate heuristic here???
                    stateWithSameGridAsSubstate = checkForSameGridInOpen(OPEN, subState)
                    closedStateWithSameGridAsSubstate = checkForSameGridInClosed(CLOSED, subState)
                    
                    #check if movement results into winning if not do state add to queue evaluation
                    if subState.grid.isGoalSpace():
                        goalStates.append(subState)
                        break

                    #add new subState if not same grid is found in the OPEN queue
                    elif stateWithSameGridAsSubstate is None and closedStateWithSameGridAsSubstate is None: #would probably evaluate if same state already in OPEN but compare cost
                        OPEN.insertG(subState)
                        stateSearchCount += 1
                        #Check if substate has car possible for exit
                        subState.grid.removeExitCar()
                    else: 
                        #if same grid found with lower cost, we ignore the new substate
                        #if same grid but higher cost, we add new one and discard the more expensive state from OPEN
                        if stateWithSameGridAsSubstate is not None and subState.cost < stateWithSameGridAsSubstate.cost:
                            #remove state from queue
                            stateSearchCount += 1
                            OPEN.getState(stateWithSameGridAsSubstate)
                            OPEN.insertG(subState)
                        #Check if substate has car possible for exit
                        subState.grid.removeExitCar()


        
                
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


def checkForSameGridInClosed(CLOSED: list[State], subState:State) -> State:
    
    for stateInQueue in CLOSED:
        if(subState.grid.map == stateInQueue.grid.map):
            return stateInQueue
    
    return None

def doMovement(parent:State, carName, movement, searchHistory:str = '') -> State:
    #Create new state
    newState = State()


    #Deepcopy of the grid + do movement and set movement(dict)
    newGrid = copy.deepcopy(parent.grid)
    newGrid = updateGrid(newGrid, carName, movement)

    #Retrieve a copy of prior gasConsumption
    newState.carGasCapacities = copy.deepcopy(parent.carGasCapacities)

    # Set variables
    newState.grid = newGrid
    newState.parent = parent
    newState.movement = movement

    #Update car capacities for search print
    newState.carGasCapacities[str(carName)] = newGrid.getCarByName(carName).gas
    
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
    selectedCar.useGas(int(movement[1]))
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

def addResultForAnalysis(puzzleNum: int, alg:str, heur:str, sol:int, search:int, time):
    global puzzleNumber
    global algo
    global heuristic
    global length_of_sol
    global length_of_search
    global exec_time

    puzzleNumber.append(puzzleNum)
    algo.append(alg)
    heuristic.append(heur)
    length_of_sol.append(sol)
    length_of_search.append(search)
    exec_time.append(time)


def solvePuzzle(puzzleString, puzzleNum:int):
    global dir

    gameInput = puzzleString.split(' ')
    # print(gameInput)
    grid = setupGame(gameInput)
    grid.printMap()
    
    print("start")

    # UniformCostSearch(grid)
    ucs_state, ucs_details, search_time, stateSearchCount = UniformCostSearch(grid)
    moveCount = generateOutputFiles(dir, 'ucs',  puzzleNum, puzzleString, ucs_state, ucs_details, search_time, stateSearchCount)
    addResultForAnalysis(puzzleNum, 'UCS', 'N/A', moveCount, stateSearchCount, search_time)
    
    gbfs_state, gbfs_details, search_time, stateSearchCount = GBFS(grid, 'h1')
    moveCount = generateOutputFiles(dir, 'GBFS',  puzzleNum, puzzleString, gbfs_state, gbfs_details, search_time, stateSearchCount)

    #GBFS
    # ucs_state, ucs_details, search_time, stateSearchCount = UniformCostSearch(grid)
    # generateOutputFiles(dir, 'ucs',  puzzleNum, puzzleString, ucs_state, ucs_details, search_time, stateSearchCount)
    print(search_time)



validPuzzles = getPuzzlesFromFile('./Sample/sample-input.txt')
puzzleNumber = []
algo = []
heuristic = []
length_of_sol = []
length_of_search = []
exec_time = []




#Prepare output folders
dir = './output_files/'
if os.path.exists(dir):
    shutil.rmtree(dir)

os.makedirs(dir)

analysis_dir = './analysis/'
if not os.path.exists(analysis_dir):
    os.makedirs(analysis_dir)


puzzleNum = 1
for puzzle in validPuzzles:
    solvePuzzle(puzzle, puzzleNum)
    puzzleNum += 1

printAnalysisFile(puzzleNumber, algo, heuristic, length_of_sol, length_of_search, exec_time)

