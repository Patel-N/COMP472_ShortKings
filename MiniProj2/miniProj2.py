from Car import Car
from Grid import Grid


# c = Car('horizontal', '10', '20', 95)

# print(c.isVertical())

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