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



def executeTheSuperFancyPoolThreadsToCalculateMegaComplexGraphs(graphs, lock):

    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"

    # ======= PRIM ========
    # executorPrim = concurrent.futures.ThreadPoolExecutor(max_workers=24)
    #loaderPrim = Loader("Executing Prim...", "Executing Prim... COMPLETED!", 0.05).start()
    print("Executing Prim...")
    datasetNumber = 1

    for graph in graphs:
        output = "./output_prim_" + outputfilePostfix
        #executorPrim.submit(executeSingleThreadCalculus, output, "prim", graph, datasetNumber, lock)
        executeSingleThreadCalculus(output, "prim", graph, datasetNumber, lock)
        datasetNumber += 1    
    #executorPrim.shutdown(wait=True)
    #loaderPrim.stop()

    # ======= KRUSKAL UNION FIND ========
    #executorKruskalUF = concurrent.futures.ThreadPoolExecutor(max_workers=24)
    #loaderKruskalUF = Loader("Executing Kruskal-UF...", "Executing Kruskal-UF... COMPLETED!", 0.05).start()
    print("Executing Kruskal Union Find...")
    datasetNumber = 1

    for graph in graphs:
        output = "./output_kruskal_uf_" + outputfilePostfix
        #executorKruskalUF.submit(executeSingleThreadCalculus, output, "kruskal-opt", graph, datasetNumber, lock)
        executeSingleThreadCalculus(output, "kruskal-opt", graph, datasetNumber, lock)
        datasetNumber += 1    
    #executorKruskalUF.shutdown(wait=True)
    #loaderKruskalUF.stop()

    # ======= KRUSKAL NAIVE ========
    #executorKruskal = concurrent.futures.ThreadPoolExecutor(max_workers=24)
    #loaderKruskal = Loader("Executing Kruskal Naive...", "Executing Kruskal Naive... COMPLETED!", 0.05).start()
    print("Executing Kruskal...")
    datasetNumber = 1

    for graph in graphs:
        output = "./output_kruskal_" + outputfilePostfix
        #executorKruskal.submit(executeSingleThreadCalculus, output, "kruskal", graph, datasetNumber, lock)
        executeSingleThreadCalculus(output, "kruskal", graph, datasetNumber, lock)
        datasetNumber += 1    
    #executorKruskal.shutdown(wait=True)
    #loaderKruskal.stop()


def executeSingleThreadCalculus(outputfile, algoname, graph, filenumber, fileResultLock):

    executionTimes = 1

    # First execution

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

    # Check if execution time is less than 1 seconds
    # in case, take the avg time after 1000 execution

    if localEndTime <= 1000000000: 

        loopStartTime = time.perf_counter_ns()
        gc.disable()
        for i in range(0, 1000):

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
        rightTime = loopEndTime/1000
        executionTimes = 1000
    else:
        rightTime = localEndTime
    
    # dataset number | n vertex | n edges | nano seconds time | seconds time | weight | exe times

    with fileResultLock: 
        file_object = open(outputfile, 'a')
        file_object.write(str(filenumber) + "\t" + str(len(graph.V)) + "\t" + str(len(graph.E)) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".format(rightTime/1000000000) + "\t" + str(kw) + "\t" + str(executionTimes) + "\n")
        file_object.close()
    