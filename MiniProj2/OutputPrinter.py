from PriorityQueue import State, PriorityQueue
import re
import pandas as pd
import os

def generateOutputFiles(dir:str, filePrefix:str,  puzzleNum:int, initialPuzzle:str, finalState:State, searchDetails:str, timeToSol, stateSearchCount:int):
    
    printSearchFile(dir, filePrefix, puzzleNum, searchDetails)
    moveCount = printSolutionFile(dir, filePrefix, puzzleNum, initialPuzzle, finalState, timeToSol, stateSearchCount)
    # print(initialPuzzle)
    # print(finalState)
    # print(searchDetails)
    return moveCount

def printSearchFile(dir:str, file_name:str, puzzleNum:int, searchDetails:str):
    #Create file name 
    fileString = dir + file_name + '-search-' + str(puzzleNum) + '.txt'
    
    #open text file
    search_file = open(fileString, "w")
    
    #write string to file
    n = search_file.write(searchDetails)
    
    #close file
    search_file.close()


def printSolutionFile(dir:str, file_name:str, puzzleNum:int, initialPuzzle:str, finalState: State, time, stateSearchCount):
    mapInfo = initialPuzzle.split(" ", 1)
    movementList, initialCarFuel, solutionPath, moveCount, gridFormatInit = buildMovementList(finalState)

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

    search_file.write(gridFormatInit + '\n')

    search_file.write('Car fuel available: ' + initialCarFuel + '\n\n')

    if finalState.parent is None:
        search_file.write(movementList + '\n\n')

    search_file.write('Runtime: ' + str(time) + ' seconds\n')
    
    if finalState.parent is not None:
        search_file.write('Search path length: ' + str(stateSearchCount) + ' states\n')
        search_file.write('Solution path length: ' + str(moveCount) + ' moves\n')
        search_file.write('Solution path: ' + solutionPath + '\n\n')

        search_file.write(movementList + '\n\n')
        search_file.write('! ' + finalState.getCarConsumptionHistory() + '\n')
        search_file.write(finalState.grid.getGridFormatMap() + '\n\n')

    search_file.write('--------------------------------------------------------------------------------')
    
    #close file
    search_file.close()

    return moveCount


def buildMovementList(startState:State):
    movementListArr = []
    movementList = ''
    initCarGas = ''
    initMap = ''
    solutionPathArr = []
    solutionPath = ''
    moveCount = 0
    
    if startState.parent is None:
        movementList = 'Sorry, could not solve the puzzle as specified.\nError: no solution found'
        initCarGas = startState.grid.getAllCarFuel()
        initMap = startState.grid.getGridFormatMap()
    else:
        currentState = startState

        while currentState is not None:

            if currentState.movement is not None:
                movementString = '{:<2}{:>5}{:>2}       {:<3}{mapString} {history}'.format(currentState.movement[2], currentState.movement[0], currentState.movement[1], currentState.grid.getCarByName(currentState.movement[2]).gas, mapString = currentState.grid.getSingleLineMap(), history = currentState.getCarConsumptionHistory())
                movementListArr.insert(0, movementString)
                solStr = currentState.movement[2] + ' ' + currentState.movement[0] + ' ' + str(currentState.movement[1])
                
                if moveCount == 0:
                    solutionPathArr.insert(0, solStr)
                else:
                    solutionPathArr.insert(0, solStr + '; ')

                                
            if currentState.parent is None:
                initCarGas = currentState.grid.getAllCarFuel()
                initMap = currentState.grid.getGridFormatMap()
            else:
                moveCount += 1

            currentState = currentState.parent


        movementList = '\n'.join(movementListArr)
        solutionPath = ''.join(solutionPathArr)

    return movementList, initCarGas, solutionPath, moveCount, initMap

def printAnalysisFile(puzzleNumber, algo, heuristic, length_of_sol, length_of_search, exec_time):
    data = {
        "Puzzle Number": puzzleNumber,
        "Algorithm": algo,
        "Heuristic": heuristic,
        "Length of the Solution": length_of_sol,
        "Length of Search Path": length_of_search,
        "Execution Time(in seconds)": exec_time
    }

    df = pd.DataFrame(data)

    fileName = uniquify('./analysis/results.csv')

    df.to_csv(fileName)

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path