from Grid import Grid
from typing import List

class State:
    def __init__(self, cost:int = 0, grid:Grid = None, parent:'State' = None, movement:list = None):
        self.cost:int = cost
        self.grid:Grid = grid
        self.parent = parent
        self.movement = movement
        self.f = 0
        self.g = 0
        self.h = 0
        self.carGasCapacities:dict = dict()

    def getCarConsumptionHistory(self) -> str:
        history = ''
        for key, value in self.carGasCapacities.items():
            history = history + key + str(value) + ' '

        return history

    def getStateSearchDetail(self) -> str:
        detailAtState = str(self.f) + ' ' + str(self.g) + ' ' + str(self.h) + ' ' + self.grid.getSingleLineMap() + ' ' + self.getCarConsumptionHistory()
        # print('Details at state -> ', detailAtState)
        return detailAtState

class PriorityQueue(object):
    def __init__(self):
        self.queue:List[State] = []
 
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
 
    # for checking if the queue is empty
    def isEmpty(self) -> bool:
        return len(self.queue) == 0
 
    # for inserting an element in the queue
    def insert(self, data:State):
        self.queue.append(data)
        sortedQueue = sorted(self.queue, key=self.takeCost)
        self.queue = sortedQueue

    def insertH(self, data:State):
        self.queue.append(data)
        sortedQueue = sorted(self.queue, key=self.takeH)
        self.queue = sortedQueue

    def insertG(self, data:State):
        self.queue.append(data)
        sortedQueue = sorted(self.queue, key=self.takeG)
        self.queue = sortedQueue
 
    def takeCost(self, elem:State):
        return elem.cost

    def takeH(self, elem:State):
        return elem.h
        
    def takeG(self, elem:State):
        return elem.h + elem.cost

    def getState(self, state:State) -> State:
        return self.queue.remove(state)
            
    # for popping the leftMost state based on Priority
    # if no item, silently handle exception
    def get(self) -> State :
        try:
            item = self.queue[0]
            del self.queue[0]
            return item
        except IndexError:
            print()
            exit()
