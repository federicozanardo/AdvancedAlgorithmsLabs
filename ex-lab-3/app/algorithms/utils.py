#!/user/bin/env python3

import sys
from data_structures.graph import Graph
from os import walk
sys.path.append('../')
import os

from itertools import cycle
from shutil import get_terminal_size
from time import sleep

def populateGraphFromFile(filepath):
    file = open(filepath, 'r')
    g = Graph()
    formatted_file = file.read().split('\n')
    n_vertices, n_edges = int(formatted_file[0].split(
        ' ')[0]), int(formatted_file[0].split(' ')[1])
    g.totalVertex, g.totalEdges = n_vertices, n_edges
    g.datasetName = os.path.basename(file.name)

    for i in range(n_edges):
        row = formatted_file[i+1].split(' ')
        g.add_vertex(int(row[0]))
        g.add_vertex(int(row[1]))
        g.add_edge(int(row[0]), int(row[1]), int(row[2]))

    file.close()

    return g


def loadFromFolder(dirpath):
    print("Loading dataset files...", end="")
    sys.stdout.flush()

    graphs = []
    filenames = []

    for root, dirs, files in walk(dirpath):  # load filenames
        for filename in files:
            filenames.append(filename)
    filenames.sort() 

    for file in filenames:  # load files
        g = populateGraphFromFile(dirpath + '/' + file)
        graphs.append(g)

    print("DONE")
    sys.stdout.flush()

    return graphs


def loadFromFile(filepath):
    print("Loading dataset files...", end="")
    sys.stdout.flush()

    graph = populateGraphFromFile(filepath)

    print("DONE")
    sys.stdout.flush()

    return graph


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

