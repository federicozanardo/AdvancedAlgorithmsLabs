#!/user/bin/env python3

import sys
from data_structures.graph import Graph
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

    return g
