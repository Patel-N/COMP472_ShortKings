class Car:
    def __init__(car,direction, start, end, gas=100):
        car.direction = direction
        car.start = start
        car.end = end
        car.gas = gas

    def isVertical(car):
        return car.direction == 'vertical'
    
    def isHorizontal(car):
        return car.direction == 'horizontal'
        
