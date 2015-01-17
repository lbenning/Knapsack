#! /usr/bin/python

import tools
import multiprocessing as mp
import sys
import visual

import traditionalGA
import crowdingGA
import metropolisGA
import parametric

'''
Compare Genetic Algorithms
 - Fitness vs Evaluations
   Genetic Algorithms Employed:
     - Metropolis
     - Stoch Univ. Sampling
     - Ranking
     - Deterministic Crowding
     - Simulated Annealing
     - Random Search
'''

def main(evals,density,runs):

	# Parameter and data initialization
	popSize = 60
	recombRate = 0.20

	print "Creating large dataset..."

	dataset = tools.generateLarge()

	processPool = mp.Pool(processes=20)

	intervals = set()
	intervals.add(1)
	for x in range(1,density+1):
		intervals.add(x*(evals/density))

	print "Simulating Genetic Algorithms & Parametric Optimizers..."

	# Metropolis Crowding GA
	metroJobs = [processPool.apply_async(metropolisGA.recordMetropolis,
		args=(popSize,dataset[0],dataset[1],dataset[2],intervals,evals)) for x in range (runs)]

	# Stochastic Universal Sampling GA
	stochJobs = [processPool.apply_async(traditionalGA.recordTraditional,
		args=(popSize,recombRate,dataset[0],dataset[1],dataset[2],False,intervals,evals)) for x in range (runs)]

	# Ranking GA
	rankJobs = [processPool.apply_async(traditionalGA.recordTraditional,
		args=(popSize,recombRate,dataset[0],dataset[1],dataset[2],True,intervals,evals)) for x in range (runs)]

	# Deterministic Crowding GA
	detJobs = [processPool.apply_async(crowdingGA.recordCrowd,
		args=(popSize,dataset[0],dataset[1],dataset[2],intervals,evals,0.0)) for x in range (runs)]

	# Simulated Annealer
	annealJobs = [processPool.apply_async(parametric.simulatedAnnealer,
		args=(dataset[0],dataset[1],dataset[2],intervals,evals)) for x in range (runs)]

	# Random Search
	randJobs = [processPool.apply_async(parametric.randomSearch,
		args=(dataset[0],dataset[1],dataset[2],intervals,evals)) for x in range (runs)]

	# Lists to hold data results
	metroRes= [g.get() for g in metroJobs]
	stochRes = [g.get() for g in stochJobs]
	rankingRes = [g.get() for g in rankJobs]
	detRes = [g.get() for g in  detJobs]
	annealRes = [g.get() for g in annealJobs]
	randRes = [g.get() for g in randJobs]

	print "Simulation complete - Generating Plot..."

	visual.geneticVisuals(intervals,metroRes,stochRes,rankingRes,detRes,annealRes,randRes)

'''
arg1 : int value - number of evaluations to run each GA
arg2 : int value - number of runs for each GA
arg3 : int value - sampling density - number of points to record
fitness at - uniformly spread over the evaluations
'''
if __name__ == '__main__':
	main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))