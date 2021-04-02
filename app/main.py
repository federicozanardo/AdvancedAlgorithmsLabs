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




# TODO: adapt the code to the one we need

def measure_run_time(list_size, num_calls, num_instances):
  sum_times = 0.0
  for i in range(num_instances):
    alist = [randint(0,10000) for i in range(list_size)]
    target = randint(0,10000)
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



def main(args):
    # """ Main entry point of the app """
    # print("hello world")
    # print(args)
    h = Heap()
    h.insert(Node(1, 100))
    h.insert(Node(2, 200))
    h.insert(Node(3, 1))
    h.insert(Node(1, 50))
    h.insert(Node(2, 2000))
    h.insert(Node(3, 2))

    h.print()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)