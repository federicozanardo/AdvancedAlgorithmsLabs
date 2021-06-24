from data_structures.karger_graph import KargerGraph
import math
import numpy.random as rnd
from copy import deepcopy
import gc
import time
import sys

sys.path.append('../')


class KargerStein:

    def random_select(self, C):
        random = rnd.uniform(low=0, high=C[len(C) - 1], size=(1,))
        r = round(random[0])

        found = False
        start = 1
        end = len(C)
        mid = 0

        while start < end and found == False:
            mid = (start + end) // 2

            if C[mid - 1] <= r and r < C[mid]:
                found = True
            elif C[mid] <= r:
                start = mid + 1
            elif C[mid] > r:
                end = mid

        return mid

    def edge_select(self, G: KargerGraph):
        C_D = []
        for i in range(1, len(G.D) + 1):
            acc = 0
            for j in range(1, i):
                acc += G.D[j]
            C_D.append(acc)

        u = self.random_select(C_D)

        C_W = []
        for i in range(1, len(G.D) + 1):
            acc = 0
            for j in range(1, i):
                acc += G.W[u][j]
            C_W.append(acc)

        v = self.random_select(C_W)

        return (u, v)

    def contract_edge(self, G: KargerGraph, u, v):
        G.D[u] = G.D[u] + G.D[v] - 2 * G.W[u][v]
        G.D[v] = 0
        G.n_vertices = G.n_vertices - 1
        G.W[u][v] = G.W[v][u] = 0

        for w in range(1, G.n_vertices_input + 1):
            if w != u and w != v:
                G.W[u][w] += G.W[v][w]
                G.W[w][u] += G.W[w][v]
                G.W[v][w] = G.W[w][v] = 0

    def contract(self, G: KargerGraph, k: int):
        for i in range(0, G.n_vertices - k):
            (u, v) = self.edge_select(G)
            self.contract_edge(G, u, v)
        return G

    def recursive_contract(self, G: KargerGraph):
        if G.n_vertices <= 6:
            G_prime = self.contract(G, 2)

            u, v = 0, 0
            for i in range(len(G_prime.D)):
                if u == 0 and G_prime.D[i] != 0:
                    u = i
                elif u != 0 and v == 0 and G_prime.D[i] != 0:
                    v = i

            # Ritorna il peso dell\'unico arco (u, v) in G_prime
            return G_prime.W[u][v]

        t = math.ceil(G.n_vertices / math.sqrt(2) + 1)

        w = []
        for i in range(1, 3):
            G_i = self.contract(G, t)
            w.append(self.recursive_contract(G_i))

        return min(w[0], w[1])

    def algorithm(self, G: KargerGraph, threshold_in_seconds=math.inf):
        # Calcola il vettore D
        G.calculate_weighted_degrees_vertices()

        is_threshold_activated = False
        discovery_time = 0
        minimum = math.inf
        k_min = 0
        k = round((math.log(G.n_vertices, 2)) ** 2)

        starting_total_time = starting_discovery_time = time.perf_counter_ns()
        gc.disable()
        for i in range(0, k):
            if time.perf_counter_ns() > (starting_total_time + (threshold_in_seconds * 1000000000)):
                is_threshold_activated = True
                break

            t = self.recursive_contract(deepcopy(G))

            if t < minimum:
                discovery_time = time.perf_counter_ns() - starting_discovery_time
                minimum = t
                k_min = (i + 1)

        gc.enable()
        total_time = time.perf_counter_ns() - starting_total_time

        return minimum, k, k_min, discovery_time, total_time, is_threshold_activated

    def measurements(self, G: KargerGraph, threshold_in_seconds=math.inf):
        min_cut, k, k_min, discovery_time, total_time, is_threshold_activated = self.algorithm(G, threshold_in_seconds)

        if total_time < 1000000000:
            num_calls = 1000000000 // total_time

            starting_repetitions_total_time = time.perf_counter_ns()
            repetitions_discovery_time = 0
            for j in range(0, num_calls):
                min_cut, k, k_min, discovery_time, total_time, is_threshold_activated = self.algorithm(G, threshold_in_seconds)
                repetitions_discovery_time += discovery_time
            repetitions_total_time = time.perf_counter_ns() - starting_repetitions_total_time

            return min_cut, k, k_min, (repetitions_discovery_time / num_calls), (repetitions_total_time / num_calls), num_calls, is_threshold_activated
        else:
            return min_cut, k, k_min, discovery_time, total_time, 1, is_threshold_activated