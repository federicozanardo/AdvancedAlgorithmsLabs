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
# import matplotlib.pyplot as plt
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
from measurements.single import executeTheSuperFancyFunctionToCalculateMegaComplexTSPs
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
        tsps = loadFromFolder(dirpath)
    elif path.isfile(dirpath):     
        tsp = loadFromFile(dirpath)
        tsps = [tsp]

    if sys.argv[1] == "all":
        executeTheSuperFancyFunctionToCalculateMegaComplexTSPs(tsps, fileResultLock)


    if sys.argv[1] == "2ap" or sys.argv[1] == "all-single":
        print(col.HEADER + "TWO-APPROXIMATION" + col.ENDC)
        for tsp in tsps:
            final = TwoApproximation()
            res = final.algorithm(tsp)
            print('{:<15}{:^15}{:>15}'.format(tsp.name, '=>', res))

    if sys.argv[1] == "nn" or sys.argv[1] == "all-single":
        print(col.HEADER + "NEAREST NEIGHBORS" + col.ENDC)
        for tsp in tsps:
            res = NearestNeighbor().algorithm(tsp)
            print('{:<15}{:^15}{:>15}'.format(tsp.name, '=>', res))

    if sys.argv[1] == "hk" or sys.argv[1] == "all-single":
        print(col.HEADER + "HELD AND KARP" + col.ENDC)
        for tsp in tsps:
            hk = HeldKarp()
            res = hk.hk_init(tsp)
            print('{:<15}{:^15}{:>15}'.format(tsp.name, '=>', res))   

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