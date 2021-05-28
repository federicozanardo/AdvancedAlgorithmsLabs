"""
Module - measurements.quartet

Modulo di misurazione dei dataset raggruppati in un quartetto 
di grafi composti dallo stesso numero di vertici

"""

import argparse
from random import randint
import gc
import math
from time import perf_counter_ns
from data_structures.heap import Heap, Node
from data_structures.graph import Graph
from algorithms.utils import populateGraphFromFile as populate
from algorithms.utils import loadFromFolder
from algorithms.utils import loadFromFile
from algorithms.utils import bcolors as col
from algorithms.utils import Loader
from algorithms.mst import MST
import sys
from os import walk, path
import time
import concurrent.futures
import multiprocessing


"""
Composizione ed esecuzione dei quartetti a partire da più dataset

    graphs          =   grafi dei dataset da eseguire
    lock  =   accesso condiviso dei threads per la scrittura in append dei file (eventuale implementazione)

"""
def executeOneOfTheMostAdvancedFunctionInHumanHistoryToCalculateQuartets(graphs, lock):

    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"

    # ======= QUARTET PRIM ========
    # executorPrim = concurrent.futures.ProcessPoolExecutor(max_workers=17)
    #loaderPrim = Loader("Executing quartet Prim...", "Executing quartet Prim... COMPLETED!", 0.05).start()
    print("Executing quartet Prim...")
    output = "./quartet_prim_" + outputfilePostfix
    datasetNumber = 1
    graphsAccumulator = []
    datasetNumberAccumulator = []
    foo = 0
    
    # Compongo ed eseguo i quartetti
    for graph in graphs:
        if foo == 4:
            foo = 0
            #executorPrim.submit(executeSingleThreadQuartetMeasurement, output, "prim", graphsAccumulator, datasetNumberAccumulator, lock)
            executeSingleQuartetMeasurement(output, "prim", graphsAccumulator, datasetNumberAccumulator, lock)
            graphsAccumulator = []
            datasetNumberAccumulator = []
            
        if foo != 4:
            datasetNumberAccumulator.append(datasetNumber)
            graphsAccumulator.append(graph)
            datasetNumber += 1
            foo += 1

    # Eseguo l'ultimo quartetto
    if len(graphsAccumulator) != 0 :
        executeSingleQuartetMeasurement(output, "prim", graphsAccumulator, datasetNumberAccumulator, lock)
          
    # executorPrim.shutdown(wait=True)
    #loaderPrim.stop()


    # # ======= QUARTET KRUSKAL UNION FIND ========

    print("Executing quartet Kruskal Union Find...")
    output = "./quartet_kruskal_uf_" + outputfilePostfix
    datasetNumber = 1
    graphsAccumulator = []
    datasetNumberAccumulator = []
    foo = 0
    # Compongo ed eseguo i quartetti
    for graph in graphs:
        if foo == 4:
            foo = 0
            executeSingleQuartetMeasurement(output, "kruskal-opt", graphsAccumulator, datasetNumberAccumulator, lock)
            graphsAccumulator = []
            datasetNumberAccumulator = []
            
        if foo != 4:
            datasetNumberAccumulator.append(datasetNumber)
            graphsAccumulator.append(graph)
            datasetNumber += 1
            foo += 1

    # Eseguo l'ultimo quartetto
    if len(graphsAccumulator) != 0 :
        executeSingleQuartetMeasurement(output, "kruskal-opt", graphsAccumulator, datasetNumberAccumulator, lock)


    # # ======= QUARTET KRUSKAL NAIVE ========

    print("Executing quartet Kruskal Naive...")
    output = "./quartet_kruskal_" + outputfilePostfix
    datasetNumber = 1
    graphsAccumulator = []
    datasetNumberAccumulator = []
    foo = 0

    # Compongo ed eseguo i quartetti
    for graph in graphs:
        if foo == 4:
            foo = 0
            executeSingleQuartetMeasurement(output, "kruskal", graphsAccumulator, datasetNumberAccumulator, lock)
            graphsAccumulator = []
            datasetNumberAccumulator = []
            
        if foo != 4:
            datasetNumberAccumulator.append(datasetNumber)
            graphsAccumulator.append(graph)
            datasetNumber += 1
            foo += 1

    # Eseguo l'ultimo quartetto
    if len(graphsAccumulator) != 0 :
        executeSingleQuartetMeasurement(output, "kruskal", graphsAccumulator, datasetNumberAccumulator, lock)



"""
Esecuzione di un singolo quartetto di grafi

    outputfile      =   file di salvataggio dei risultati
    algoname        =   tipo algoritmo da eseguire
    graphs          =   grafi dei dataset da eseguire
    filenumbers     =   array di numeri dei dataset da eseguire
    fileResultLock  =   accesso condiviso dei threads per la scrittura in append dei file (eventuale implementazione)

"""
def executeSingleQuartetMeasurement(outputfile, algoname, graphs, filenumbers, fileResultLock):

    executionTimes = 4

    # Eseguo la prima volta il quartetto e ricavo la media del tempo di esecuzione
    averageTimePerQuartet = 0
    gc.disable()
    for graph in graphs:
        localStartTime = time.perf_counter_ns()
        executeAlgorithm(algoname, graph)
        averageTimePerQuartet += time.perf_counter_ns()-localStartTime
    gc.enable()
    
    averageTimePerQuartet /= 4

    # Se la media di esecuzione è sotto al secondo, 
    # allora lo eseguo n volte tale da avvicinarmi a 1 secondo
    # e ne faccio la media

    if averageTimePerQuartet <= 1000000000: 

        numCalls = 1000000000 // math.floor(averageTimePerQuartet)
        sumTimePerQuartet = 0
        
        for graph in graphs:
            loopStartTime = time.perf_counter_ns()
            gc.disable()
            
            for i in range(0, numCalls):
                executeAlgorithm(algoname, graph)
            
            gc.enable()
            sumTimePerQuartet += (time.perf_counter_ns() - loopStartTime) / numCalls
        
        averageTimePerQuartet = sumTimePerQuartet / 4
        
        rightTime = averageTimePerQuartet
        executionTimes = 4*numCalls
    else:
        rightTime = averageTimePerQuartet
    


    # Una volta concluso, inserisco in append su un file i risultati
    # con la seguente struttura:

    # ============================================================================================
    # n vertex | dataset number | n edges | avg num edges | time | exe times | exe times per graph
    # ============================================================================================

    outFilenumbers = "( "
    for i in filenumbers:
        outFilenumbers += str(i) + " "
    outFilenumbers += ")"

    outEdges = "( "
    for graph in graphs:
        outEdges = outEdges + str(len(graph.E)) + " "
    outEdges += ")"

    outAvgEdges = 0
    for graph in graphs:
        outAvgEdges += len(graph.E)
    outAvgEdges /= 4

    with fileResultLock: 
        file_object = open(outputfile, 'a')
        file_object.write(str(len(graphs[0].V)) + "\t" + outFilenumbers + "\t" + outEdges + "\t" + str(outAvgEdges) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".format(rightTime/1000000000) + "\t" + str(executionTimes) + "\t" + str(executionTimes//4) + "\n")
        file_object.close()


"""
Esecuzione di un singolo algoritmo in un grafo

    algoname        =   tipo algoritmo da eseguire
    graph           =   grafo di input

"""
def executeAlgorithm(algoname, graph):

    # if algoname == "prim":
    #     prim = Prim()
    #     final_graph, _ = prim.prim_mst(graph, 1)
    #     kw = prim.get_weight(final_graph)

    # elif algoname == "kruskal":
    #     mst = MST()
    #     final_graph = mst.kruskal_naive(graph)
    #     kw = mst.get_mst_weight(final_graph.E)

    # elif algoname == "kruskal-opt":
    #     mst = MST()
    #     final_graph = mst.kruskal_union_find(graph)
    #     kw = mst.get_mst_weight(final_graph)
    # else:
    #     pass

    # return kw

    return 0
