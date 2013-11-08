#!/usr/bin/python
import random

import sys
import numpy as np
from collections import deque
from MyStatistics import StatisticsAccumulator

# The network from the book
TEST_NETWORK = ["1 2 3", "1 3 6", "1 4 13", "2 5 3", "2 3 9", "3 4 9", "3 6 7", "4 6 6", "5 6 3"]

# Necessary global constants
N = []
Y = []

# Stores the node prior to the specified node in the critical path (rather than better ways of doing it)
previous_nodes = []


# Returns the number of predecessor nodes to the current node
def len_of_B(j):
    return sum(map(lambda x: 1 if x == -1 else 0, N[j]))


# Calculates the completion time for the network, saving the critical path in the previous_nodes array
def T(j):
    global N, Y, previous_nodes
    k = 1                            # initialize index for columns of N
    l = 0                            # initialize index for predecessors to node j
    t_max = 0.0                      # initialize longest time of all paths to node j
    while l < len_of_B(j):           # loop through predecessor nodes to node j
        if N[j][k] == -1:            # if column k of N has arc entering node j
            i = 1                    # begin search for predecessor node
            while N[i][k] != 1:      # while i not a predecessor index
                i += 1               # increment i

            t = T(i) + Y[i][j]       # recursive call: t is completion time of a_ij
            if t >= t_max:
                t_max = t            # choose largest completion time
                previous_nodes[j] = i

            l += 1                   # increment predecessor index
        k += 1                       # increment column index

    return t_max                     # return completion time T j


# Parses the iterable (file or array) into a more usable format, and finds the number of nodes
def get_san_parameters(network_iterable):
    san_parameters = []
    terminal_node = 1
    for line in network_iterable:
        (from_node, to_node, upper_bound) = line.split()
        from_node = int(from_node)
        to_node = int(to_node)
        upper_bound = float(upper_bound)

        if from_node > terminal_node:
            terminal_node = from_node
        if to_node > terminal_node:
            terminal_node = to_node

        san_parameters.append((from_node, to_node, upper_bound))

    return san_parameters, terminal_node


# Creates the SAN by initializing N, Y, and the previous_nodes array
def generate_san(san_parameters, terminal_node):
    global N, Y, previous_nodes
    N = np.zeros(((terminal_node+1), (len(san_parameters)+1)))
    Y = np.zeros(((terminal_node+1), (terminal_node+1)))
    previous_nodes = [0] * (terminal_node+1)

    j = 0
    for (from_node, to_node, upper_bound) in san_parameters:
        j += 1
        N[from_node][j] = 1
        N[to_node][j] = -1
        Y[from_node][to_node] = random.uniform(0, upper_bound)


# Uses the previous_nodes array to create the list of arcs in the critical path
def generate_critical_path(terminal_node):
    critical_path = []

    node_1 = previous_nodes[terminal_node]
    node_2 = terminal_node

    while node_1 != 0:
        critical_path.append("a%d%d" % (node_1, node_2))
        node_2 = node_1
        node_1 = previous_nodes[node_1]

    return critical_path[::-1]


# Creates the string representation of the critical path from the list of arcs
def get_path_representation(critical_path):
    representation = ''.join([arc + ',' for arc in critical_path])
    representation = ":" + representation[:-1] + ":"
    return representation


def run_san(runs, network_params):
    # Get the parameters of the network
    san_parameters, terminal_node = get_san_parameters(network_params)

    # Initialize stuff for the output
    counts = {}
    stats = StatisticsAccumulator()

    # Run the experiment
    for i in xrange(runs):
        generate_san(san_parameters, terminal_node)

        max_time = T(terminal_node)
        stats.update_statistics(max_time)

        critical_path = generate_critical_path(terminal_node)
        critical_path_string = get_path_representation(critical_path)

        if critical_path_string in counts:
            counts[critical_path_string] += 1
        else:
            counts[critical_path_string] = 1

    # Print out the output
    for path in counts:
        count = counts[path]
        print "OUTPUT \t %-20s \t %20.4f" % (path, count/float(runs))

    print "The mean time to complete the network is ", stats.get_mean()