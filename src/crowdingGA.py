import random
import numpy
from tools import *
import math

# Computes the Hamming distance between 2 bitstrings,
# which is simply the number of places where the bitstrings
# differ in value
def hammingDistance(x,y):
	dist = 0
	for z in range(len(x)):
		if (not x[z] == y[z]):
			dist += 1
	return dist

# Genetic algorithm that uses generalized crowding for diversity
# maintenance - base on parameter phi:
# - phi = 0 => Deterministic Crowding
# - 0 < phi < 1 => Probabilistic Crowding
def generalizedCrowd(popSize,values,weights,limit,epsilon,exactSoln,phi):

	# Initialization
	population = []
	for x in range(popSize):
		population.append(generatePack(values,weights,limit))
	# Track number of evaluations of fitness function
	fitCtr = 0
	# Mutation rate that will be degraded
	mut = degradeMutation(fitCtr)
	# Top individual's fitness
	topFitness = -1
	# Pairing indices for tournament 
	pairing = numpy.arange(0,popSize)

	while(True):

		# Run a tournament
		numpy.random.shuffle(pairing)
		curr = 0
		while (curr+1 < len(population)):
			parent1 = population[pairing[curr]]
			parent2 = population[pairing[curr+1]]

			child1 = reproduce(parent1,parent2,weights,limit,mut)
			child2 = reproduce(parent2,parent1,weights,limit,mut)

			# Compute fitnesses of parents and children
			fitnesses = (fitness(parent1,values),fitness(parent2,values),fitness(child1,values),
				fitness(child2,values))

			# Update the top fitness if new best achieved
			topFitness = max(topFitness,fitnesses[0],fitnesses[1],
				fitnesses[2],fitnesses[3])

			# Replace according to Metropolis algorithm
			if (hammingDistance(parent1,child1)+hammingDistance(parent2,child2) >
				hammingDistance(parent1,child2)+hammingDistance(parent2,child1)):
				if (random.uniform(0,1) <= childProb(fitnesses[2],fitnesses[0],phi)):
					population[pairing[curr]] = child1
				if (random.uniform(0,1) <= childProb(fitnesses[3],fitnesses[1],phi)):
					population[pairing[curr+1]] = child2
			else:
				if (random.uniform(0,1) <= childProb(fitnesses[3],fitnesses[0],phi)):
					population[pairing[curr]] = child2
				if (random.uniform(0,1) <= childProb(fitnesses[2],fitnesses[1],phi)):
					population[pairing[curr+1]] = child1

			# Termination condition
			if (topFitness*(1+epsilon) >= exactSoln):
				return topFitness

			fitCtr += 4
			curr += 2

		# Update the mutation rate
		mut = degradeMutation(fitCtr)

# Genetic algorithm that uses generalized crowding for diversity
# maintenance - base on parameter phi:
# - phi = 0 => Deterministic Crowding
# - 0 < phi < 1 => Probabilistic Crowding
def recordCrowd(popSize,values,weights,limit,intervals,bound,phi):

	# Initialization
	population = []
	for x in range(popSize):
		population.append(generatePack(values,weights,limit))
	# Track number of evaluations of fitness function
	fitCtr = 0
	# Mutation rate that will be degraded
	mut = degradeMutation(fitCtr)
	# Top individual's fitness
	topFitness = -1
	# Pairing indices for tournament 
	pairing = numpy.arange(0,popSize)
	# Record fitnesses
	recFitnesses = []

	while(True):

		# Run a tournament
		numpy.random.shuffle(pairing)
		curr = 0
		while (curr+1 < len(population)):
			parent1 = population[pairing[curr]]
			parent2 = population[pairing[curr+1]]

			child1 = reproduce(parent1,parent2,weights,limit,mut)
			child2 = reproduce(parent2,parent1,weights,limit,mut)

			# Compute fitnesses of parents and children
			fitnesses = (fitness(parent1,values),fitness(parent2,values),fitness(child1,values),
				fitness(child2,values))

			# Update the top fitness if new best achieved
			topFitness = max(topFitness,fitnesses[0],fitnesses[1],
				fitnesses[2],fitnesses[3])

			# Replace according to Metropolis algorithm
			if (hammingDistance(parent1,child1)+hammingDistance(parent2,child2) >
				hammingDistance(parent1,child2)+hammingDistance(parent2,child1)):
				if (random.uniform(0,1) <= childProb(fitnesses[2],fitnesses[0],phi)):
					population[pairing[curr]] = child1
				if (random.uniform(0,1) <= childProb(fitnesses[3],fitnesses[1],phi)):
					population[pairing[curr+1]] = child2
			else:
				if (random.uniform(0,1) <= childProb(fitnesses[3],fitnesses[0],phi)):
					population[pairing[curr]] = child2
				if (random.uniform(0,1) <= childProb(fitnesses[2],fitnesses[1],phi)):
					population[pairing[curr+1]] = child1

			if (fitCtr+1 in intervals or fitCtr+2 in intervals or fitCtr+3 in intervals or 
				fitCtr+4 in intervals):
				recFitnesses.append(topFitness)

			fitCtr += 4
			curr += 2

			# Termination condition
			if (fitCtr >= bound):
				return recFitnesses

		# Update the mutation rate
		mut = degradeMutation(fitCtr)