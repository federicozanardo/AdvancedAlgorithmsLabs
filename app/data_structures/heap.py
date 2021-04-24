#!/user/bin/env python3

import sys
from collections import defaultdict
sys.path.append('../')
"""
    Heap (binary)
    -----------------------------------------
"""

"""
Classe Node
node: Node = (index: int, weight: int)
    index = numero del vertice
    weight = peso del vertice
"""
class Node : 

    def __init__(self, index, weight):
        self.index = index
        self.weight = weight
    
    # Funzione di utilità che a partire da un oggetto node lo ritorna in forma di tupla (index, weight)
    def toTuple(self):
        return (self.index, self.weight)


"""
Classe Heap
heap: Heap = (list: Node[], currentSize: int)
    Node[] = lista di nodi del grafo
    currentSize = dimensione dello Heap
"""
class Heap:

    def __init__(self):
        self.list = [Node(0, float('-inf'))] # nodo fittizio per avere array che partono da 1
        self.mapList = defaultdict(list)
        self.currentSize = 0
    
    """
    parent(index: int) : Node
        index = indice del nodo corrente
    Ritorna il parent del nodo con indice index
    """
    def parent(self, index):
        return list[index//2]

    """
    right(index: int) : Node
        index = indice del nodo corrente
    Ritorna il figlio destro del nodo con indice index
    """
    def right(self, index):
        return list[(index * 2) + 1]
    
    """
    left(index: int) : Node
        index = indice del nodo corrente
    Ritorna il figlio sinistro del nodo con indice index
    """
    def left(self, index):
        return list[(index * 2)]

    """
    heapifyUp(index: int) : void
        index = indice del nodo da cui eseguire heapify
    Esegue la procedura heapify dello heap dal basso verso l´alto
    """
    def heapifyUp(self, index):
        # while(index>0):
        #     el = self.list[index]
        #     pIndex = index // 2
        #     parent = self.list[pIndex]
        #     if parent.weight < el.weight:
        #         break
            
        #     self.mapList[self.list[pIndex].index] = index
        #     self.list[index] = parent
        #     self.list[pIndex] = el
        #     index = pIndex
        # return index 

    # def heapifyUp(self, index):
        constInd = index
        while index // 2 > 0:
            if self.list[index].weight < self.list[index // 2].weight:
                self.mapList[self.list[(index)].index] = index // 2
                self.mapList[self.list[index // 2].index] = index
                constInd = index // 2
                self.list[index], self.list[index // 2] = self.list[index // 2], self.list[index]
            index //= 2
        return constInd
    
    
    """
    search(index: int) : boolean
        index = indice del nodo da cercare
    Restituisce True se il nodo di indice index è presente nello heap, altrimenti restituisce false
    """
    def search(self, index):
        if index in self.mapList.keys():
            return True
        return False
    
    """
    searchAndUpdateWeight(index: int, newWeight: int) : void
        index = indice del nodo da aggiornare
        newWeight = nuovo peso del nodo
    Aggiorna lo heap con il nuovo valore del nodo

    Il funzionamento è il seguente:
    Per ogni nodo nella lista di nodi dello heap
        Se il nodo è quello cercato
            peso del nodo = -inf
            esegui heapifyUp dal nodo cercato per farlo andare in cima allo heap
            aggiorna il peso del nodo in cima allo heap
            esegui heapifyDown per garantire la proprietà dello heap
        Altrimenti
            aggiorna l´indice a cui cercare il nodo
    """
    def searchAndUpdateWeight(self, index, newWeight):
        print(index)
        i = self.mapList[index]
        for node in self.list:
            print(node.toTuple())
        self.list[i].weight = float('-inf')
        self.heapifyUp(i)
        self.list[1].weight = newWeight
        self.heapifyDown(1)

        # i = 0
        # for node in self.list:
        #     if i == 0:
        #         i += 1
        #         continue
        #     if node.index == index:
        #         self.list[i].weight = float('-inf')
        #         self.heapifyUp(i)
        #         self.list[1].weight = newWeight
        #         self.heapifyDown(1)
        #         return
        #     else: 
        #         i += 1
            
    """
    insert(node: Node) : void
        node = nodo da inserire
    Inserisce il nuovo nodo nello heap ed esegue heapifyUp per garantire la proprietà dello heap
    """
    def insert(self, node):
        self.list.append(node)
        self.currentSize += 1
        pos = self.heapifyUp(self.currentSize)
        self.mapList[node.index] = pos
    
    """
    heapifyDown(index: int) : void
        index = indice del nodo da cui eseguire heapify
    Esegue la procedura heapify dello heap dall´alto verso il basso
    """
    def heapifyDown(self, index):
        # left = 2 * index
        # right = 2 * index +1
        # smallest = index
        # length = self.currentSize

        # if(left <= length and self.list[left] and self.list[left].weight < self.list[smallest].weight):
        #     smallest = left

        # if(right <= length and self.list[right] and self.list[right].weight < self.list[smallest].weight):
        #     smallest = right

        # self.mapList[self.list[smallest].index] = index
        # self.mapList[self.list[index].index] = smallest

        # if smallest != index:
        #     self.list[smallest], self.list[index] = self.list[index], self.list[smallest]

        # self.heapifyDown(smallest)

        while (index * 2) <= self.currentSize :
            minChild = self.minChild(index)
            if self.list[index].weight > self.list[minChild].weight: 
                self.mapList[self.list[minChild].index] = index
                self.mapList[self.list[index].index] = minChild
                self.list[index], self.list[minChild] = self.list[minChild], self.list[index]
            index = minChild

    """
    minChild(index: int) : int
        index = indice del nodo di cui restituire il figlio minore
    Ritorna l´indice del nodo figlio del nodo di indice index di peso minore
    """
    def minChild(self, index):
        if (index * 2)+1 > self.currentSize:
            return index * 2
        else:
            if self.list[index*2].weight < self.list[(index*2)+1].weight:
                return index * 2
            else:
                return (index * 2) + 1
 
    """
    extractMin() : Node
    Ritorna il nodo di peso minimo dello heap che, poiché questo è un minHeap, coincide con il primo elemento

    Il funzionamento è il seguente:
    Se la lista di nodi dello heap ha lunghezza 1
        La lista è vuota per definizione della classe e quindi non ritorna niente
    Altrimenti
        memorizza il nodo di peso minore, ossia il primo nodo dello heap
        sposta l´ultimo elemento dello heap in testa
        elimina l´ultimo elemento dello heap
        diminuisci la dimensione dello heap
        esegui heapifyDown per garantire la proprietà dello heap
        ritorna il nodo di peso minore precedentemente salvato
    """
    def extractMin(self):
        if len(self.list) == 1:
            return None
        minEl = self.list[1]
        del self.mapList[minEl.index]
        self.list[1] = self.list[self.currentSize]
        self.mapList[self.list[self.currentSize].index] = 1
        # *self.list, _ = self.list
        del self.list[self.currentSize]
        self.currentSize -= 1
        self.heapifyDown(1)
        return minEl

    """
    print() : void
    Funzione di utilità per stampare lo heap
    """
    def print(self):
        for i in range(1, (self.currentSize//2)+1):
            
            print(" PARENT: "+ str(self.list[i].index) + "(w." + str(self.list[i].weight)+") LEFT CHILD: "+ str(self.list[2*i].index) + "(w." +
                                str(self.list[2 * i].weight) + ")", end="")
            if 2*i+1 <= self.currentSize : 
                print(" RIGHT CHILD: " + str(self.list[2*i+1].index) + "(w." + str(self.list[2 * i + 1].weight) + ")")
            else:
                print("")
            