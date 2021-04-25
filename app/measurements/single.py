"""
Module - measurements.single

Modulo di misurazione dei dataset con output del tempo di esecuzione dei singoli

"""

import argparse
from random import randint
import gc
import matplotlib.pyplot as plt
from data_structures.heap import Heap, Node
from data_structures.graph import Graph
from algorithms.utils import populateGraphFromFile as populate
from algorithms.utils import loadFromFolder
from algorithms.utils import loadFromFile
from algorithms.utils import bcolors as col
from algorithms.utils import Loader
from algorithms.mst import MST
from algorithms.prim import Prim
import sys
from os import walk, path
import time
import concurrent.futures
import multiprocessing


"""
Esecuzione degli algoritmi in tutti i dataset

    graphs      =   grafi dei dataset da eseguire
    lock        =   accesso condiviso dei threads per la scrittura in append dei file (eventuale implementazione)

"""
def executeTheSuperFancyFunctionToCalculateMegaComplexGraphs(graphs, lock):

    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"

    # ======= PRIM ========
    # executorPrim = concurrent.futures.ThreadPoolExecutor(max_workers=24)
    # loaderPrim = Loader("Executing Prim...", "Executing Prim... COMPLETED!", 0.05).start()
    print("Executing Prim...")
    datasetNumber = 1
    output = "./output_prim_" + outputfilePostfix

    for graph in graphs:
        # executorPrim.submit(executeSingleThreadCalculus, output, "prim", graph, datasetNumber, lock)
        executeSingleGraphCalculus(output, "prim", graph, datasetNumber, lock)
        datasetNumber += 1    
    # executorPrim.shutdown(wait=True)
    # loaderPrim.stop()

    # ======= KRUSKAL UNION FIND ========
    print("Executing Kruskal Union Find...")
    datasetNumber = 1
    output = "./output_kruskal_uf_" + outputfilePostfix

    for graph in graphs:
        executeSingleGraphCalculus(output, "kruskal-opt", graph, datasetNumber, lock)
        datasetNumber += 1    

    # ======= KRUSKAL NAIVE ========
    print("Executing Kruskal...")
    datasetNumber = 1
    output = "./output_kruskal_" + outputfilePostfix

    for graph in graphs:
        executeSingleGraphCalculus(output, "kruskal", graph, datasetNumber, lock)
        datasetNumber += 1 




"""
Esecuzione di un singolo grafo 

    outputfile      =   file di salvataggio dei risultati
    algoname        =   tipo algoritmo da eseguire
    graph           =   grafo di partenza in input
    filenumber      =   numero del dataset
    fileResultLock  =   accesso condiviso dei threads per la scrittura in append dei file (eventuale implementazione)

"""
def executeSingleGraphCalculus(outputfile, algoname, graph, filenumber, fileResultLock):

    executionTimes = 1

    # Eseguo la prima volta il quartetto e ricavo il tempo di esecuzione

    localStartTime = time.perf_counter_ns()
    gc.disable()

    if algoname == "prim":
        prim = Prim()
        final_graph,_ = prim.prim_mst(graph, 1)
        kw = prim.get_weight(final_graph)

    elif algoname == "kruskal":
        mst = MST()
        final_graph = mst.kruskal_naive(graph)
        kw = mst.get_mst_weight(final_graph.E)

    elif algoname == "kruskal-opt":
        mst = MST()
        final_graph = mst.kruskal_union_find(graph)
        kw = mst.get_mst_weight(final_graph)
    else:
        pass

    gc.enable()
    localEndTime = time.perf_counter_ns()-localStartTime


    # Se il tempo di esecuzione è minore di 1 secondo, lo eseguo n volte \
    # tale da avvicinarmi a 1 secondo
    # e ne faccio la media

    if localEndTime <= 1000000000: 

        numCalls = 1000000000//localEndTime

        loopStartTime = time.perf_counter_ns()
        gc.disable()
        for i in range(0, numCalls):

            if algoname == "prim":
                prim = Prim()
                final_graph,_ = prim.prim_mst(graph, 1)
                kw = prim.get_weight(final_graph)

            elif algoname == "kruskal":
                mst = MST()
                final_graph = mst.kruskal_naive(graph)
                kw = mst.get_mst_weight(final_graph.E)

            elif algoname == "kruskal-opt":
                mst = MST()
                final_graph = mst.kruskal_union_find(graph)
                kw = mst.get_mst_weight(final_graph)
            
        gc.enable()
        loopEndTime = time.perf_counter_ns() - loopStartTime
        rightTime = loopEndTime/numCalls
        executionTimes = numCalls
    else:
        rightTime = localEndTime
    

    # Una volta concluso, inserisco in append su un file i risultati
    # con la seguente struttura:
    
    # ======================================================================
    # dataset number | n vertex | n edges | nano seconds time | seconds time | weight | exe times
    # ======================================================================
  
    with fileResultLock: 
        file_object = open(outputfile, 'a')
        file_object.write(str(filenumber) + "\t" + str(len(graph.V)) + "\t" + str(len(graph.E)) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".format(rightTime/1000000000) + "\t" + str(kw) + "\t" + str(executionTimes) + "\n")
        file_object.close()
    