#!/usr/bin/env python3

"""
=================================================
    Advanced Algorithm - Lab 2 (2020-21)
  MD in Computer Science - University of Padua
=================================================
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
from data_structures.tsp import TSP
from algorithms.utils import populateTSPFromFile as populate
from algorithms.utils import loadFromFile
from algorithms.utils import loadFromFolder
from algorithms.utils import bcolors as col
from algorithms.prim import Prim
from algorithms.hk import HeldKarp
from algorithms.two_approximation import TwoApproximation
from algorithms.nearestneighbor import NearestNeighbor
import sys
from os import walk, path
import time
import concurrent.futures
import multiprocessing

def main(args):

    start = time.time()  # Timer di partenza del programma
    
    # Recupero il path in input e salvo i grafi individuati

    dirpath = sys.argv[2]

    assert path.isfile(dirpath) or path.isdir(
        dirpath), "File or folder not found"

    if path.isdir(dirpath):
        tsps = loadFromFolder(dirpath)
    elif path.isfile(dirpath):     
        tsp = loadFromFile(dirpath)
        tsps = [tsp]

    # Eseguo una delle opzioni seguenti

    # if sys.argv[1] == "all":
    #     executeTheSuperFancyFunctionToCalculateMegaComplexGraphs(graphs, fileResultLock)

    # if sys.argv[1] == "all-quartet":
    #     executeOneOfTheMostAdvancedFunctionInHumanHistoryToCalculateQuartets(graphs, fileResultLock)



    if sys.argv[1] == "2ap" or sys.argv[1] == "all-single":
        for tsp in tsps:
            final = TwoApproximation()
            res = final.algorithm(tsp)
            print("2 approximation \t => \t", res)

    if sys.argv[1] == "hk" or sys.argv[1] == "all-single":
        for tsp in tsps:
            hk = HeldKarp()
            res = hk.hk_init(tsp)
            print("Held and Karp \t => \t", res)    


    if sys.argv[1] == "nn" or sys.argv[1] == "all-single":
        for tsp in tsps:
            res = NearestNeighbor().algorithm(tsp)
            print("Nearest neighbor \t => \t", res)

    print(">" + col.OKGREEN + " Total execution time: " + col.HEADER + str(round(time.time()-start, 8)) + "s" + col.ENDC)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional arguments
    parser.add_argument("<algo type>", help="Tipo di algoritmo <all/all-single>")
    parser.add_argument("<dataset path>", help="Posizione del singolo file o della cartella con i dataset")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s TSPCalculator (version {version}) by {authors}".format(version=__version__,authors=__author__))

    args = parser.parse_args()
    main(args)