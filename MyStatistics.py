#!/usr/bin/python

import math

class StatisticsAccumulator:
    """Accepts one value at a time and keeps track of the associated statistics"""
    def __init__(self):
        self.__welford_mean__ = 0.0
        self.__welford_i_var__ = 0.0
        self.i = 0

    # Maintain the statistics for each estimate
    def update_statistics(self, estimate):
        self.i += 1
        self.__update_i_var__(estimate) # The previous mean is used in this calculation, so calculate this first
        self.__update_mean__(estimate)

    # Account for the new value in the Welford mean
    def __update_mean__(self, estimate):
        self.__welford_mean__ += (1.0/self.i) * (estimate - self.__welford_mean__)

    # Account for the new value in the Welford iVar
    def __update_i_var__(self, estimate):
        self.__welford_i_var__ += ((self.i-1.0)/self.i) * (estimate - self.__welford_mean__)**2

    # Functions to return the statistics
    def get_mean(self):
        return self.__welford_mean__

    def get_variance(self):
        return self.__welford_i_var__ / float(self.i)

    def get_stdev(self):
        return math.sqrt(self.get_variance())