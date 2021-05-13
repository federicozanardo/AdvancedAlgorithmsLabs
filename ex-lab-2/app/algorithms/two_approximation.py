from algorithms.prim import Prim
from data_structures.tsp import TSP


class TwoApproximation:
    def algorithm(self, graph: TSP):
        print('[TwoApproximation] AdjMatrix')
        for i in range(1, len(graph.adjMatrix)):
            # pass
            print(graph.adjMatrix[i])
        print()

        starting_node = 1
        prim = Prim()
        _, mst = prim.prim_mst(graph, starting_node)
        print('[TwoApproximation] Result of Prim: {}'.format(mst))

        tree = {}

        # Convert the MST result to a tree-like structure
        # Complexity: O(m)
        for index in mst:
            if mst[index] != None:
                (parent, _) = mst[index]
                # print('mst[index]: ', mst[index])
                if parent not in tree:
                    tree[parent] = []
                tree[parent].append(index)

        print('[TwoApproximation] Tree: {}\n'.format(tree))

        preorder_result = []
        # summation = self.preorder(graph, tree, starting_node, preorder_result)
        self.preorder(graph, tree, starting_node, preorder_result)
        preorder_result.append(starting_node)
        print('[TwoApproximation] Result of preorder: ', preorder_result)

        # Add the weight of the edge between the starting node and the last node of the MST to create a cycle
        # sum += int(graph.get_weight(preorder_result[len(preorder_result) - 1], 1))
        # summation += int(graph.adjMatrix[preorder_result[len(preorder_result) - 1]][1])

        summation = 0
        for i in range(len(preorder_result) - 1):
            # print('Weight ({}, {}): {}'.format(str(i), str(i + 1), str(graph.adjMatrix[preorder_result[i]][preorder_result[i + 1]])))
            summation += graph.adjMatrix[preorder_result[i]][preorder_result[i + 1]]

        print('[TwoApproximation] Result: {}'.format(str(summation)))

        return int(summation)

    # Complexity: teta(n)
    def preorder(self, graph: TSP, tree, v, result):
        if v not in result:
            result.append(v)
        if v in tree:
            for u in tree[v]:
                self.preorder(graph, tree, u, result)

    # def preorder(self, graph: TSP, tree, v, result):
    #     if v not in result:
    #         result.append(v)
    #     if v in tree:
    #         summation = 0
    #         for u in tree[v]:
    #             # print()
    #             # print(tree[v])
    #             # print()
    #             #graph.get_weight(v, u))  # THE GRAPH MUST USE THE ADJACENCY MATRIX TO HAVE THIS TIME COMPLEXITY!
    #             print('Weight ({}, {}): {}'.format(str(v), str(u), str(graph.adjMatrix[v][u])))
    #             summation = self.preorder(graph, tree, u, result) + int(graph.adjMatrix[v][u])
    #         return summation
    #     else:
    #         return 0

# berlin52   10403   10402   10403
# burma13    4003    4003    4003
# ch150      9202    9053    9202 *
# d493               45114   45717
# dsj1000            25526005    25526009
# eil51              567     615
# gr202      52615   52615   52615
# gr229      179335  179335  179335
# kroA100    30516   30536   30516 *
# kroD100    28599   28599   28599
# pcb442     75763   74856   76004 *
# ulysses16  7788    7788    7788
#ulysses22  8308    8308    8308
