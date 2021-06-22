from collections import defaultdict
from data_structures.graph import Graph
from data_structures.max_heap import MaxHeap, Node
from copy import deepcopy

class StoerWagner:

  def algorithm(self, G: Graph):
    self.backupG = deepcopy(G)
    res = self.globalMinCut(G)
    return res[1][0][1]
    
  def stMinCut(self, G: Graph):

    Q = MaxHeap()
    key = defaultdict(list)

    for node in G.V:
      key[node] = 0
      Q.insert(Node(node, key[node]))

    s = t = None

    while Q.currentSize != 0:
      u = (Q.extractMax()).toTuple()
      s = t
      t = u
      for (v, w) in G.graph[u[0]]:
        if Q.search(v):         
          key[v] = key[v] + w
          #print("v=", v, " w=", w, " key[v]=", key[v])
          Q.searchAndUpdateWeight(v, key[v])

    V_diff = []
    for x in G.V:
        if(x != t[0]):
          V_diff.append(x)

   # print((V_diff, [t]), s[0], t[0])
    return (V_diff, [t]), s[0], t[0]


  def globalMinCut(self, G: Graph):
    if len(G.V) == 2:
      v1 = G.V.pop()
      v2 = G.V.pop()
      G.V.add(v2)
      G.V.add(v1)
      #print('base case=', v1, v2)
      return ([v1], [(v2, G.weightBetween(v1, v2))])
    
    else:
      (C1, s, t) = self.stMinCut(G)

      #print('C1=', C1[1], 's=', s, 't=', t)

      contractedG = self.contractGraph(G, s, t)


      C2 = self.globalMinCut(contractedG)
      # print(self.weightMinCut(C1), self.weightMinCut(C2))
     # if type(C2[1][0]) is int:
        #exit(C2)
      if type(C2[1][0]) is tuple:
        if self.weightMinCut(C1) <= self.weightMinCut(C2):
          return C1
        else:
          return C2
      else: # sono nel caso base
        v1 = G.V.pop()
        v2 = G.V.pop()
        G.V.add(v2)
        G.V.add(v1)
        nuovo = ([v1], [(v2, self.backupG.graph[v1][0][1])])
        return nuovo


  def weightMinCut(self, C: any):
    V, t = C
    #print("t=", t)
    sum = 0
    t = t[0]
    # if type(t) is tuple:
    return t[1]
    # else:
    #   return float('inf')

    # for (u, w) in self.backupG.graph[t]:
    #   sum+=w

    # return sum

    for v in self.backupG.V:
      for (u,w) in self.backupG.graph[v]:
        if u == t:
          sum += w
    return sum

  def contractGraph(self, G: Graph, s, t):
    for (u,w) in G.graph[t]:
      if u == s:
        G.remove_edge(t, u, w)
    for (u, w) in G.graph[t]:
      if u != s:
        G.add_edge(s, u, w)
        # newValues[u] = newValues[u] + w
    # for u in newValues.keys():
    #   G.add_edge(s, u, newValues[u])
    G.remove_node(t)

    return G