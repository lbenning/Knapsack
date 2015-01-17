#! /usr/bin/python

import sys
import time
import solvers
import numpy
import visual
import random
import cPickle
from tools import *
from traditionalGA import geneticTraditional
from crowdingGA import generalizedCrowd
from metropolisGA import geneticMetropolis

# Runs genetic alg. on dataset to achieve 1+eps. approx, and returns
# result time tuple (epsilon,time). This is a traditional GA - performs
# selection, crossover then mutation as normal. Selection is done either as
# roulette (selection=True) or stoch. univ. sampling (selection=False)
def geneticApprox(dataset, epsilon, popSize, recombRate, selection, exactSoln):
	startTime = time.time()
	geneticTraditional(popSize, recombRate, 
		dataset[0], dataset[1], dataset[2], selection, epsilon, exactSoln)
	endTime = time.time()
	return endTime-startTime

# Metropolis GA - 
def metropolisApprox(dataset, epsilon, popSize, exactSoln):
	startTime = time.time()
	geneticMetropolis(popSize, dataset[0],
	 dataset[1], dataset[2], epsilon, exactSoln)
	endTime = time.time()
	return endTime-startTime

# Generalized crowding - capable of performing both
# deterministic and probabilistic crowding methods to maintain
# diversity
def crowdingApprox(dataset, epsilon, popSize, exactSoln, phi):
	startTime = time.time()
	generalizedCrowd(popSize, dataset[0],
	 dataset[1], dataset[2], epsilon, exactSoln, phi)
	endTime = time.time()
	return endTime-startTime

# Runs PTAS on dataset to achieve 1+eps. approx. and returns result time
# tuple (epsilon, time)
def knapsackPtas(dataset, epsilon):
	startTime = time.time()
	solvers.knapsackPtas(dataset[0],dataset[1],dataset[2],epsilon)
	endTime = time.time()
	return endTime-startTime

# Gateway to the knapsack simulation
# Runs :
# - PTAS
# - GA with Stoch Univ. Samp + 2 Pt. Crossover
# - GA with Ranking + 2 Pt. Crossover
def main(epsilon,iterations,density,delta):

	startTime = time.time()

	print "Generating random dataset(s)..."
	datasets = []
	for i in range(iterations):
		datasets.append(generateSmall())

	# Predefined constants that empirically tend to make the GA run
	# the best on the randomly generated datasets
	popSize = 60
	recombRate = 0.20

	# Dataset results that will be plotted. Each array will hold
	# at every index j the average time to solve all datasets to
	# within a factor of epsilons[j]
	geneticMeansStoch = numpy.zeros((density,iterations))
	metropolisMeans = numpy.zeros((density,iterations))
	detCrowdingMeans = numpy.zeros((density,iterations))
	ptasMeans = numpy.zeros((density,iterations))

	# These are the various epsilon approximation factors that will
	# be employed. The user specifies a base epsilon, and this is incremented
	# density times by delta
	epsilons = numpy.zeros((density))
	eps = epsilon

	print "Computing exact solutions..."

	# Compute the exact solutions to the generated datasets - cache them to be used in the
	# various genetic algorithms
	exactSolutions = numpy.zeros(iterations)
	for i in range(iterations):
		exactSolutions[i] = solvers.dynamicKnapsack(datasets[i][0],datasets[i][1],datasets[i][2])[0]

	# Begin the genetic simulations - woohoo!
	for d in range(density):
		print "Knapsack simulations on epoch " + str(d) + "..."
		for i in range(iterations):
			metropolisMeans[d][i] = metropolisApprox(datasets[i],eps,popSize,exactSolutions[i])
			print "Metropolis genetic algorithm took " + str(metropolisMeans[d][i])
			geneticMeansStoch[d][i] = geneticApprox(datasets[i],eps,popSize,recombRate,False,exactSolutions[i])
			print "Stochastic universal sampling algorithm took " + str(geneticMeansStoch[d][i])
			detCrowdingMeans[d][i] = crowdingApprox(datasets[i],eps,popSize,exactSolutions[i],0)
			print "Deterministic crowding genetic algorithm took " + str(detCrowdingMeans[d][i])
			ptasMeans[d][i] = knapsackPtas(datasets[i],eps)
			print "The polynomial-time approximation scheme took " + str(ptasMeans[d][i])
		# Record the epsilon used
		epsilons[d] = eps
		# Increment epsilon to the next value
		eps += delta

	endTime = time.time()

	print "The program ran for " + str(endTime-startTime) + " seconds..."
	
	# Call the visualizer to plot fitness vs time (seconds)
	visual.geneticVsPtas(geneticMeansStoch, metropolisMeans, detCrowdingMeans, ptasMeans, epsilons)
	
'''
arg1 : float value - base epsilon approximation factor
arg2 : int value :- number of iterations per unique epsilon (i.e. per epoch)
arg3 : int value : number of different epsilon to try = number of epochs
arg4 : float value : value to increase epsilon by every epoch
'''
if __name__ == '__main__':
	main(float(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]))