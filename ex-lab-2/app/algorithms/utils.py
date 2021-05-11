#!/user/bin/env python3

import sys
from data_structures.tsp import TSP
from os import walk
sys.path.append('../')

from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep


# TODO: change this into a working one with the new dataset

def populateTSPFromFile(filepath):
    file = open(filepath, 'r')
    formatted_file = file.read().split('\n')
    tsp = TSP()

    absolutelyUsefulVariableIndexBecausePregMatchBad = 0
    for i in range(10):
        absolutelyUsefulVariableIndexBecausePregMatchBad += 1 # (i+1) past the NODE_COORD_SECTION

        if formatted_file[i].split(':')[0] == "NAME":
            tsp.name = formatted_file[i].split(':')[1]
            
        if formatted_file[i].split(':')[0] == "TYPE":
            tsp.etype = formatted_file[i].split(':')[1]

        if formatted_file[i].split(':')[0] == "DIMENSION":
            tsp.dimension = int(formatted_file[i].split(':')[1])
    
        if formatted_file[i] == "NODE_COORD_SECTION":
            break

    if absolutelyUsefulVariableIndexBecausePregMatchBad == 10:
        print("where banana")
        exit()

    for i in range(tsp.dimension):
        row = formatted_file[i+absolutelyUsefulVariableIndexBecausePregMatchBad].split(' ')
        tsp.add_node(float(row[0]), float(row[1]), float(row[2]))
    file.close()

    tsp.calculateAdjMatrix()

    return tsp


def loadFromFolder(dirpath):
    print("Loading dataset files...", end="")
    sys.stdout.flush()

    tsps = []
    filenames = []

    for root, dirs, files in walk(dirpath):  # load filenames
        for filename in files:
            filenames.append(filename)
    filenames.sort() 

    for file in filenames:  # load files
        p = populateTSPFromFile(dirpath + '/' + file)
        tsps.append(p)

    print("DONE")
    sys.stdout.flush()

    return tsps


def loadFromFile(filepath):
    print("Loading dataset files...", end="")
    sys.stdout.flush()

    tsp = populateTSPFromFile(filepath)

    print("DONE")
    sys.stdout.flush()

    return tsp


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
