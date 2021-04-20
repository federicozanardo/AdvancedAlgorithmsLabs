import copy
import sys

sys.path.append('../')

from data_structures.disjoint_set import DisjointSet
from data_structures.graph import Graph


class MST:

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
        A = Graph()

        for i in range(len(G.V)):
            A.add_vertex(i + 1)

        self._mergeSort(G.E, 0, len(G.E) - 1)

        for (u, v, w) in G.E:
            if self._is_acyclic(A, (u, v, w)):
                A.add_edge(u, v, w)

            # Ottimizzazione: mi fermo quando ho aggiunto n - 1 archi
            if len(A.E) == (len(G.V) - 1):
                break

        return A

    def _is_acyclic(self, A: Graph, e):
        (u, v, w) = e
        A.add_edge(u, v, w)
        flag = self.isCyclic(A)
        A.remove_edge(u, v, w)
        return not flag

    # Returns true if the graph
    # contains a cycle, else false.
    def isCyclic(self, G):

        # Mark all the vertices
        # as not visited
        visited = [False] * (len(G.V) + 1)

        # Call the recursive helper
        # function to detect cycle in different
        # DFS trees
        for i in range(len(G.V)):

            # Don't recur for u if it
            # is already visited
            if not visited[(i + 1)]:
                if self.isCyclicUtil(G, (i + 1), visited, -1):
                    return True

        return False

    def isCyclicUtil(self, G, v, visited, parent):
        # Mark the current node as visited
        visited[v] = True

        # Recur for all the vertices
        # adjacent to this vertex
        for e in G.graph[v]:
            (u, w) = e

            # If the node is not
            # visited then recurse on it
            if not visited[u]:
                if self.isCyclicUtil(G, u, visited, v):
                    return True

            # If an adjacent vertex is
            # visited and not parent
            # of current vertex,
            # then there is a cycle
            elif parent != u:
                return True

        return False

    # Pseudo-codice Kruskal con Union-Find
    #
    # Complessità temporale: O(m * log(n))
    #
    # Kruskal-Union-Find(G, w)
    #   A = empty_set
    #   for each vertex belongs to G.V
    #     make-set(v)
    #   sort the edges of G.E into nondecreasing order by weight w
    #   for each edge (u, v) belongs to G.E, taken in nondecreasing order by weight
    #     if find-set(u) != find-set(v)
    #       A = A U {(u, v)}
    #       Union(u, v)
    #   return A
    def kruskal_union_find(self, G):
        ds = DisjointSet(len(G.V))
        A = []

        for v in G.V:
            ds.make_set(int(v))

        # Ordina i lati con merge sort (complessità: O(nlogn))
        self._mergeSort(G.E, 0, len(G.E) - 1)

        for (u, v, w) in G.E:
            if ds.find_set(int(u)) != ds.find_set(int(v)):
                A.append((u, v, w))
                ds.union_by_size(int(u), int(v))

        return A

    def _mergeSort(self, array, left, right):
        if left < right:
            m = (left + (right - 1)) // 2

            self._mergeSort(array, left, m)
            self._mergeSort(array, m + 1, right)
            self._merge(array, left, m, right)

    def _merge(self, arr, left, m, right):
        n1 = m - left + 1
        n2 = right - m

        L = [0] * n1
        R = [0] * n2

        for i in range(0, n1):
            L[i] = arr[left + i]

        for j in range(0, n2):
            R[j] = arr[m + 1 + j]

        i = 0
        j = 0
        k = left

        while i < n1 and j < n2:
            (_, _, w1) = L[i]
            (_, _, w2) = R[j]

            if int(w1) <= int(w2):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1

            k += 1

        # Copy the remaining elements of L[], if there are any
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        # Copy the remaining elements of R[], if there are any
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    def get_mst_weight(self, E):
        summation = 0

        for (u, v, w) in E:
            summation += int(w)

        return summation
