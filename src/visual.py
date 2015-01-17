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
def geneticVisuals(intervals,metrop,metropLinkage,stoch,ranking,det,anneal,rand):

	# Convert the interval set into a sorted list
	intervals = sorted(list(intervals))

	# Get errors
	metropBars = applyLog(errorBars(metrop,intervals))
	metropLinkageBars = applyLog(errorBars(metropLinkage,intervals))
	stochBars = applyLog(errorBars(stoch,intervals))
	rankingBars = applyLog(errorBars(ranking,intervals))
	detBars = applyLog(errorBars(det,intervals))
	annealBars = applyLog(errorBars(anneal,intervals))
	randBars = applyLog(errorBars(rand,intervals))

	# Average Values over multiple iterations - take logarithm (since
		# the fitness values can be in the thousands)
	metrop = applyLog(collapse(metrop))
	metropLinkage = applyLog(collapse(metropLinkage))
	stoch = applyLog(collapse(stoch))
	ranking = applyLog(collapse(ranking))
	det = applyLog(collapse(det))
	anneal = applyLog(collapse(anneal))
	rand = applyLog(collapse(rand))

	# Plot fitness results over predefined intervals
	pylab.plot(intervals,metrop,"red",label = "Metropolis")
	pylab.plot(intervals,metropLinkage,"green",label = "Metropolis Linkage")
	pylab.plot(intervals,stoch,"black", label = "Stoch. Univ. Samp.")
	pylab.plot(intervals,ranking,"blue", label = "Ranking")
	pylab.plot(intervals,det,"orange", label = "Determ. Crowding")
	pylab.plot(intervals,anneal,"yellow", label = "Simulated Annealing")
	pylab.plot(intervals,rand,"purple", label = "Random")


	print metrop
	print intervals
	print metropBars

	for x in range(len(intervals)):
		pylab.errorbar(intervals[x],metrop[x],yerr=metropBars[x],
		 linestyle="--", marker="None", color="red")
		pylab.errorbar(intervals[x],metropLinkage[x],yerr=metropLinkageBars[x],
		 linestyle="None", marker="None", color="green")
		pylab.errorbar(intervals[x],stoch[x],yerr=stochBars[x],
		 linestyle="None", marker="None", color="black")
		pylab.errorbar(intervals[x],ranking[x],yerr=rankingBars[x],
		 linestyle="None", marker="None", color="blue")
		pylab.errorbar(intervals[x],det[x],yerr=detBars[x],
		 linestyle="None", marker="None", color="orange")
		pylab.errorbar(intervals[x],anneal[x],yerr=annealBars[x],
		 linestyle="None", marker="None", color="yellow")
		pylab.errorbar(intervals[x],rand[x],yerr=randBars[x],
		 linestyle="None", marker="None", color="purple")

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

# Computes error bars for multiple simulations on
# each algorithm - represented as standard deviation
# over the square root of the number of iterations
def errorBars(data,inter):
	devs = []
	for x in range(len(data[0])):
		n = np.arange(0,len(data))
		for y in range(len(data)):
			n[y] = data[y][x]
		devs.append(np.std(n)/math.sqrt(inter[x]+1))
	return devs