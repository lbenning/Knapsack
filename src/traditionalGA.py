import random
import numpy
from tools import *
import math

# Returns parent indices using stochastic
# universal sampling procedure
def stochUnivSamp(maps, start, delta, ctr):
	indices = []
	x = 0
	while (len(indices) < ctr):
		while (start > 0):
			start -= maps[x][0]
			x += 1
		indices.append(maps[x-1][1])
		start += delta
	return indices

# Genetic algorithm simulation
def geneticTraditional(popSize, recombRate, values,
 weights, limit, select, epsilon, exactSoln):

	# Generate initial population - a list of tuples that are
	# bitstrings (0/1), where ith index is 1`if the ith item
	# is in the knapsack and 0 otherwise
	population = []
	for x in range(popSize):
		population.append(generatePack(values,weights,limit))

	# Track number of evaluations of fitness function
	fitCtr = 0
	# Mutation rate that will be degraded
	mut = degradeMutation(fitCtr)
	# Top individual's fitness
	topFitness = -1
	# Number of individuals to replace each round - must be even
	repIndivid = int(recombRate*popSize)
	if (repIndivid % 2 == 1):
		repIndivid += 1

	while(True):

		# List of tuples - first elmt. is fitness, which
		# is that of the individual at the index specified
		# by the second element
		maps = []

		# Compute fitnesses
		for x in range(popSize):
			f = fitness(population[x],values)
			maps.append((f,x))
			fitCtr += 1
			if (f > topFitness):
				topFitness = f
			if (topFitness*(1.0+epsilon) >= exactSoln):
				return topFitness

		maps.sort(reverse=True)

		# Generate children
		children = []

		# Ranking Selection
		if (select):
			x = 0
			while (x < repIndivid):
				parX = population[maps[x][1]]
				parY = population[maps[x+1][1]]
				childX = reproduce(parX,parY,weights,limit,mut)
				childY = reproduce(parY,parX,weights,limit,mut)
				children.append(childX)
				children.append(childY)
				x += 2
		# Stochastic universal sampling
		else:
			totalFitness = 0
			for m in maps:
				totalFitness += m[0]
			startPt = random.randint(0,totalFitness/repIndivid-1)
			delta = random.randint(1,totalFitness/repIndivid)
			parents = stochUnivSamp(maps,startPt,delta,repIndivid)
			p = 0
			while (p < len(parents)):
				childX = reproduce(population[parents[p]],population[parents[p+1]],
					weights,limit,mut)
				childY = reproduce(population[parents[p+1]],population[parents[p]],
					weights,limit,mut)
				children.append(childX)
				children.append(childY)
				p += 2

		# Replace bottom portion
		# of population with these individuals
		# Follows elitism - highest performing individuals
		# remain in the population
		x = len(maps)-1
		while (len(children) > 0):
			population[maps[x][1]] = children.pop()
			x -= 1

		#King of the hill
		if (maps[0][0] > maps[1][0]*2):
			population[maps[len(maps)-1][1]] = population[maps[0][1]]

		# Update the mutation rate
		mut = degradeMutation(fitCtr)

# Genetic algorithm simulation
def recordTraditional(popSize, recombRate, values,
 weights, limit, select, intervals, bound):

	# Generate initial population - a list of tuples that are
	# bitstrings (0/1), where ith index is 1`if the ith item
	# is in the knapsack and 0 otherwise
	population = []
	for x in range(popSize):
		population.append(generatePack(values,weights,limit))

	# Track number of evaluations of fitness function
	fitCtr = 0
	# Mutation rate that will be degraded
	mut = degradeMutation(fitCtr)
	# Top individual's fitness
	topFitness = -1
	# Number of individuals to replace each round - must be even
	repIndivid = int(recombRate*popSize)
	if (repIndivid % 2 == 1):
		repIndivid += 1
	# Record fitnesses
	recFitnesses = []

	while(True):

		# List of tuples - first elmt. is fitness, which
		# is that of the individual at the index specified
		# by the second element
		maps = []

		# Compute fitnesses
		for x in range(popSize):
			f = fitness(population[x],values)
			maps.append((f,x))
			fitCtr += 1
			if (f > topFitness):
				topFitness = f
			if (fitCtr in intervals):
				recFitnesses.append(topFitness)
			if (fitCtr >= bound):
				return recFitnesses

		maps.sort(reverse=True)

		# Generate children
		children = []

		# Ranking Selection
		if (select):
			x = 0
			while (x < repIndivid):
				parX = population[maps[x][1]]
				parY = population[maps[x+1][1]]
				childX = reproduce(parX,parY,weights,limit,mut)
				childY = reproduce(parY,parX,weights,limit,mut)
				children.append(childX)
				children.append(childY)
				x += 2
		# Stochastic universal sampling
		else:
			totalFitness = 0
			for m in maps:
				totalFitness += m[0]
			startPt = random.randint(0,totalFitness/repIndivid-1)
			delta = random.randint(1,totalFitness/repIndivid)
			parents = stochUnivSamp(maps,startPt,delta,repIndivid)
			p = 0
			while (p < len(parents)):
				childX = reproduce(population[parents[p]],population[parents[p+1]],
					weights,limit,mut)
				childY = reproduce(population[parents[p+1]],population[parents[p]],
					weights,limit,mut)
				children.append(childX)
				children.append(childY)
				p += 2

		# Replace bottom portion
		# of population with these individuals
		# Follows elitism - highest performing individuals
		# remain in the population
		x = len(maps)-1
		while (len(children) > 0):
			population[maps[x][1]] = children.pop()
			x -= 1

		#King of the hill
		if (maps[0][0] > maps[1][0]*2):
			population[maps[len(maps)-1][1]] = population[maps[0][1]]

		# Update the mutation rate
		mut = degradeMutation(fitCtr)