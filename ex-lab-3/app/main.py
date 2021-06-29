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
from algorithms.utils import bcolors as col
from algorithms.utils import loadData
from measurements.single import executeTheSuperFancyFunctionToCalculateMegaComplexGraphsFromDirpath
from measurements.quartet import executeOneOfTheMostAdvancedFunctionInHumanHistoryToCalculateQuartetsFromDirpath
from algorithms.stoerwagner import StoerWagner
from algorithms.karger_stein import KargerStein
import sys
from os import path
import time

def main(args):

    start = time.time()  # Timer di partenza del programma
    
    # Recupero il path in input e salvo i grafi individuati

    dirpath = sys.argv[2]

    assert path.isfile(dirpath) or path.isdir(
        dirpath), "File or folder not found"


    if sys.argv[1] == "all":
        executeTheSuperFancyFunctionToCalculateMegaComplexGraphsFromDirpath(dirpath)


    if sys.argv[1] == "all-quartet":
        executeOneOfTheMostAdvancedFunctionInHumanHistoryToCalculateQuartetsFromDirpath(dirpath)

    if sys.argv[1] == "sw" or sys.argv[1] == "all-single":

        graphs = loadData(dirpath, False)

        print(col.HEADER + "STOER-WAGNER" + col.ENDC)
        for graph in graphs:
            res = StoerWagner().algorithm(graph)
            print(col.OKBLUE+ graph.datasetName, ' \t' + col.ENDC, 'Min-cut: ' + col.ENDC, res)

    if sys.argv[1] == "ks" or sys.argv[1] == "all-single":

        graphs = loadData(dirpath, True)

        print(col.HEADER + "KARGER-STEIN" + col.ENDC)
        i = 1
        for graph in graphs:
            karger = KargerStein(graph)
            threshold_in_seconds = 7
            min_cut, k, k_min, discovery_time, total_time, n_repetitions, is_threshold_activated = karger.measurements()
            print('Graph {}'.format(i))
            print('\tMin-cut: {}'.format(min_cut))
            print('\tNumero di ripetizioni totali (k): {}'.format(k))
            print('\tIl min-cut è stato trovato all\'iterazione: {}'.format(k_min))
            print('\tDiscovery time: {}ns ({}s)'.format(discovery_time, discovery_time / 1000000000))
            print('\tTempo totale di esecuzione: {}ns ({}s)'.format(total_time, total_time / 1000000000))
            print('\tNumero di ripetizioni: {}'.format(n_repetitions))
            print('\tThreshold di {}s attivata: {}\n'.format(threshold_in_seconds, is_threshold_activated))
            i+=1

  
    print(">" + col.OKGREEN + " Total execution time: " + col.HEADER + str(round(time.time()-start, 8)) + "s" + col.ENDC)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional arguments
    parser.add_argument("<algo type>", help="Tipo di algoritmo <all/all-single/sw/ks>")
    parser.add_argument("<dataset path>", help="Posizione del singolo file o della cartella con i dataset")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s MinCutCalculator (version {version}) by {authors}".format(version=__version__,authors=__author__))

    args = parser.parse_args()
    main(args)
