import math

'''

Algorithms for the 0/1 knapsack problem

Dynamic Programming
  - Solves for exact solution.

PTAS:
  - Poly-Time Approximation Scheme - Rounds values
    and calls dynamic program to solve - achieves (1+eps.)
    approximation to the optimal knapsack value.

'''

# Dynamic programming algorithm for solving 
# 0/1 knapsack exactly
# Returns 2-tuple t of the form:
# t[0] = Value of the optimal solution
# t[1] = Indices of items selected
def dynamicKnapsack(values,weights,limit):

	# The ith entry stores the max value achievable 
	# with weight limit i
	memo = {}
	# The ith entry stores the items selected corresponding
	# to the ith value in memo
	indices = {}
	# Base cases
	memo[0] = 0
	indices[0] = []
	# Optimum value
	optimumValue = float('-inf')
	optimumIndices = []

	# Try all items, memoizing subsolutions and tracking the optimum
	for x in range(len(values)):
		y = limit
		while (y >= weights[x]):
			if (y - weights[x] in memo):
				if (y in memo and values[x] + memo[y-weights[x]] > memo[y] or y not in memo):
					# Update memoized value
					memo[y] = values[x] + memo[y-weights[x]]
					# Update memoized indices
					cp = indices[y-weights[x]][:]
					cp.append(x)
					indices[y] = cp
					# Attempt to update the optimum
					if (memo[y] > optimumValue):
						optimumValue = memo[y]
						optimumIndices = indices[y]
			y -= 1

	# Return the value of the optimum
	return (optimumValue,optimumIndices)

# Polynomial time approximation scheme for solving
# knapsack within a 1+epsilon factor
# Returns 2-tuple t of the form:
# t[0] = Value of the approximate solution
# t[1] = Indices of items selected
def knapsackPtas(values,weights,limit,epsilon):
	# Find maximum values
	maxValue = -1
	for v in values:
		if (v > maxValue):
			maxValue = v
	roundFactor = epsilon*float(maxValue)/len(values)

	# Scale down values and floor to integers
	scaledValues = []
	for v in values:
		scaledValues.append(int(math.floor(v/roundFactor)))

	# Return results of dynamic program running on scaled values
	res = dynamicKnapsack(scaledValues,weights,limit)
	trueValue = 0
	for x in res[1]:
		trueValue += values[x]
	return (trueValue,res[1])