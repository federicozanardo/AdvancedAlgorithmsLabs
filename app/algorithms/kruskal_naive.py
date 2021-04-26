from data_structures.graph import Graph

from algorithms.merge_sort import MergeSort


class KruskalNaive:

    # Pseudo-codice Kruskal naive
    #
    # Complessità temporale: O(m * n)
    #
    # Kruskal-Naive(G)
    #     A = empty_set
    #     sort edges if G by cost
    #     for each edge e in nondecreasing order of cost
    #         if A U {e} is acyclic
    #             A = A U {e}
    #     return A
    def kruskal_naive(self, G):

        # Inizializzo il grafo che conterrà il Minimum Spanning Tree
        A = Graph()

        # Aggiungo tutti i vertici del grafo G al grafo A
        #
        # Complessità temporale: teta(n)
        for i in range(len(G.V)):
            A.add_vertex(i + 1)

        # Ordina i lati in base al loro peso, in ordine crescente
        #
        # Complessità temporale: teta(m * log(m)))
        merge_sort = MergeSort()
        merge_sort.algorithm(G.E, 0, len(G.E) - 1)

        # Complessità temporale: O(m * n)
        for (u, v, w) in G.E:
            if self._is_acyclic(A, (u, v, w)):
                A.add_edge(u, v, w)

            # Mi fermo quando ho aggiunto n - 1 archi
            if len(A.E) == (len(G.V) - 1):
                break

        return A

    # Controlla se il grafo in input è aciclico o meno
    #
    # Complessità temporale: O(m)
    def _is_acyclic(self, A: Graph, e):
        (u, v, w) = e

        # Controllo che l'arco che si vuole aggiungere non sia un self-loop
        if u != v:

            # Se almeno uno dei due nodi dell'arco non è presente nel grafo, sono sicuro che non introdurrà un ciclo,
            # in quanto questo arco mi porterà a scroprire almeno un nuovo nodo.
            # Se entrambi i nodi sono presenti nel grafo, allora verifico se il grafo è aciclico
            if A.graph[u] == [] or A.graph[v] == []:
                return True
            else:
                return not self.is_there_a_path(A, u, v)
        else:
            return False

    # Chiama DFS modificata
    #
    # Complessità temporale: O(m)
    def is_there_a_path(self, G, source_node, destination_node):

        # Imposto tutti i vertici come non visitati
        visited = [False] * (len(G.V) + 1)

        return self.dfs(G, source_node, destination_node, visited)

    # Si esegue una DFS modificata in modo da determinare se esiste o meno un percorso da source_node a destination_node
    #
    # Complessità temporale: O(m)
    def dfs(self, G, current_node, destination_node, visited):
        if destination_node == current_node:
            return True

        visited[current_node] = True

        for e in G.graph[current_node]:
            (u, w) = e
            if not visited[u] and self.dfs(G, u, destination_node, visited):
                return True

        return False
