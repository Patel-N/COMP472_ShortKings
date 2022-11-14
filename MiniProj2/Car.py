from typing import List
class Car:
    def __init__(car, name, direction='', start:list=[], end:list=[], gas=100):
        car.direction = direction
        car.start = start
        car.end = end
        car.gas = gas
        car.name = name

    def isVertical(car):
        return car.direction == 'vertical'
    
    def isHorizontal(car):
        return car.direction == 'horizontal'
        
    def useGas(car, amount):
        Car(car).gas -= amount

    def hasGas(car):
        return Car(car).gas > 0

    def __str__(self) -> str:
        strToPrint = ''
        strToPrint += 'Car: ' + self.name + '\n'
        strToPrint += '  Start:\t' + str(self.start) + '\n' 
        strToPrint += '  End:\t\t' + str(self.end) + '\n'
        strToPrint += '  Direction:\t' + self.direction + '\n'
        strToPrint += '  Gas:\t\t' + str(self.gas)
    
        return strToPrint