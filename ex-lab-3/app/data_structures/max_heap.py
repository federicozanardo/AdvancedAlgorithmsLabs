#!/user/bin/env python3

import sys
from collections import defaultdict
sys.path.append('../')
"""
    MaxHeap (binary)
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
Classe MaxHeap
maxheap: MaxHeap = (list: Node[], mapList: defaultdict(list), currentSize: int)
    list = lista di nodi del grafo
    mapList = mappa che associa indice del vertice alla sua posizione in list
    currentSize = dimensione dello Heap
"""
class MaxHeap:

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
        return self.list[index//2]

    """
    right(index: int) : Node
        index = indice del nodo corrente
    Ritorna il figlio destro del nodo con indice index
    """
    def right(self, index):
        return self.list[(index * 2) + 1]
    
    """
    left(index: int) : Node
        index = indice del nodo corrente
    Ritorna il figlio sinistro del nodo con indice index
    """
    def left(self, index):
        return self.list[(index * 2)]

    """
    heapifyUp(index: int) : void
        index = indice del nodo da cui eseguire heapify
    Esegue la procedura heapify dello heap dal basso verso l´alto
    Nel farlo aggiorna anche la mappa delle posizioni
    Ritorna la posizione in cui il nodo è stato aggiunto
    """
    def heapifyUp(self, index):
        constInd = index
        while index // 2 > 0:
            if self.list[index].weight > self.list[index // 2].weight:
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
    estrapola la posizione in list del Node con indice index
    aggiorna il peso di tale nodo a -inf
    esegue heapifyUp dal nodo cercato per farlo andare in cima allo heap
    aggiorna il peso del nodo (ora) in cima allo heap
    esegue heapifyDown per garantire la proprietà dello heap
    """
    def searchAndUpdateWeight(self, index, newWeight):
        i = self.mapList[index]
        self.list[i].weight = float('inf')
        self.heapifyUp(i)
        self.list[1].weight = newWeight
        self.heapifyDown(1)

        # i = self.mapList[index]
        # if newWeight < self.list[i].weight:
        #     print('dovrebbe essere impossibile')
        #     return False

        # self.list[i].weight = newWeight

        # while i > 1 and self.list[self.parent(i).index].weight < self.list[i].weight:
        #     self.list[i], self.list[self.parent(i).index] = self.list[self.parent(i).index], self.list[i]
        #     i = self.parent(i).index

        # i = self.mapList[index]
        # self.list[i].weight = newWeight
        # self.heapifyUp(i)
            
    """
    insert(node: Node) : void
        node = nodo da inserire
    Inserisce il nuovo nodo nello heap ed esegue heapifyUp per garantire la proprietà dello heap
    Aggiorna anche la mappa delle posizioni con la posizione restituita da heapifyUp
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
    Nel farlo aggiorna anche la mappa delle posizioni
    """
    def heapifyDown(self, index):
        while (index * 2) <= self.currentSize :
            maxChild = self.maxChild(index)
            if self.list[index].weight < self.list[maxChild].weight: 
                self.mapList[self.list[maxChild].index] = index
                self.mapList[self.list[index].index] = maxChild
                self.list[index], self.list[maxChild] = self.list[maxChild], self.list[index]
            index = maxChild

    """
    maxChild(index: int) : int
        index = indice del nodo di cui restituire il figlio minore
    Ritorna l´indice del nodo figlio del nodo di indice index di peso minore
    """
    def maxChild(self, index):
        if (index * 2)+1 > self.currentSize:
            return index * 2
        else:
            if self.list[index*2].weight > self.list[(index*2)+1].weight:
                return index * 2
            else:
                return (index * 2) + 1
 
    """
    extractMax() : Node
    Ritorna il nodo di peso massimo dello heap che, poiché questo è un maxHeap, coincide con il primo elemento

    Il funzionamento è il seguente:
    Se la lista di nodi dello heap ha lunghezza 1
        La lista è vuota per definizione della classe e quindi non ritorna niente
    Altrimenti
        memorizza il nodo di peso maggiore, ossia il primo nodo dello heap
        sposta l´ultimo elemento dello heap in testa
        elimina l´ultimo elemento dello heap
        diminuisci la dimensione dello heap
        esegui heapifyDown per garantire la proprietà dello heap
        ritorna il nodo di peso maggiore precedentemente salvato
    Inoltre, nel fare ciò aggiorna anche la mappa delle posizioni
    """
    def extractMax(self):
        if len(self.list) == 1:
            return None
        maxEl = self.list[1]
        del self.mapList[maxEl.index]
        self.list[1] = self.list[self.currentSize]
        self.mapList[self.list[self.currentSize].index] = 1
        # *self.list, _ = self.list
        del self.list[self.currentSize]
        self.currentSize -= 1
        self.heapifyDown(1)
        return maxEl


    def extractChecker(self, extracted):
        for a in self.list:
            if(extracted < a.weight):
                return False
        return True

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
            