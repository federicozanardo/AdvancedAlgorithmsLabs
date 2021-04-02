from AdvancedAlgorithmsLab1.app.data_structures.disjoint_set import DisjointSet


class MST:

    # Pseudo-code
    #
    # Kruskal(G, w)
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
            ds.make_set(v)

        self._mergeSort(G.E, 0, len(G.E) - 1)

        for (u, v, w) in G.E:
            if ds.find_set(u) != ds.find_set(v):
                A.append((u, v, w))
                ds.union_by_size(u, v)

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

            if w1 <= w2:
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
