from algorithms.prim import Prim
from data_structures.graph import Graph


class TwoApproximation:
    def algorithm(self, graph: Graph):
        starting_node = 1
        prim = Prim()
        key, mst = prim.prim_mst(graph, starting_node)

        tree = {}

        # Convert the MST result to a tree-like structure
        # Complexity: O(m)
        for index in mst:
            if mst[index] != None:
                (parent, w) = mst[index]
                if parent not in tree:
                    tree[parent] = []
                tree[parent].append(index)

        print('Tree')
        print(tree)
        print()

        preorder_result = []
        sum = self.preorder(graph, tree, starting_node, preorder_result)

        # Add the weight of the edge between the starting node and the last node of the MST to create a cycle
        sum += int(graph.get_weight(preorder_result[len(preorder_result) - 1], 1))

        print('Result: {}'.format(str(sum)))

    # Complexity: teta(n)
    def preorder(self, graph: Graph, tree, v, result):
        if v not in result:
            result.append(v)
        if v in tree:
            for u in tree[v]:
                return self.preorder(graph, tree, u, result) + int(
                    graph.get_weight(v, u))  # THE GRAPH MUST USE THE ADJACENCY MATRIX TO HAVE THIS TIME COMPLEXITY!
        else:
            return 0
