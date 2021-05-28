import math
import sys
sys.path.append('../')


class DisjointSet:
    def __init__(self, n: int):

        # Questo array rappresenta i parent dei vari nodi
        self.parents = [math.inf] * (n + 1)

        # Questo array rappresenta le varie size dei nodi
        self.sizes = [0] * (n + 1)

    # Aggiungo un nodo alla struttura dati
    #
    # Complessità temporale: teta(1)
    def make_set(self, x: int):
        self.parents[x] = x
        self.sizes[x] = 1

    # Dato un nodo, permette di determinare quale sia il nodo parent dell'albero a cui appartiene tale nodo
    #
    # Complessità temporale: O(log n)
    def find_set(self, x: int):
        root = x

        while self.parents[root] != root:
            root = self.parents[root]

        return root

    # Permette di unire due nodi sotto un unico albero
    #
    # Complessità temporale: O(log n)
    def union_by_size(self, x: int, y: int):
        i = self.find_set(x)
        j = self.find_set(y)

        if i != j:
            if self.sizes[i] >= self.sizes[j]:
                self.parents[j] = i
                self.sizes[i] += self.sizes[j]
            else:
                self.parents[i] = j
                self.sizes[j] += self.sizes[i]
