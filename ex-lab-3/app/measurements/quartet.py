"""
Module - measurements.quartet

Modulo di misurazione dei dataset raggruppati in un quartetto 
di grafi composti dallo stesso numero di vertici

"""

import gc
import math
from algorithms.stoerwagner import StoerWagner
from algorithms.karger_stein import KargerStein
from algorithms.utils import loadData
import time


"""
Composizione ed esecuzione dei quartetti a partire da più dataset
    graphs          =   grafi dei dataset da eseguire

"""
def executeOneOfTheMostAdvancedFunctionInHumanHistoryToCalculateQuartetsFromDirpath(dirpath):
    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"

    # ======= QUARTET STOER-WAGNER ========
    print("Executing quartet Stoer-Wagner...")
    output = "./quartet_stoerwagner_" + outputfilePostfix
    datasetNumber = 1
    graphsAccumulator = []
    datasetNumberAccumulator = []
    foo = 0
    
    graphs = loadData(dirpath, False)
    
    # Compongo ed eseguo i quartetti
    for graph in graphs:
        if foo == 4:
            foo = 0
            executeSingleQuartetMeasurement(output, "sw", graphsAccumulator, datasetNumberAccumulator)
            graphsAccumulator = []
            datasetNumberAccumulator = []
            
        if foo != 4:
            datasetNumberAccumulator.append(datasetNumber)
            graphsAccumulator.append(graph)
            datasetNumber += 1
            foo += 1

    # Eseguo l'ultimo quartetto
    if len(graphsAccumulator) != 0 :
        executeSingleQuartetMeasurement(output, "sw", graphsAccumulator, datasetNumberAccumulator)

    # ======= QUARTET KARGER-STEIN ========
    print("Executing quartet Karger-Stein...")
    output = "./quartet_kargerstein_" + outputfilePostfix
    datasetNumber = 1
    graphsAccumulator = []
    datasetNumberAccumulator = []
    foo = 0
    
    graphs = loadData(dirpath, True)
    
    # Compongo ed eseguo i quartetti
    for graph in graphs:
        if foo == 4:
            foo = 0
            executeSingleQuartetMeasurement(output, "ks", graphsAccumulator, datasetNumberAccumulator)
            graphsAccumulator = []
            datasetNumberAccumulator = []
            
        if foo != 4:
            datasetNumberAccumulator.append(datasetNumber)
            graphsAccumulator.append(graph)
            datasetNumber += 1
            foo += 1

    # Eseguo l'ultimo quartetto
    if len(graphsAccumulator) != 0 :
        executeSingleQuartetMeasurement(output, "ks", graphsAccumulator, datasetNumberAccumulator)


"""
Esecuzione di un singolo quartetto di grafi

    outputfile      =   file di salvataggio dei risultati
    algoname        =   tipo algoritmo da eseguire
    graphs          =   grafi dei dataset da eseguire
    filenumbers     =   array di numeri dei dataset da eseguire

"""
def executeSingleQuartetMeasurement(outputfile, algoname, graphs, filenumbers):

    executionTimes = 4

    # Eseguo la prima volta il quartetto e ricavo la media del tempo di esecuzione
    averageTimePerQuartet = 0
    gc.disable()
    for graph in graphs:
        localStartTime = time.perf_counter_ns()
        executeAlgorithm(algoname, graph)
        averageTimePerQuartet += time.perf_counter_ns()-localStartTime
    gc.enable()
    
    averageTimePerQuartet /= 4

    # Se la media di esecuzione è sotto al secondo, 
    # allora lo eseguo n volte tale da avvicinarmi a 1 secondo
    # e ne faccio la media

    if averageTimePerQuartet <= 1000000000: 

        numCalls = 1000000000 // math.floor(averageTimePerQuartet)
        sumTimePerQuartet = 0
        
        for graph in graphs:
            loopStartTime = time.perf_counter_ns()
            gc.disable()
            
            for i in range(0, numCalls):
                executeAlgorithm(algoname, graph)
            
            gc.enable()
            sumTimePerQuartet += (time.perf_counter_ns() - loopStartTime) / numCalls
        
        averageTimePerQuartet = sumTimePerQuartet / 4
        
        rightTime = averageTimePerQuartet
        executionTimes = 4*numCalls
    else:
        rightTime = averageTimePerQuartet
    


    # Una volta concluso, inserisco in append su un file i risultati
    # con la seguente struttura:

    # ============================================================================================
    # n vertex | dataset number | n edges | avg num edges | time | exe times | exe times per graph
    # ============================================================================================

    outFilenumbers = "( "
    for i in filenumbers:
        outFilenumbers += str(i) + " "
    outFilenumbers += ")"

    if algoname == "sw":
        outEdges = "( "
        for graph in graphs:
            outEdges = outEdges + str(len(graph.E)) + " "
        outEdges += ")"

        outAvgEdges = 0
        for graph in graphs:
            outAvgEdges += len(graph.E)
        outAvgEdges /= 4

        file_object = open(outputfile, 'a')
        file_object.write(str(len(graphs[0].V)) + "\t" + outFilenumbers + "\t" + outEdges + "\t" + str(outAvgEdges) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".format(rightTime/1000000000) + "\t" + str(executionTimes) + "\t" + str(executionTimes//4) + "\n")
        file_object.close()

    elif algoname == "ks":
        outEdges = "( "
        for graph in graphs:
            outEdges = outEdges + str(graph.n_edges) + " "
        outEdges += ")"

        outAvgEdges = 0
        for graph in graphs:
            outAvgEdges += graph.n_edges
        outAvgEdges /= 4

        file_object = open(outputfile, 'a')
        file_object.write(str(graphs[0].n_vertices) + "\t" + outFilenumbers + "\t" + outEdges + "\t" + str(outAvgEdges) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".format(rightTime/1000000000) + "\t" + str(executionTimes) + "\t" + str(executionTimes//4) + "\n")
        file_object.close()



"""
Esecuzione di un singolo algoritmo in un grafo

    algoname        =   tipo algoritmo da eseguire
    graph           =   grafo di input

"""
def executeAlgorithm(algoname, graph):

    if algoname == "sw":
        res = StoerWagner().algorithm(graph)

    elif algoname == "ks": #TODO
        res = KargerStein(graph).algorithm()

    else:
        pass

    return res
