class Car:
    def __init__(car, name, direction='', start=[], end=[], gas=100):
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