from PriorityQueue import State, PriorityQueue
import os
import shutil

def generateOutputFiles(dir:str, filePrefix:str,  puzzleNum:int, initialPuzzle:str, finalState:State, searchDetails:str, timeToSol):
    
    printSearchFile(dir, filePrefix, puzzleNum, searchDetails)
    print(finalState)
    printSolutionFile(dir, filePrefix, puzzleNum, initialPuzzle, finalState, timeToSol)
    # print(initialPuzzle)
    # print(finalState)
    # print(searchDetails)


def printSearchFile(dir:str, file_name:str, puzzleNum:int, searchDetails:str):
    #Create file name 
    fileString = dir + file_name + '-search-' + str(puzzleNum) + '.txt'
    
    #open text file
    search_file = open(fileString, "w")
    
    #write string to file
    n = search_file.write(searchDetails)
    
    #close file
    search_file.close()


def printSolutionFile(dir:str, file_name:str, puzzleNum:int, initialPuzzle:str, finalState: State, time):
    mapInfo = initialPuzzle.split(" ", 1)
    
    movementList, initialCarFuel = buildMovementList(finalState)

    #Create file name 
    fileString = dir + file_name + '-sol-' + str(puzzleNum) + '.txt'
    
    #open text file
    search_file = open(fileString, "w")
    
    #write string to file
    search_file.write('--------------------------------------------------------------------------------\n\n')
    search_file.write('Initial board configuration:  ' + initialPuzzle + '\n\n')
    search_file.write('! ')
    
    if len(mapInfo) > 1:
        search_file.write(mapInfo[1])
    
    search_file.write('\n')

    search_file.write(finalState.grid.printMap() + '\n')

    search_file.write('Car fuel available: ' + initialCarFuel + '\n\n')

    search_file.write(movementList + '\n\n')

    search_file.write('Runtime: ' + str(time) + ' seconds\n')

    search_file.write('--------------------------------------------------------------------------------')
    
    #close file
    search_file.close()


def buildMovementList(startState:State):
    movementList = ''
    initCarGas = ''

    if startState.parent is None:
        movementList = 'Sorry, could not solve the puzzle as specified.\nError: no solution found'
        initCarGas = startState.grid.getAllCarFuel()
    else:
        currentState = startState
        while currentState is not None:
            print(currentState.movement)

            if currentState.parent is None:
                initCarGas = currentState.grid.getAllCarFuel()

            currentState = currentState.parent

    return movementList, initCarGas

