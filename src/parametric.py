#! /usr/bin/python

from tools import *
import numpy
import random
import math
import time
import sys
from solvers import dynamicKnapsack

'''
Parametric optimizers for 0/1 knapsack - 
* Simulated annealer
* Random Search
'''

# Simulated annealer - optimizing solutions to 0/1
# knapsack - climber can get close to optimal or achieved
# if enough iterations and viable cooling factor
# Returns value of best knapsack found
def simulatedAnnealer(values,weights,limit,intervals,bound):

	# Starting temperature
	temp = 1000
	# Cooling interval
	interval = 250
	# Cooling factor
	coolFactor = 0.99
	# Initial individual
	pack = generatePack(values,weights,limit)
	g = []
	for x in range(len(pack)):
		g.append(pack[x])
	# Evaluations of fitness function performed
	evals = 0
	# Historical Fitness values
	histFit = []
	# The highest fitness observed so far
	topFitness = fitness(pack,values)

	while (True):
		for i in range(interval):
			rand = random.randint(0,len(values)-1)
			if (g[rand] == 0):
				if (weight(g,weights) + weights[rand] <= limit):
					g[rand] = 1
					f = fitness(g,values)
					if (f > topFitness):
						topFitness = f
			else:
				prob = math.exp(-values[rand]/temp)
				if (random.uniform(0,1) <= prob):
					g[rand] = 0
			evals += 1
			if (evals in intervals):
				histFit.append(topFitness)
			if (evals >= bound):
				return histFit
		temp *= coolFactor

# Randomly search state space of 0/1 knapsack
# Returns value of best knapsack found
def randomSearch(values,weights,limit,intervals,bound):
	topFitness = -1
	# Historical Fitness values
	histFit = []
	for i in range(1,bound+1):
		g = generatePack(values,weights,limit)
		f = fitness(g,values)
		if (f > topFitness):
			topFitness = f
		if (i in intervals):
			histFit.append(topFitness)
	return histFit