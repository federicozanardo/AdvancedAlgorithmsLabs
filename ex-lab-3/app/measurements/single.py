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
from algorithms.stoerwagner import StoerWagner
import sys
from os import walk, path
import time

"""
Esecuzione degli algoritmi in tutti i dataset

    graphs      =   grafi dei dataset da eseguire
    lock        =   accesso condiviso dei threads per la scrittura in append dei file (eventuale implementazione)

"""
def executeTheSuperFancyFunctionToCalculateMegaComplexGraphs(graphs, lock):

    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"

    # ======= Stoer-Wagner ========
    print("Executing StoerWagner...")
    datasetNumber = 1
    output = "./output_stoerwagner_" + outputfilePostfix

    for graph in graphs:
        executeSingleGraphCalculus(output, "sw", graph, datasetNumber, lock)
        datasetNumber += 1    

    # ======= Karger-Stein ========
    print("Executing Karger-Stein...")
    datasetNumber = 1
    output = "./output_kargerstein_" + outputfilePostfix

    for graph in graphs:
        executeSingleGraphCalculus(output, "ks", graph, datasetNumber, lock)
        datasetNumber += 1    


"""
Esecuzione di un singolo grafo 

    outputfile      =   file di salvataggio dei risultati
    algoname        =   tipo algoritmo da eseguire
    graph           =   grafo di partenza in input
    filenumber      =   numero del dataset
    fileResultLock  =   accesso condiviso dei threads per la scrittura in append dei file (eventuale implementazione)

"""
def executeSingleGraphCalculus(outputfile, algoname, graph, filenumber, fileResultLock):

    executionTimes = 1

    localStartTime = time.perf_counter_ns()
    gc.disable()

    if algoname == "sw":
        res = StoerWagner().algorithm(graph)
    
    elif algoname == "ks": #TODO
        pass

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
  
    if algoname == "sw":
        with fileResultLock: 
            file_object = open(outputfile, 'a')
            file_object.write(str(filenumber) + "\t" + str(len(graph.V)) + "\t" +   str(len(graph.E)) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".  format(rightTime/1000000000) + "\t" + str(res) + "\t" + str    (executionTimes) + "\n")
            file_object.close()


    # ======================================================================
    # dataset number | n vertex | n edges | nano seconds time | seconds time | result | error | rep times
    # ======================================================================

    # NOTA BENE:
    # - errore relativo (soluzionetrovata-soluzioneottima)/soluzioneottima
    # - repetition times (per rendere l'algoritmo in h.p.)

    elif algoname == "ks": #TODO
        pass
        with fileResultLock: 
            file_object = open(outputfile, 'a')
            file_object.write(str(filenumber) + "\t" + str(len(graph.V)) + "\t" +   str(len(graph.E)) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".  format(rightTime/1000000000) + "\t" + str(kw) + "\t" + str    (executionTimes) + "\n")
            file_object.close()

