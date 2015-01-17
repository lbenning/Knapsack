import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pylab
import math
import numpy as np

'''
Visualization functions for knapsack results
'''

# Plot average times versus approx. factor epsilon for both
# genetic algorithm and the ptas
def geneticVsPtas(stochastic, tradMet, detCrowd, ptas, epsilons):

	stochRes = applyLog(flipCollapse(stochastic))
	ptah = applyLog(flipCollapse(ptas))
	dcra = applyLog(flipCollapse(detCrowd))
	tmta = applyLog(flipCollapse(tradMet))

	# Stoch. univ. sampling results
	pylab.plot(epsilons,stochRes,"red",label="GSUS")
	# Poly-time approx. scheme results
	pylab.plot(epsilons,ptah,"black",label="PTAS")
	# Deterministic crowding results
	pylab.plot(epsilons,dcra,"orange",label="GDET")
	# Metropolis results
	pylab.plot(epsilons,tmta,"purple",label="GMET")

	pylab.ylabel('Average Times (Seconds) (Log base 10)')
	pylab.xlabel('Epsilon Approximation Factors')
	pylab.title('Approximation times for Gen. Alg. vs PTAS')

	pylab.legend(loc='upper right')

	pylab.show()

# Logarithmically scales down values of an entire list
def applyLog(x):
	s = []
	for y in range(len(x)):
		s.append(math.log10(x[y]+1))
	return s

# Comparison of genetic algorithms - fitness vs evaluations
def geneticVisuals(intervals,metrop,stoch,ranking,det,anneal,rand):

	# Convert the interval set into a sorted list
	intervals = sorted(list(intervals))

	# Average Values over multiple iterations - take logarithm (since
		# the fitness values can be in the thousands)
	metrop = applyLog(collapse(metrop))
	stoch = applyLog(collapse(stoch))
	ranking = applyLog(collapse(ranking))
	det = applyLog(collapse(det))
	anneal = applyLog(collapse(anneal))
	rand = applyLog(collapse(rand))

	# Plot fitness results over predefined intervals
	pylab.plot(intervals,metrop,"red",label = "Metropolis")
	pylab.plot(intervals,stoch,"black", label = "Stoch. Univ. Samp.")
	pylab.plot(intervals,ranking,"blue", label = "Ranking")
	pylab.plot(intervals,det,"orange", label = "Determ. Crowding")
	pylab.plot(intervals,anneal,"green", label = "Simulated Annealing")
	pylab.plot(intervals,rand,"purple", label = "Random")

	pylab.ylabel('Fitness (Log base 10)')
	pylab.xlabel('Evaluations')
	pylab.title('Comparison of Genetic Algorithms with Parametric Optimizers')

	pylab.legend(loc='lower right')

	pylab.show()
	
# Plot fitness vs. evaluations for genetic algorithm approx.
# 0/1 knapsack problem
def fitnessVsEval(geneticSeries, intervals):

	genCollapse = collapse(geneticSeries)
	genBars = errorBars(geneticSeries,intervals)

	plt.plot(intervals,genCollapse,"red")

	plt.ylabel('Fitness')
	plt.xlabel('Evaluations')
	plt.title('Genetic Algorithm Performance on 0/1 Knapsack')

	for x in range(len(intervals)):
		plt.errorbar(intervals[x], genCollapse[x], yerr=genBars[x]*25,
		 linestyle="None", marker="None", color="red")

	plt.show()

def flipCollapse(data):
	t = []
	for x in range(len(data)):
		tot = 0
		for y in range(len(data[x])):
			tot += data[x][y]
		t.append(float(tot)/len(data[x]))
	return t

# Average results at each timestep
def collapse(data):
	t = []
	for x in range(len(data[0])):
		total = 0.0
		for y in range(len(data)):
			total += data[y][x]
		t.append(total/len(data))
	return t