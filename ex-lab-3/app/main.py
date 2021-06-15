#!/usr/bin/env python3

"""
=================================================
    Advanced Algorithm - Lab 3 (2020-21)
  MD in Computer Science - University of Padua
=================================================
"""

__author__ = "E. Buratto, M. Sciacco, F. Zanardo"
__version__ = "1.0.0"
__license__ = "Unlicense"

import argparse
from random import randint
import gc
from time import perf_counter_ns
import matplotlib.pyplot as plt
from data_structures.max_heap import MaxHeap, Node
from data_structures.graph import Graph
from algorithms.utils import populateGraphFromFile as populate
from algorithms.utils import loadFromFolder
from algorithms.utils import loadFromFile
from algorithms.utils import bcolors as col
from algorithms.mst import MST
# from measurements.single import executeSingleGraphCalculus,executeTheSuperFancyFunctionToCalculateMegaComplexGraphs
# from measurements.quartet import executeOneOfTheMostAdvancedFunctionInHumanHistoryToCalculateQuartets
from algorithms.stoerwagner import StoerWagner
import sys
from os import walk, path
import time
import concurrent.futures
import multiprocessing

def main(args):

    start = time.time()  # Timer di partenza del programma
    fileResultLock = multiprocessing.Lock() # Accesso condiviso per una eventuale implementazione con multithreading
    
    # Recupero il path in input e salvo i grafi individuati

    dirpath = sys.argv[2]

    assert path.isfile(dirpath) or path.isdir(
        dirpath), "File or folder not found"

    if path.isdir(dirpath):
        graphs = loadFromFolder(dirpath)
    elif path.isfile(dirpath):     
        graph = loadFromFile(dirpath)
        graphs = [graph]

    if sys.argv[1] == "sw" or sys.argv[1] == "all-single":
        print(col.HEADER + "STOER-WAGNER" + col.ENDC)
        for graph in graphs:
            final = StoerWagner()
            res=final.algorithm(graph)
            print(res)


    # Eseguo una delle opzioni seguenti

    # if sys.argv[1] == "all":
    #     executeTheSuperFancyFunctionToCalculateMegaComplexGraphs(graphs, fileResultLock)

    # if sys.argv[1] == "all-quartet":
    #     executeOneOfTheMostAdvancedFunctionInHumanHistoryToCalculateQuartets(graphs, fileResultLock)
    
    # if sys.argv[1] == "prim" or sys.argv[1] == "all-single":
    #     for graph in graphs:
    #         prim = Prim()
    #         mst = MST()
    #         key,_ = prim.prim_mst(graph, 1)
    #         print("Prim \t\t => \t", prim.get_weight(key))

    # if sys.argv[1] == "kruskal-opt" or sys.argv[1] == "all-single":
    #     for graph in graphs:
    #         mst = MST()
    #         final_graph = mst.kruskal_union_find(graph)
    #         print("Kruskal UF \t => \t", mst.get_mst_weight(final_graph))

    # if sys.argv[1] == "kruskal" or sys.argv[1] == "all-single":
    #     for graph in graphs:
    #         mst = MST()
    #         final_graph = mst.kruskal_naive(graph)
    #         print("Kruskal Naive \t => \t", mst.get_mst_weight(final_graph.E))

    print(">" + col.OKGREEN + " Total execution time: " + col.HEADER + str(round(time.time()-start, 8)) + "s" + col.ENDC)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional arguments
    parser.add_argument("<algo type>", help="Tipo di algoritmo <all/all-quartet/all-single/prim/kruskal/kruskal-opt>")
    parser.add_argument("<dataset path>", help="Posizione del singolo file o della cartella con i dataset")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s MSTCalculator (version {version}) by {authors}".format(version=__version__,authors=__author__))

    args = parser.parse_args()
    main(args)