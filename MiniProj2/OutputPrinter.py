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
    
    movementList, initialCarFuel, solutionPath = buildMovementList(finalState)

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

    search_file.write('Runtime: ' + str(time) + ' seconds\n')
    
    if finalState.parent is not None:
        search_file.write('Search path length: ' + str(None) + ' states\n')
        search_file.write('Solution path length: ' + str(None) + ' moves\n')
        search_file.write('Solution path: ' + solutionPath + '\n\n')

        search_file.write(movementList + '\n\n')
        search_file.write('! ' + finalState.getCarConsumptionHistory() + '\n')
        search_file.write(finalState.grid.printMap() + '\n\n')

    search_file.write('--------------------------------------------------------------------------------')
    
    #close file
    search_file.close()


def buildMovementList(startState:State):
    movementListArr = []
    movementList = ''
    initCarGas = ''
    solutionPathArr = []
    solutionPath = ''
    
    if startState.parent is None:
        movementList = 'Sorry, could not solve the puzzle as specified.\nError: no solution found'
        initCarGas = startState.grid.getAllCarFuel()
    else:
        currentState = startState

        while currentState is not None:

            if currentState.movement is not None:
                movementString = '{:<2}{:>5}{:>2}       {:<3}{mapString} {history}'.format(currentState.movement[2], currentState.movement[0], currentState.movement[1], currentState.grid.getCarByName(currentState.movement[2]).gas, mapString = currentState.grid.getSingleLineMap(), history = currentState.getCarConsumptionHistory())
                movementListArr.insert(0, movementString)
                solStr = currentState.movement[2] + ' ' + currentState.movement[0] + ' ' + str(currentState.movement[1])
                if currentState.parent.movement is None:
                    print(solStr + ';')
                    solutionPathArr.insert(0, solStr + '; ')
                else:
                    print(solStr)
                    solutionPathArr.insert(0, solStr)
                    
            if currentState.parent is None:
                initCarGas = currentState.grid.getAllCarFuel()
            currentState = currentState.parent

        movementList = '\n'.join(movementListArr)
        solutionPath = ''.join(solutionPathArr)

    return movementList, initCarGas, solutionPath

