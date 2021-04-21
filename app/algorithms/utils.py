#!/user/bin/env python3

import sys
from data_structures.graph import Graph
from os import walk
sys.path.append('../')

from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

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


class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()