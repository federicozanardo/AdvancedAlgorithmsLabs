from algorithms.prim import Prim
from data_structures.tsp import TSP


class TwoApproximation:
    def algorithm(self, graph: TSP):
        starting_node = 1
        prim = Prim()
        _, mst = prim.prim_mst(graph, starting_node)

        tree = {}

        # Convert the MST result to a tree-like structure
        # Complexity: O(m)
        for index in mst:
            if mst[index] != None:
                (parent, _) = mst[index]
                if parent not in tree:
                    tree[parent] = []
                tree[parent].append(index)

        # print('[TwoApproximation] Tree: {}\n'.format(tree))

        preorder_result = []
        self.preorder(graph, tree, starting_node, preorder_result)
        preorder_result.append(starting_node)
        # print('[TwoApproximation] Result of preorder: ', preorder_result)
        # print(preorder_result)

        summation = 0
        for i in range(len(preorder_result) - 1):
            # print('Weight ({}, {}): {}'.format(str(i), str(i + 1), str(graph.adjMatrix[preorder_result[i]][preorder_result[i + 1]])))
            summation += graph.adjMatrix[preorder_result[i]][preorder_result[i + 1]]

        return int(summation)

    # Complexity: teta(n)
    def preorder(self, graph: TSP, tree, v, result):
        if v not in result:
            result.append(v)
        if v in tree:
            for u in tree[v]:
                self.preorder(graph, tree, u, result)

# SENZA ROUND
#             Our     TS     Other
# berlin52   10403   10402   10403  * TS
# burma14    4003    4003    4003
# ch150      9202    9053    9202   * TS
# d493       45375   45114   45717  **
# dsj1000    25526009   25526005    25526009    * TS
# eil51      615     567     615    * TS
# gr202      52615   52615   52615
# gr229      179335  179335  179335
# kroA100    30516   30536   30516  * TS
# kroD100    28599   28599   28599
# pcb442     75763   74856   76004  **
# ulysses16  7788    7788    7788
# ulysses22  8308    8308    8308

# CON ROUND
#             Our     TS     Other
# berlin52   10402   10402   10403  * Other
# burma14    4003    4003    4003
# ch150      9250    9053    9202   **
# d493       45585   45114   45717  **
# dsj1000    25526005   25526005    25526009    * Other
# eil51      567     567     615    * Other
# gr202      52615   52615   52615
# gr229      179335  179335  179335
# kroA100    30536   30536   30516  * Other
# kroD100    28599   28599   28599
# pcb442     75305   74856   76004  **
# ulysses16  7788    7788    7788
# ulysses22  8308    8308    8308

# Ludo
#
# 4003
# 7788
# 8308
# 605 *
# 10402
# 28599
# 30516 *
# 9126 *
# 52615
# 179335
# 72853 *
# 45595 *
# 25526005

# CON ROUND E PI NUOVO
#             Our     TS     Other
# berlin52   10402   10402   10403  * Other
# burma14    4003    4003    4003
# ch150      9250    9053    9202   **
# d493       45585   45114   45717  **
# dsj1000    25526005   25526005    25526009    * Other
# eil51      567     567     615    * Other
# gr202      52615   52615   52615
# gr229      179335  179335  179335
# kroA100    30536   30536   30516  * Other
# kroD100    28599   28599   28599
# pcb442     75305   74856   76004  **
# ulysses16  7788    7788    7788
# ulysses22  8308    8308    8308
