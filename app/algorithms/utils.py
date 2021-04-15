#!/user/bin/env python3

import sys
from data_structures.graph import Graph
from os import walk
sys.path.append('../')


def populateGraphFromFile(filepath):
    file = open(filepath, 'r')
    g = Graph()
    formatted_file = file.read().split('\n')
    n_vertices, n_edges = int(formatted_file[0].split(
        ' ')[0]), int(formatted_file[0].split(' ')[1])

    for i in range(n_edges):
        row = formatted_file[i+1].split(' ')
        g.add_vertex(row[0])
        g.add_vertex(row[1])
        g.add_edge(row[0], row[1], row[2])

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
    filenames.sort()  # lmao

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
