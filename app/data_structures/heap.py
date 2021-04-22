#!/user/bin/env python3

import sys
sys.path.append('../')
"""
    Heap (binary)
    -----------------------------------------
"""

class Node : 

    def __init__(self, index, weight):
        self.index = index
        self.weight = weight
    
    def toTuple(self):
        return (self.index, self.weight)
    # def setIndex(self, index):
    #     self.index = index

    # def setWeight(self, weight):
    #     self.weight = weight

    

class Heap:

    def __init__(self):
        self.list = [Node(0, float('-inf'))]
        self.currentSize = 0
    
    def parent(self, index):
        return list[index//2]

    def right(self, index):
        return list[(index * 2) + 1]
    
    def left(self, index):
        return list[(index * 2)]

    def heapifyUp(self, index): 
        while index // 2 > 0:
            if self.list[index].weight < self.list[index // 2].weight:
                self.list[index], self.list[index // 2] = self.list[index // 2], self.list[index]
            index //= 2

    def search(self, index):
        for node in self.list:
            if node.index == index:
                return True
        return False
    
    def searchAndUpdateWeight(self, index, newWeight):
        i = 0
        for node in self.list:
            if i == 0:
                i += 1
                continue
            if node.index == index:
                node.weight = float('-inf')
                self.heapifyUp(i)
                self.list[1].weight = newWeight
                self.heapifyDown(1)
                return
            else: 
                i += 1
            

    def insert(self, node):
        self.list.append(node)
        self.currentSize += 1
        self.heapifyUp(self.currentSize)
    
    def heapifyDown(self, index):
        while (index * 2) <= self.currentSize :
            minChild = self.minChild(index)
            if self.list[index].weight > self.list[minChild].weight: 
                self.list[index], self.list[minChild] = self.list[minChild], self.list[index]
            index = minChild

    def minChild(self, index):
        if (index * 2)+1 > self.currentSize:
            return index * 2
        else:
            if self.list[index*2].weight < self.list[(index*2)+1].weight:
                return index * 2
            else:
                return (index * 2) + 1
 
    def extractMin(self):
        
        if len(self.list) == 1:
            return None
        minEl = self.list[1]
        self.list[1] = self.list[self.currentSize]
        *self.list, _ = self.list
        self.currentSize -= 1
        self.heapifyDown(1)
        return minEl

    def print(self):
        for i in range(1, (self.currentSize//2)+1):
            
            print(" PARENT: "+ str(self.list[i].index) + "(w." + str(self.list[i].weight)+") LEFT CHILD: "+ str(self.list[2*i].index) + "(w." +
                                str(self.list[2 * i].weight) + ")", end="")
            if 2*i+1 <= self.currentSize : 
                print(" RIGHT CHILD: " + str(self.list[2*i+1].index) + "(w." + str(self.list[2 * i + 1].weight) + ")")
            else:
                print("")
            