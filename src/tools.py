'''
Utility class - provides various functions 
for knapsack simulations
'''

import random

# Generate a random bitstring representing
# a selection of items to place in the knapsack
# that satisfy the weight limit
def generatePack(values, weights, limit):
	 indiv = []
	 indic = []
	 for x in range(len(values)):
	 	indiv.append(0)
	 	indic.append(x)
	 knapWeight = 0
	 while (True):
	 	i = random.randint(0,len(indic)-1)
	 	index = indic.pop(i)
	 	if (weights[index] + knapWeight > limit):
	 		break
	 	else:
	 		indiv[index] = 1
	 		knapWeight += weights[index]
	 return tuple(indiv)

# Compute the fitness of the given individual
def fitness(indiv, values):
	ctr = 0
	for i in range(len(indiv)):
		if (indiv[i] == 1):
			ctr += values[i]
	return ctr

# Compute the weight of the given individual
def weight(indiv, weights):
	ctr = 0
	for i in range(len(indiv)):
		if (indiv[i] == 1):
			ctr += weights[i]
	return ctr

# Degrade the mutation rate over a predefined
# discrete set of values
def degradeMutation(evals):
	if (evals <= 5000):
		return 0.55
	elif (evals <= 20000):
		return 0.25
	elif (evals <= 40000):
		return 0.15
	elif (evals <= 60000):
		return 0.08
	elif (evals <= 80000):
		return 0.06
	else:
		return 0.04

# Reproduce between 2 parents to create one child
# This is done using 2 point crossover
def reproduce(parX,parY,weights,limit,mutRate):
	b1 = random.randint(len(weights)/4,len(weights)/2)
	b2 = random.randint(len(weights)/2+1,len(weights)*3/4)
	child = []
	for x in range(b1):
		child.append(parX[x])
	for x in range(b1,b2):
		child.append(parY[x])
	for x in range(b2,len(weights)):
		child.append(parX[x])

	# Check if merge invalidated the weight limit
	# Remove items from knapsack if necessary
	validate(child,weights,limit)

	# With probability <mutRate>, mutate the child
	if (random.uniform(0,1) <= mutRate):
		mutate(child,weights,limit)

	return tuple(child)

# Removes items from a knapsack until the weight
# limit is satisfied
def validate(indiv,weights,limit):
	w = weight(indiv, weights)
	if (w <= limit):
		return

	indices = []
	for x in range(len(indiv)):
		if (indiv[x] == 1):
			indices.append(x)

	while (w > limit and len(indices) > 0):
		target = random.randint(0,len(indices)-1)
		index = indices.pop(target)
		indiv[index] = 0
		w -= weights[index] 

# Perform mutation on a child
def mutate(child,weights,limit):
	flips = random.randint(1,5)
	w = weight(child,weights)
	for x in range(flips):
		i = random.randint(0,len(weights)-1)
		if (child[i] == 1):
			child[i] == 0
			w -= weights[i]
		else:
			if (w + weights[i] <= limit):
				child[i] = 1
				w += weights[i]

# Computes child replacement probability for generalized 
# crowding GA
def childProb(fitChild,fitPar,phi):
	if (fitChild > fitPar):
		return fitChild/(fitChild + phi*fitPar)
	elif (fitChild == fitPar):
		return 0.5
	else:
		return (phi*fitChild)/(phi*fitChild+fitPar)
	return num/denom

# Parses a file containing knapsack data.
# The first line contains a single value which
# is the weight limit of the knapsack
# where each line contains 2 values separated
# by spaces, the first is the value of an item and
# the second is the corresponding weight of that 
# item
def parser(filename):
	values = []
	weights = []
	f = open(filename, 'r')
	limit = int(f.readline())
	for line in f:
		s = line.split(" ")
		values.append(int(s[0]))
		weights.append(int(s[1]))
	f.close()
	return (values, weights, limit)

# Generates sample knapsack data
def generateData():
	limit = random.randint(1000,100000)
	items = random.randint(1000,1000)
	values = []
	weights = []
	for x in range(items):
		values.append(random.randint(10,1000))
		weights.append(random.randint(10,1000))
	return (values,weights,limit)

# Generates a small sized dataset
def generateSmall():
	limit = 10000
	items = 1000
	values = []
	weights = []
	for x in range(items):
		values.append(random.randint(10,1000))
		weights.append(random.randint(10,1000))
	return (values,weights,limit)

# Generate a medium sized dataset
def generateMedium():
	limit = 100000
	items = 2500
	values = []
	weights = []
	for x in range(items):
		values.append(random.randint(10,2500))
		weights.append(random.randint(10,2500))
	return (values,weights,limit)

# Generates a large dataset
def generateLarge():
	limit = 500000
	items = 5000
	values = []
	weights = []
	for x in range(items):
		values.append(random.randint(10,5000))
		weights.append(random.randint(10,5000))
	return (values,weights,limit)

# Parameterized data generation
def paramGeneration(limit,itemCt,lowBound,upBound):
	values = []
	weights = []
	for x in range(itemCt):
		values.append(random.randint(lowBound,upBound))
		weights.append(random.randint(lowBound,upBound))
	return (values,weights,limit)