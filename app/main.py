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
from multithreading.threads import executeSingleThreadCalculus,executeTheSuperFancyPoolThreadsToCalculateMegaComplexGraphs
import sys
from os import walk, path
import time
import concurrent.futures
import multiprocessing

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
    
    if sys.argv[1] == "prim" or sys.argv[1] == "all-single":
        for graph in graphs:
            prim = Prim()
            mst = MST()
            key = prim.prim_mst(graph, 1)
            print(prim.get_weight(key))

    if sys.argv[1] == "kruskal" or sys.argv[1] == "all-single":
        for graph in graphs:
            mst = MST()
            final_graph = mst.kruskal_naive(graph)
            print(mst.get_mst_weight(final_graph.E))

    if sys.argv[1] == "kruskal-opt" or sys.argv[1] == "all-single":
        for graph in graphs:
            mst = MST()
            final_graph = mst.kruskal_union_find(graph)
            print(mst.get_mst_weight(final_graph))

    print(">" + col.OKGREEN + " Total execution time: " + col.HEADER + str(round(time.time()-start, 8)) + "s" + col.ENDC)





if __name__ == "__main__":
    main()
