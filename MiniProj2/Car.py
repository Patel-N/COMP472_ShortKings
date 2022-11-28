from typing import List
class Car:
    def __init__(self, name, direction='', start:list[int, int]=[], end:list[int, int]=[], gas=100):
        self.direction = direction
        self.start = start
        self.end = end
        self.gas = gas
        self.name = name
        self.isOnGrid = True

    def isVertical(self):
        return self.direction == 'vertical'
    
    def isHorizontal(self):
        return self.direction == 'horizontal'
        
    def useGas(self, amount):
        self.gas -= amount

    def hasGas(self) -> bool:
        return self.gas > 0

    def getCarLength(self) -> int:
        if self.isHorizontal():
            return int(self.end[1]) - int(self.start[1]) + 1
        elif self.isVertical():
            return int(self.end[0]) - int(self.start[0]) + 1

    def __str__(self) -> str:
        strToPrint = ''
        strToPrint += 'Car: ' + self.name + '\n'
        strToPrint += '  Start:\t' + str(self.start) + '\n' 
        strToPrint += '  End:\t\t' + str(self.end) + '\n'
        strToPrint += '  Direction:\t' + self.direction + '\n'
        strToPrint += '  Gas:\t\t' + str(self.gas)
    
        return strToPrint