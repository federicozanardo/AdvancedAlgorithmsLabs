

#!/usr/bin/env python3

"""
Module - Measurements
"""

import argparse
from random import randint
import gc
from time import perf_counter_ns
# import matplotlib.pyplot as plt
from data_structures.heap import Heap, Node
from data_structures.graph import Graph
from algorithms.utils import populateGraphFromFile as populate
from algorithms.utils import loadFromFolder
from algorithms.utils import loadFromFile
from algorithms.utils import bcolors as col
from algorithms.utils import Loader
from algorithms.mst import MST
from algorithms.prim import Prim
import sys
from os import walk, path
import time
import concurrent.futures
import multiprocessing


DEFAULT_NUM_CALLS = 10


# def main():
#     mode = None

#     # read datasets
#     dirpath = sys.argv[2]

#     assert path.isfile(dirpath) or path.isdir(
#         dirpath), "File or folder not found"

#     if path.isdir(dirpath):
#         graphs = loadFromFolder(dirpath)
#         mode = 1
#     elif path.isfile(dirpath):
#         graph = loadFromFile(dirpath)
#         graphs = [graph]
#         mode = 2

#     outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"
#     output = "./output_kruskal_opt_" + outputfilePostfix
#     file_object = open(output, 'a')
#     file_object.write("n_vertex\ttime\tconstant\tratio\n")
#     file_object.close()

#     times = measure(graphs)
#     #print(times)
#     #print('Len times: {}'.format(str(len(times))))

#     num_nodes = [10, 20, 40, 80, 100, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 20000, 40000, 80000, 100000]
#     #print('Len num_nodes: {}'.format(str(len(num_nodes))))

#     ratios = [None] + [round(times[i + 1] / times[i], 6) for i in range(len(num_nodes) - 1)]
#     c_estimates = [round(times[i] / num_nodes[i], 6) for i in range(len(num_nodes))]

#     for i in range(len(num_nodes)):
#         file_object = open(output, 'a')
#         file_object.write(str(num_nodes[i]) + "\t" + str(round(times[i], 5)) + "\t" + str(c_estimates[i]) + "\t" + str(
#             ratios[i]) + "\n")
#         file_object.close()


def executeAlgorithm(algoname, graph):

    if algoname == "prim":
        prim = Prim()
        final_graph, _ = prim.prim_mst(graph, 1)
        kw = prim.get_weight(final_graph)

    elif algoname == "kruskal":
        mst = MST()
        final_graph = mst.kruskal_naive(graph)
        kw = mst.get_mst_weight(final_graph.E)

    elif algoname == "kruskal-opt":
        mst = MST()
        final_graph = mst.kruskal_union_find(graph)
        kw = mst.get_mst_weight(final_graph)
    else:
        pass

    return kw



def executeOneOfTheMostAdvancedFunctionInHumanHistoryToCalculateAsynthoticStuff(graphs, lock):

    outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"

    # ======= PRIM ========
    # executorPrim = concurrent.futures.ProcessPoolExecutor(max_workers=17)
    #loaderPrim = Loader("Executing quartet Prim...", "Executing quartet Prim... COMPLETED!", 0.05).start()
    print("Executing quartet Prim...")
    datasetNumber = 1
    graphsAccumulator = []
    datasetNumberAccumulator = []
    foo = 0
    for graph in graphs:
        if foo == 4:
            foo = 0
            output = "./quartet_prim_" + outputfilePostfix
            #executorPrim.submit(executeSingleThreadQuartetMeasurement, output, "prim", graphsAccumulator, datasetNumberAccumulator, lock)
            executeSingleThreadQuartetMeasurement(output, "prim", graphsAccumulator, datasetNumberAccumulator, lock)
            graphsAccumulator = []
            datasetNumberAccumulator = []
            
        if foo != 4:
            datasetNumberAccumulator.append(datasetNumber)
            graphsAccumulator.append(graph)
            datasetNumber += 1
            foo += 1
          
    # executorPrim.shutdown(wait=True)
    #loaderPrim.stop()


    # # ======= KRUSKAL UNION FIND ========

    print("Executing quartet Kruskal Union Find...")
    datasetNumber = 1
    graphsAccumulator = []
    datasetNumberAccumulator = []
    foo = 0
    for graph in graphs:
        if foo == 4:
            foo = 0
            output = "./quartet_kruskal_uf_" + outputfilePostfix
            #executorPrim.submit(executeSingleThreadQuartetMeasurement, output, "prim", graphsAccumulator, datasetNumberAccumulator, lock)
            executeSingleThreadQuartetMeasurement(output, "kruskal-opt", graphsAccumulator, datasetNumberAccumulator, lock)
            graphsAccumulator = []
            datasetNumberAccumulator = []
            
        if foo != 4:
            datasetNumberAccumulator.append(datasetNumber)
            graphsAccumulator.append(graph)
            datasetNumber += 1
            foo += 1


    # # ======= KRUSKAL NAIVE ========

    print("Executing quartet Kruskal Naive...")
    datasetNumber = 1
    graphsAccumulator = []
    datasetNumberAccumulator = []
    foo = 0
    for graph in graphs:
        if foo == 4:
            foo = 0
            output = "./quartet_kruskal_" + outputfilePostfix
            #executorPrim.submit(executeSingleThreadQuartetMeasurement, output, "prim", graphsAccumulator, datasetNumberAccumulator, lock)
            executeSingleThreadQuartetMeasurement(output, "kruskal", graphsAccumulator, datasetNumberAccumulator, lock)
            graphsAccumulator = []
            datasetNumberAccumulator = []
            
        if foo != 4:
            datasetNumberAccumulator.append(datasetNumber)
            graphsAccumulator.append(graph)
            datasetNumber += 1
            foo += 1



def executeSingleThreadQuartetMeasurement(outputfile, algoname, graphs, filenumbers, fileResultLock):

    # outputfile -> dove salvo i risultati
    # algoname --> quale tipo algoritmo eseguire
    # graphs --> i dataset file da eseguire
    # filenumbers --> i numeri dei dataset da eseguire
    # fileResultLock --> per l'accesso condiviso dei thread per la scrittura in append dei file
    # =======================================================

    executionTimes = 4

    # First execution
    
    averageTimePerQuartet = 0
    gc.disable()
    for graph in graphs:
        localStartTime = time.perf_counter_ns()
        executeAlgorithm(algoname, graph)
        averageTimePerQuartet += time.perf_counter_ns()-localStartTime
    gc.enable()
    
    averageTimePerQuartet /= 4

    # Check if execution time is less than 1 seconds
    # in case, take the avg time after 1000 execution


    if averageTimePerQuartet <= 1000000000: 

        numCalls = 1000
        sumTimePerQuartet = 0
        
        for graph in graphs:
            loopStartTime = time.perf_counter_ns()
            gc.disable()
            
            for i in range(numCalls):
                executeAlgorithm(algoname, graph)
            
            gc.enable()
            sumTimePerQuartet += (time.perf_counter_ns() - loopStartTime) / numCalls
        
        averageTimePerQuartet = sumTimePerQuartet / 4
        
        rightTime = averageTimePerQuartet
        executionTimes = 4*numCalls
    else:
        rightTime = averageTimePerQuartet
    
    #  n vertex | dataset number | n edges | avg num edges | time | exe times
    # 10 | (1,2,3,4) | (10, 9, 11, 12) | 10+eps  | 0.2345 | 4000

    outFilenumbers = "( "
    for i in filenumbers:
        outFilenumbers += str(i) + " "
    outFilenumbers += ")"

    outEdges = "( "
    for graph in graphs:
        outEdges = outEdges + str(len(graph.E)) + " "
    outEdges += ")"

    outAvgEdges = 0
    for graph in graphs:
        outAvgEdges += len(graph.E)
    outAvgEdges /= 4

    with fileResultLock: 
        file_object = open(outputfile, 'a')
        file_object.write(str(len(graphs[0].V)) + "\t" + outFilenumbers + "\t" + outEdges + "\t" + str(outAvgEdges) + "\t" + "{:.7f}".format(rightTime) + "\t" + "{:.7f}".format(rightTime/1000000000) + "\t" + str(executionTimes) + "\n")
        file_object.close()


    # =======================================================



#     num_calls = DEFAULT_NUM_CALLS
#     index = 0
#     sum_times = 0.0
#     datasetNumber = 1

#     # outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"
#     # output = "./output_measure_kruskal_opt_" + outputfilePostfix

# #dont
#     # file_object = open(output, 'a')
#     # file_object.write("Iteration\tn_vertex\ttime\n")
#     # file_object.close()

#     is_test_failed = False
#     times = []

#     for graph in graphs:
#         print('Graph: {}'.format(str(datasetNumber)))

#         if index == 0:
#             print('NEW DATASETS SEQUENCE')

#             # Speed test of the algorithm
#             gc.disable()
#             start_time = perf_counter_ns()

#             executeSingleThreadCalculus(output, "kruskal-opt", graph, datasetNumber)

#             end_time = perf_counter_ns()
#             gc.enable()

#             print('Speed test: {}s'.format(str((end_time - start_time) / 1000000000)))

#             if ((end_time - start_time) / 1000000000) >= 1.0:
#                 print('TEST PASSED')
#                 is_test_failed = False

#                 #times.append((end_time - start_time) / 1000000000)
#                 sum_times += (end_time - start_time)

#                 # file_object = open(output, 'a')
#                 # file_object.write(str(datasetNumber) + "\t" + str(len(graph.V)) + "\t" + "{:.7f}".format(
#                 #     (end_time - start_time)) + "\n")
#                 # file_object.close()
#             else:
#                 print('TEST FAILED')
#                 is_test_failed = True

#                 gc.disable()
#                 start_time = perf_counter_ns()

#                 for i in range(num_calls):
#                     executeSingleThreadCalculus(output, "kruskal-opt", graph, datasetNumber)

#                 end_time = perf_counter_ns()
#                 gc.enable()

#                 sum_times += (end_time - start_time) / num_calls
#         else:
#             if not is_test_failed:
#                 gc.disable()
#                 start_time = perf_counter_ns()

#                 executeSingleThreadCalculus(output, "kruskal-opt", graph, datasetNumber)

#                 end_time = perf_counter_ns()
#                 gc.enable()

#                 print('Time: {}s'.format(str((end_time - start_time) / 1000000000)))

#                 #times.append((end_time - start_time) / 1000000000)

#                 sum_times += (end_time - start_time)

#                 # file_object = open(output, 'a')
#                 # file_object.write(str(datasetNumber) + "\t" + str(len(graph.V)) + "\t" + "{:.7f}".format(
#                 #     (end_time - start_time)) + "\n")
#                 # file_object.close()

#             else:
#                 gc.disable()
#                 start_time = perf_counter_ns()

#                 for i in range(num_calls):
#                     executeSingleThreadCalculus(output, "kruskal-opt", graph, datasetNumber)

#                 end_time = perf_counter_ns()
#                 gc.enable()

#                 sum_times += (end_time - start_time) / num_calls

#         if index == 3:

#             avg_time = sum_times / (index + 1)
#             avg_time = avg_time / 1000000000
#             print('Avg time: {}'.format(str(avg_time)))

#             # run_times.append(round(avg_time / 20, 3))
#             times.append(avg_time)

#             # file_object = open(output, 'a')
#             # file_object.write(str(datasetNumber) + "\t" + str(len(graph.V)) + "\t" + "{:.7f}".format(avg_time) + "\n")
#             # file_object.close()

#             index = 0
#             is_test_failed = False
#             sum_times = 0.0
#         else:
#             index += 1

#         datasetNumber += 1

#     return times


# def executeTheSuperFancyPoolThreadsToCalculateMegaComplexGraphs(graphs):
#     outputfilePostfix = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".csv"
#     # executor = concurrent.futures.ThreadPoolExecutor(max_workers=24)
#     executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
#     datasetNumber = 1

#     # testing.. executeSingleThreadCalculus("./output_prim_" + outputfilePostfix, "prim", graphs[0], 1, lock)

#     # loader = Loader("Executing Prim...", "Executing Prim... COMPLETED!", 0.05).start()
#     loader = Loader("Executing Kruskal optimized...", "Executing Kruskal optimized... COMPLETED!", 0.05).start()

#     num_calls = DEFAULT_NUM_CALLS
#     index = 1

#     for graph in graphs:
#         print('Graph: {}'.format(str(index)))

#         # output = "./output_prim_" + outputfilePostfix
#         # executor.submit(executeSingleThreadCalculus, output, "prim", graph, datasetNumber, lock)

#         output = "./output_kruskal_opt_" + outputfilePostfix

#         # Speed test of the algorithm
#         gc.disable()
#         start_time = perf_counter_ns()
#         # start_time = time.time()

#         executor.submit(executeSingleThreadCalculus, output, "kruskal-opt", graph, datasetNumber)

#         end_time = perf_counter_ns()
#         # end_time = time.time()
#         gc.enable()

#         print('Speed test: {}s'.format(str((end_time - start_time) / 1000000000)))

#         if ((end_time - start_time) / 1000000000) >= 1.0:
#             file_object = open(output, 'a')
#             file_object.write(
#                 str(datasetNumber) + "\t" + str(len(graph.V)) + "\t" + "{:.7f}".format((end_time - start_time)) + "\n")
#             file_object.close()
#         else:
#             print('FAIL')
#             exit_flag = False

#             print('Num calls: {}'.format(str(num_calls)))

#             # Repeat until avg_time >= 1.0
#             while not exit_flag:

#                 gc.disable()
#                 start_time = perf_counter_ns()
#                 # start_time = time.time()

#                 for i in range(num_calls):
#                     executor.submit(executeSingleThreadCalculus, output, "kruskal-opt", graph, datasetNumber)

#                 end_time = perf_counter_ns()
#                 # end_time = time.time()
#                 gc.enable()

#                 # sum_times += (end_time - start_time) / num_calls
#                 avg_time = (end_time - start_time) / 1000000000
#                 avg_time = avg_time / num_calls

#                 datasetNumber += 1

#                 # avg_time = int(round(sum_times / num_instances))
#                 print('Avg time: {}'.format(str(avg_time)))

#                 if avg_time >= 1.0:

#                     # Reset variables
#                     exit_flag = True
#                     num_calls = DEFAULT_NUM_CALLS

#                     # Save the result
#                     file_object = open(output, 'a')
#                     file_object.write(
#                         str(datasetNumber) + "\t" + str(len(graph.V)) + "\t" + "{:.7f}".format(avg_time) + "\n")
#                     file_object.close()
#                 else:
#                     num_calls *= 10

#         index += 1

#     executor.shutdown(wait=True)
#     loader.stop()


# def executeSingleThreadCalculus(outputfile, algoname, graph, filename):
#     # localStartTime = time.time()

#     if algoname == "prim":
#         prim = Prim()
#         prim.prim_mst(graph, 1)

#     elif algoname == "kruskal":
#         mst = MST()
#         final_graph = mst.kruskal_naive(graph)

#     elif algoname == "kruskal-opt":
#         mst = MST()
#         final_graph = mst.kruskal_union_find(graph)

#     else:
#         pass

#     # endtime = time.time()-localStartTime

#     # with fileResultLock:
#     #     file_object = open(outputfile, 'a')
#     #     file_object.write(str(filename) + "\t" + str(len(graph.V)) + "\t" + "{:.7f}".format(endtime) + "\n")
#     #     file_object.close()


# if __name__ == "__main__":
#     main()