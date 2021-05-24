"""
Module - measurements.single

Modulo di misurazione dei dataset con output del tempo di esecuzione dei singoli

"""

from random import randint
import gc
# import matplotlib.pyplot as plt
from data_structures.heap import Heap, Node
from data_structures.tsp import TSP
from data_structures.disjoint_set import DisjointSet
from algorithms.utils import populateTSPFromFile as populate
from algorithms.utils import loadFromFolder
from algorithms.utils import loadFromFile
from algorithms.utils import bcolors as col
from algorithms.hk import HeldKarp
from algorithms.nearestneighbor import NearestNeighbor
from algorithms.two_approximation import TwoApproximation
from os import walk, path
import time

"""
Esecuzione degli algoritmi in tutti i dataset

    graphs      =   grafi dei dataset da eseguire
    lock        =   accesso condiviso dei threads per la scrittura in append dei file (eventuale implementazione)

"""
def executeTheSuperFancyFunctionToCalculateMegaComplexTSPs(tsps, lock):
    outputfilePostfix = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime()) + '.csv'

    #======= 2 approx =======
    print('Executing 2 approximation...')
    datasetNumber = 1
    output = './output_2approx_' + outputfilePostfix

    for tsp in tsps:
        executeSingleGraphCalculus(output, '2ap' , tsp, datasetNumber, lock)
        datasetNumber+=1

    #======= Nearest Neighbors =======
    print('Executing Nearest Neighbors...')
    datasetNumber = 1
    output = './output_nearest_neighbor' + outputfilePostfix

    for tsp in tsps:
        executeSingleGraphCalculus(output, 'nn', tsp, datasetNumber, lock)
        datasetNumber+=1

    #======= Held and Karp =======
    print('Executing Held and Karp...')
    datasetNumber = 1
    output = './output_heldkarp_' + outputfilePostfix

    for tsp in tsps:
        executeSingleGraphCalculus(output, 'hk', tsp, datasetNumber, lock)
        datasetNumber+=1

"""
Esecuzione di un singolo grafo 

    outputfile      =   file di salvataggio dei risultati
    algoname        =   tipo algoritmo da eseguire
    graph           =   grafo di partenza in input
    filenumber      =   numero del dataset
    fileResultLock  =   accesso condiviso dei threads per la scrittura in append dei file (eventuale implementazione)

"""
def executeSingleGraphCalculus(outputfile, algoname, tsp, filenumber, fileResultLock):
    executionTimes = 1

    localStartTime = time.perf_counter_ns()
    gc.disable()

    if algoname == '2ap':
        final = TwoApproximation()
        res = final.algorithm(tsp)

    elif algoname == 'nn':
        res = NearestNeighbor().algorithm(tsp)

    elif algoname == 'hk':
        hk = HeldKarp()
        res = hk.hk_init(tsp)

    else:
        pass

    gc.enable()
    localEndTime = time.perf_counter_ns() - localStartTime

    # Se il tempo di esecuzione è minore di 1 secondo, lo eseguo n volte
    # tale da avvicinarmi a 1 secondo
    # e ne faccio la media

    if localEndTime <= 1000000000: 
        numCalls = 1000000000//localEndTime
        loopStartTime = time.perf_counter_ns()
        gc.disable()
        for i in range(0, numCalls):

            if algoname == '2ap':
                final = TwoApproximation()
                res = final.algorithm(tsp)

            elif algoname == 'nn':
                res = NearestNeighbor().algorithm(tsp)

            elif algoname == 'hk':
                hk = HeldKarp()
                res = hk.hk_init(tsp)

        gc.enable()
        loopEndTime = time.perf_counter_ns() - loopStartTime
        rightTime = loopEndTime/numCalls
        executionTimes = numCalls
    else:
        rightTime = localEndTime

    # OUTPUT
    # ======================================================================
    # dataset name | tsp result | nano seconds time | seconds time | exe times
    # ======================================================================

    with fileResultLock:
        file_object = open(outputfile, 'a')
        file_object.write("{:<15}{:<12}{:<20}{:<20}{:<20}".format(tsp.name, str(int(res)), str(rightTime), '{:.7f}'.format(rightTime/1000000000), str(executionTimes)))
        file_object.write('\n')
        file_object.close()