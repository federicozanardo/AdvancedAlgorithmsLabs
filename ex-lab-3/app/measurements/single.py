"""
Module - measurements.single

Modulo di misurazione dei dataset con output del tempo di esecuzione dei singoli

"""

from random import randint
import gc
from data_structures.max_heap import MaxHeap, Node
from data_structures.graph import Graph
from algorithms.utils import populateGraphFromFile as populate
from algorithms.utils import loadFromFolder
from algorithms.utils import loadFromFile
from algorithms.utils import bcolors as col
from algorithms.utils import loadData
from algorithms.karger_stein import KargerStein
from algorithms.stoerwagner import StoerWagner
import sys
from os import walk, path
import time

"""
Esecuzione degli algoritmi in tutti i dataset
    graphs      =   grafi dei dataset da eseguire

"""
def executeTheSuperFancyFunctionToCalculateMegaComplexGraphsFromDirpath(dirpath):
    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"

    # ======= Stoer-Wagner ========
    print("Executing StoerWagner...")
    datasetNumber = 1
    output = "./output_stoerwagner_" + outputfilePostfix

    graphs = loadData(dirpath, False)

    for graph in graphs:
        executeSingleGraphCalculus(output, "sw", graph, datasetNumber)
        datasetNumber += 1    

    # ======= Karger-Stein ========
    print("Executing Karger-Stein...")
    datasetNumber = 1
    output = "./output_kargerstein_" + outputfilePostfix

    graphs = loadData(dirpath, True)

    for graph in graphs:
        executeSingleGraphCalculus(output, "ks", graph, datasetNumber)
        datasetNumber += 1    


"""
Esecuzione di un singolo grafo 

    outputfile      =   file di salvataggio dei risultati
    algoname        =   tipo algoritmo da eseguire
    graph           =   grafo di partenza in input
    filenumber      =   numero del dataset

"""
def executeSingleGraphCalculus(outputfile, algoname, graph, filenumber):

    executionTimes = 1

    localStartTime = time.perf_counter_ns()
    gc.disable()

    if algoname == "sw":

        res = StoerWagner().algorithm(graph)

        gc.enable()
        localEndTime = time.perf_counter_ns()-localStartTime

        # Se il tempo di esecuzione è minore di 1 secondo, lo eseguo n volte
        # tale da avvicinarmi a 1 secondo
        # e ne faccio la media

        if localEndTime <= 1000000000: 
            numCalls = 1000000000//localEndTime
            loopStartTime = time.perf_counter_ns()
            gc.disable()

            for i in range(0, numCalls):

                if algoname == "sw":
                    res = StoerWagner().algorithm(graph)

                elif algoname == "ks": #TODO
                    pass
                
            gc.enable()
            loopEndTime = time.perf_counter_ns() - loopStartTime
            rightTime = loopEndTime/numCalls
            executionTimes = numCalls
        else:
            rightTime = localEndTime

        # Una volta concluso, inserisco in append su un file i risultati
        # con la seguente struttura:
        
        # ======================================================================
        # dataset number | n vertex | n edges | nano seconds time | seconds time | result | exe times
        # ======================================================================
    
        file_object = open(outputfile, 'a')
        file_object.write(str(filenumber) + "\t" + str(len(graph.V)) + "\t" +   str(len(graph.E)) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".  format(rightTime/1000000000) + "\t" + str(res) + "\t" + str    (executionTimes) + "\n")
        file_object.close()
    
    elif algoname == "ks":
        res = KargerStein(graph)
        min_cut, k, k_min, discovery_time, total_time, n_repetitions, is_threshold_activated = res.measurements()

        # ======================================================================
        # dataset number | n vertex | n edges | nano seconds time | seconds time | result | discovery time | error | rep times | k | k_min | is_treshold_activated
        # ======================================================================

        file_object = open(outputfile, 'a')
        file_object.write(str(filenumber) + "\t" + str(graph.n_vertices) + "\t" +   str(graph.n_edges) + "\t" + "{:.7f}".format(total_time) + "\t" + "{:.7f}".  format(total_time/1000000000) + "\t" + str(min_cut) + "\t" + str(discovery_time) + "\t" + str(n_repetitions) + "\t" + str(k) + "\t" + str(k_min) + "\t" + str(is_threshold_activated) + "\n")
        file_object.close()