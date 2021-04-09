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
from algorithms.utils import loadFromFolder as loadFromFolder
import sys
from os import walk, path
import time

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

    # read datasets
    dirpath = sys.argv[1]
    assert path.isfile(dirpath) or path.isdir(
        dirpath), "File or folder not found"

    graphs = loadFromFolder(dirpath)

    for g in graphs:
        print(len(g.E))

    tempo = time.time() - start
    print(tempo)


if __name__ == "__main__":
    main()
