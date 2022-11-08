from Car import Car
from Grid import Grid
import queue as Q

# c = Car('horizontal', '10', '20', 95)

# print(c.isVertical())

def UniformCostSearch(grid):
    OPEN = Q.PriorityQueue() #For UCS, we want a priority queue based on cost
    OPEN.put((1,grid))
    CLOSED = []
    numberOfSteps = 0
    while True:
        if(OPEN.empty()):
            print(f"No Solution for {grid.printMap()}")
            break
        numberOfSteps += 1
        nextStep = OPEN.get()
        CLOSED.append(nextStep)

        #Check for solution state
        if(nextStep.isGoalSpace(nextStep)):
            path = nextStep.getPath(nextStep)
            return path, numberOfSteps
        children = Grid (nextStep).getMoves(grid)

        
    #hello

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
    
    for x in grid.cars:
        print(x.name)
        print('\n\t',x.start,'\n\t',x.end,'\n\t',x.direction,'\n\t',x.gas)

    UniformCostSearch(grid)
    # handle predefined gas amount

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
"""