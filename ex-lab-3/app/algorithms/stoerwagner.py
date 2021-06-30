from collections import defaultdict
from data_structures.graph import Graph
from data_structures.max_heap import MaxHeap, Node
from copy import deepcopy

class StoerWagner:
  def algorithm(self, G: Graph):

    """
    backupG: Graph = copia profonda del grafo di partenza per il calcolo dei pesi degli archi
    res: tuple = tupla contenente i risultati dell'esecuzione dell'algoritmo
    """
    backupG = deepcopy(G)
    res = self.globalMinCut(backupG)
    return res[1][0][1]
    

  def stMinCut(self, G: Graph):

    """
    Q: MaxHeap = maxheap contenente i nodi del grafo
    key: defaultdict(list) = mappa delle chiavi. Un valore è in forma key[nodo] = peso_nodo
    """
    Q = MaxHeap()
    key = defaultdict(list)

    """
    Inizializzazione
    * Per ogni nodo node di G, key[node] = 0
    * Q <- V
    * s = null, t = null: inizializzazione dei nodi s e t che la funzione deve ritornare
    """
    for node in G.V:
      key[node] = 0
      Q.insert(Node(node, key[node]))
    s = t = None

    """
    Calcolo dei nodi s e t da ritornare
    Finché l'heap Q non è vuoto
        estrai il nodo di peso massimo
        s <- t ricavato dall'iterazione precedente
        t <- u
        Per ogni nodo v con peso w adicente a u
          Se il nodo è presente in Q
            key[v] += w
            aggiorna Q con il nuovo nodo di index v e peso key[v]
    """
    while Q.currentSize != 0:
      u = (Q.extractMax()).toTuple()
      s = t
      t = u
      for (v, w) in G.graph[u[0]]:
        if Q.search(v):
          key[v] = key[v] + w
          Q.increaseKey(v, key[v])

    """
    Rimozione di t da G.V
    Ogni nodo diverso da t viene inserito in una lista di nodi ausiliaria
    """
    V_diff = []
    for x in G.V:
        if(x != t[0]):
          V_diff.append(x)

    """
    Ritorno della funzione
    La funzione ritorna:
    * Un s-t mincut composto da (V_diff, [t]) con V_diff = G.V - {t}
    * I due nodi s e t
    """
    return (V_diff, [t]), s[0], t[0]


  def globalMinCut(self, G: Graph):

    """
    Caso base
    Se la lista di nodi contiene solo due nodi, questi vengono ritornati.
    In particolare viene ritornata una tupla 
    ([v1], [(v2, G.totalWeightCost(v1, v2))]), dove
        * v1 e v2 sono i due nodi corrispondenti alle due partizioni di G.V
        * totalWeightCost(v1, v2) è il peso dell'arco tra v1 e v2
    """
    if len(G.V) == 2:
      v1 = G.V.pop()
      v2 = G.V.pop()
      G.V.add(v2)
      G.V.add(v1)
      return ([v1], [(v2, G.totalWeightCost(v1, v2))])

    else:

      """
      Passo ricorsivo
      Viene invocato stMinCut su G
      Viene contratto il grafo rispetto a s e t tramite la funzione contractGraph
      Viene invocato globalMinCut sul grafo contratto
      A fondo ricorsione vengono fatti i confronti tra C1 e C2
      """
      (C1, s, t) = self.stMinCut(G)
      contractedG = self.contractGraph(G, s, t)
      C2 = self.globalMinCut(contractedG)
      if self.weightMinCut(C1) <= self.weightMinCut(C2):
        return C1
      else:
        return C2

  # Ritorna il peso del minCut
  def weightMinCut(self, C: any):
    V, t = C
    return t[0][1]


  def contractGraph(self, G: Graph, s, t):
    """
    Contrazione del grafo rispetto a s e t
    Ogni lato adiacente a entrambi i nodi s e t viene eliminato
    Ogni lato adiacente a t viene "spostato" su s
    Viene eliminato il nodo t e viene ritornato il grafo contratto
    """
    for (u,w) in G.graph[t]:
      if u == s:
        G.remove_edge(t, u, w)
    for (u, w) in G.graph[t]:
      if u != s:
        G.add_edge(s, u, w)
    G.remove_node(t)
    return G
