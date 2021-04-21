#!/usr/bin/env python3

"""
Module Docstring
"""

__author__ = "E. Buratto, M. Sciacco, F. Zanardo"
__version__ = "0.0.1"
__license__ = "Unlicense"

import argparse
from random import randint
import gc
from time import perf_counter_ns
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

# TODO: adapt the code to the one we need

def measure_run_time(list_size, num_calls, num_instances):
    sum_times = 0.0
    for i in range(num_instances):
        alist = [randint(0, 10000) for i in range(list_size)]
        target = randint(0, 10000)
        gc.disable()
        start_time = perf_counter_ns()
        for i in range(num_calls):
            print(i)
            # linear_search(alist, target)
        end_time = perf_counter_ns()
        gc.enable()
        sum_times += (end_time - start_time)/num_calls
    avg_time = int(round(sum_times/num_instances))
    # return average time in nanoseconds
    return avg_time

# avg_time = measure_run_time(10, 100000, 4)
# print("Average time (ns):", avg_time)



def main():

    start = time.time()  # start timer
    fileResultLock = multiprocessing.Lock()
    mode = None
    
    # read datasets
    dirpath = sys.argv[2]

    assert path.isfile(dirpath) or path.isdir(
        dirpath), "File or folder not found"

    if path.isdir(dirpath):
        graphs = loadFromFolder(dirpath)
        mode = 1
    elif path.isfile(dirpath):     
        graph = loadFromFile(dirpath)
        graphs = [graph]
        mode = 2

    # select what to do

    if sys.argv[1] == "all":
        executeTheSuperFancyPoolThreadsToCalculateMegaComplexGraphs(graphs, fileResultLock)
    elif sys.argv[1] == "prim":
        for graph in graphs:
            prim = Prim()
            mst = MST()
            key = prim.prim_mst(graph, 1)
            print(prim.get_weight(key))

    elif sys.argv[1] == "kruskal":
        for graph in graphs:
            mst = MST()
            final_graph = mst.kruskal_naive(graph)
            print(mst.get_mst_weight(final_graph.E))

    elif sys.argv[1] == "kruskal-opt":
        for graph in graphs:
            mst = MST()
            final_graph = mst.kruskal_union_find(graph)
            print(mst.get_mst_weight(final_graph))

    print(">" + col.OKGREEN + " Total execution time: " + col.HEADER + str(round(time.time()-start, 8)) + "s" + col.ENDC)


def executeTheSuperFancyPoolThreadsToCalculateMegaComplexGraphs(graphs, lock):

    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"
    datasetNumber = 1

    # testing.. executeSingleThreadCalculus("./output_prim_" + outputfilePostfix, "prim", graphs[0], 1, lock)

    # ======= PRIM ========
    executorPrim = concurrent.futures.ThreadPoolExecutor(max_workers=24)
    loaderPrim = Loader("Executing Prim...", "Executing Prim... COMPLETED!", 0.05).start()

    for graph in graphs:
        output = "./output_prim_" + outputfilePostfix
        executorPrim.submit(executeSingleThreadCalculus, output, "prim", graph, datasetNumber, lock)
        datasetNumber += 1    
    executorPrim.shutdown(wait=True)
    loaderPrim.stop()

    # ======= KRUSKAL NAIVE ========
    executorKruskal = concurrent.futures.ThreadPoolExecutor(max_workers=24)
    loaderKruskal = Loader("Executing Kruskal Naive...", "Executing Kruskal Naive... COMPLETED!", 0.05).start()

    for graph in graphs:
        output = "./output_kruskal_" + outputfilePostfix
        executorKruskal.submit(executeSingleThreadCalculus, output, "kruskal", graph, datasetNumber, lock)
        datasetNumber += 1    
    executorKruskal.shutdown(wait=True)
    loaderKruskal.stop()

    # ======= KRUSKAL UNION FIND ========
    executorKruskalUF = concurrent.futures.ThreadPoolExecutor(max_workers=24)
    loaderKruskalUF = Loader("Executing Kruskal-UF...", "Executing Kruskal-UF... COMPLETED!", 0.05).start()

    for graph in graphs:
        output = "./output_kruskal_uf_" + outputfilePostfix
        executorKruskalUF.submit(executeSingleThreadCalculus, output, "kruskal-opt", graph, datasetNumber, lock)
        datasetNumber += 1    
    executorKruskalUF.shutdown(wait=True)
    loaderKruskalUF.stop()



def executeSingleThreadCalculus(outputfile, algoname, graph, filenumber, fileResultLock):

    localStartTime = time.time()

    if algoname == "prim":
        prim = Prim()
        prim.prim_mst(graph, 1)

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

    endtime = time.time()-localStartTime

    with fileResultLock: 
        file_object = open(outputfile, 'a')
        file_object.write(str(filenumber) + "\t" + str(len(graph.V)) + "\t" + "{:.7f}".format(endtime) + "\t" + str(kw) + "\n")
        file_object.close()
    


if __name__ == "__main__":
    main()
