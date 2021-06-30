from data_structures.karger_graph import KargerGraph
import math
import numpy.random as rnd
from copy import deepcopy
import gc
import time
import sys

sys.path.append('../')


class KargerStein:
    def __init__(self, G: KargerGraph):
        self.G = G
    
    """
    Input: vettore dei pesi cumulativi C

    Permette di scegliere randomicamente un certo valore r e restituisce, 
    tramite la ricerca binaria, la posizione di tale valore nel 
    vettore dei pesi cumulativi C.
    """
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

    """
    Input:  W: matrice di adiacenza pesata
            D: vettore dei gradi pesati dei vertici

    Permette di sceglie un lato del grafo G in tempo lineare rispetto al 
    numero di vertici del grafo. Per determinare i vertici, questa procedura 
    utilizza il metodo random_select.
    """
    def edge_select(self, D, W):
        C_D = []
        for i in range(1, len(D) + 1):
            acc = 0
            for j in range(1, i):
                acc += D[j]
            C_D.append(acc)

        u = self.random_select(C_D)

        C_W = []
        for i in range(1, len(D) + 1):
            acc = 0
            for j in range(1, i):
                acc += W[u][j]
            C_W.append(acc)

        v = self.random_select(C_W)

        return (u, v)

    """
    Input:  W: matrice di adiacenza pesata
            D: vettore dei gradi pesati dei vertici
            u, v: vertici
            n: numero di vertici nel grafo G

    Effettua la contrazione del lato scelto.
    """
    def contract_edge(self, D, W, u, v, n: int):
        D[u] = D[u] + D[v] - 2 * W[u][v]
        D[v] = 0
        n = n - 1
        W[u][v] = W[v][u] = 0

        for w in range(1, self.G.n_vertices + 1):
            if w != u and w != v:
                W[u][w] += W[v][w]
                W[w][u] += W[w][v]
                W[v][w] = W[w][v] = 0

        return n

    """
    Input:  W: matrice di adiacenza pesata
            D: vettore dei gradi pesati dei vertici
            k: numero di vertici da contrarre

    Definisce l'operazione completa di contrazione, aggiornando 
    tutte le strutture dati.
    """
    def contract(self, D, W, k: int):
        n = 0
        for d in D:
            if d != 0:
                n += 1

        n_i = 0
        for i in range(0, n - k):
            (u, v) = self.edge_select(D, W)
            n_i = self.contract_edge(D, W, u, v, n)
        return D, W, n_i

    """
    Input:  W: matrice di adiacenza pesata
            D: vettore dei gradi pesati dei vertici
            n: numero di vertici nel grafo G

    Corrisponde al metodo full_contraction dell'algoritmo di Karger, 
    però ottenendo un vantaggio dal punto di vista 
    computazionale e la possibilità di essere applicato per grafi pesati.
    """
    def recursive_contract(self, D, W, n: int):
        if n <= 6:
            D_prime, W_prime, _ = self.contract(D, W, 2)

            u, v = 0, 0
            for i in range(len(D_prime)):
                if u == 0 and D_prime[i] != 0:
                    u = i
                elif u != 0 and v == 0 and D_prime[i] != 0:
                    v = i

            # Ritorna il peso dell\'unico arco (u, v) in G_prime
            return W_prime[u][v]

        t = math.ceil(n / math.sqrt(2) + 1)

        w = []
        for i in range(1, 3):
            D_i, W_i, n_i = self.contract(D, W, t)
            w.append(self.recursive_contract(D_i, W_i, n_i))

        return min(w[0], w[1])

    """
    Input:  threshold_in_seconds:   valore in secondi per indicare la soglia 
                                    oltre la quale l'esecuzione dell'algoritmo
                                    viene interrotta

    Questa procedura ricorsiva richiama recursive_contract un numero sufficiente 
    di volte per poter garantire la correttezza in alta probabilità.
    """
    def algorithm(self, threshold_in_seconds=math.inf):
        # Calcola il vettore D
        self.G.calculate_weighted_degrees_vertices()

        W = self.G.W
        D = self.G.D

        is_threshold_activated = False
        discovery_time = 0
        minimum = math.inf
        k_min = 0
        k = round((math.log(self.G.n_vertices, 2)) ** 2)

        starting_total_time = starting_discovery_time = time.perf_counter_ns()
        gc.disable()

        # Ripetizioni per l'alta probabilità
        for i in range(0, k):
            if time.perf_counter_ns() > (starting_total_time + (threshold_in_seconds * 1000000000)):
                is_threshold_activated = True
                break

            t = self.recursive_contract(deepcopy(D), deepcopy(W), deepcopy(self.G.n_vertices))

            if t < minimum:
                discovery_time = time.perf_counter_ns() - starting_discovery_time
                minimum = t
                k_min = (i + 1)

        gc.enable()
        total_time = time.perf_counter_ns() - starting_total_time

        return minimum, k, k_min, discovery_time, total_time, is_threshold_activated

    """
    Input:  threshold_in_seconds:   valore in secondi per indicare la soglia 
                                    oltre la quale l'esecuzione dell'algoritmo
                                    viene interrotta

    Questo metodo viene utilizzato per effettuare le misurazioni dell'algoritmo.
    """
    def measurements(self, threshold_in_seconds=math.inf):
        min_cut, k, k_min, discovery_time, total_time, is_threshold_activated = self.algorithm(threshold_in_seconds)

        if total_time < 1000000000:
            num_calls = 1000000000 // total_time

            starting_repetitions_total_time = time.perf_counter_ns()
            repetitions_discovery_time = 0
            for j in range(0, num_calls):
                min_cut, k, k_min, discovery_time, total_time, is_threshold_activated = self.algorithm(threshold_in_seconds)
                repetitions_discovery_time += discovery_time
            repetitions_total_time = time.perf_counter_ns() - starting_repetitions_total_time

            return min_cut, k, k_min, (repetitions_discovery_time / num_calls), (repetitions_total_time / num_calls), num_calls, is_threshold_activated
        else:
            return min_cut, k, k_min, discovery_time, total_time, 1, is_threshold_activated