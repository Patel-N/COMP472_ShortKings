from Grid import Grid
from typing import List

class State:
    def __init__(self, cost:int = 0, grid:Grid = None, parent:'State' = None):
        self.priority:int = cost
        self.grid:Grid = grid
        self.parent = parent
        #dictionary like -> ['car.name',[direction, moveCount]]

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
        sortedQueue = sorted(self.queue, key=self.takePriority)
        self.queue = sortedQueue
 
    def takePriority(self, elem:State):
        return elem.priority

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
