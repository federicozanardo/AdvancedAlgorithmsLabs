from collections import defaultdict
from data_structures.graph import Graph
from data_structures.max_heap import MaxHeap, Node
from copy import deepcopy

class StoerWagner:

  def algorithm(self, G: Graph):
    self.G = G
    V = deepcopy(G.V)
    return self.globalMinCut(V)


  def stMinCut(self, V: list):
    Q = MaxHeap()
    key = defaultdict(list)

    for node in V:
      key[node] = 0
      Q.insert(Node(node, key[node]))

    s = None
    t = None

    # print(len(V))

    while Q.currentSize != 0:
      u = (Q.extractMax()).toTuple()
      s = t
      t = u
      for (v, w) in self.G.graph[u[0]]:
        if Q.search(v):
          key[v] += w
          Q.searchAndUpdateWeight(v, key[v])

    V_diff = []
    for x in V:
        if(x != t[0]):
          V_diff.append(x)

    return V_diff, s[0], t[0]


  def globalMinCut(self, V: list):
    if len(V) == 2:
      return V[0], V[1]
    else:
      (C1, s, t) = self.stMinCut(V)

      V2 = []
      for x in V:
        if(x != s and x != t):
          V2.append(x)

      #print(len(V2))

      C2 = self.globalMinCut(V2)

      # print(len(V2))
      # print(len(C2))
      # print(C2[0], C2[1])

  	  # # sommatoria = somma peso archi a partire da V nodi
      # # C1 = sommatoria(C1)
      # # C2 = sommatoria(C1 - sommatoria({s, t}))

      #print(self.niceSummatoryBecauseItIsClearHowItWorks(C1) <= self.niceSummatoryBecauseItIsClearHowItWorks(C2))

      if self.niceSummatoryBecauseItIsClearHowItWorks(C1) <= self.niceSummatoryBecauseItIsClearHowItWorks(C2):
        return C1
      else:
        return C2


  def niceSummatoryBecauseItIsClearHowItWorks(self, V: list):
    sum = 0
    for v in V:
      for (u,w) in self.G.graph[v]:
        if u in V:
          sum += w
    return sum