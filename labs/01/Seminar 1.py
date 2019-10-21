#!/usr/bin/env python
# coding: utf-8

# # NAIL025 - EVA - Seminar 1

# Imports
import ga # GeneticAlgorithms
import numpy as np # numpy
import pylab as py # plots
from tqdm import tqdm # status bar

# Hyperparameters
gene_length=31
population=10
generations=2000
r = 10

# OneMAX algorithm - we seek 111111111111111111...
class OneMax(ga.algorithms.BaseGeneticAlgorithm):
    def eval_fitness(self, chromosome):
        """
        Evaluate the fitness score for a chromosome.
        Does not use caching.
        You should probably call get_fitness().
        """
        score=0
        for gene in chromosome.genes:
            score += sum(map(int, gene.dna))
        return score

# Sum every other 1 in gene return both odd and even variants
def count(l):
    scoreA=0
    scoreB=0
    for i in range(0, len(l)):
        if i%2==0:
            scoreA+=l[i]
        else:
            scoreB+=l[i]
        
    return scoreA, scoreB

# Find gene with every other base equal to 1
class EveryOther(ga.algorithms.BaseGeneticAlgorithm):
    def eval_fitness(self, chromosome):
        """
        Evaluate the fitness score for a chromosome.
        Does not use caching.
        You should probably call get_fitness().
        """
        score=0
        for gene in chromosome.genes:
            scoreA, scoreB = count(list(map(int, gene.dna)))
            score += max(scoreA-scoreB, scoreB-scoreA)
        return score

def doTheWork(algorithm, r, generations, gene_length, population):
    print('Running {}'.format(algorithm.__name__))
    runs = []
    parameters = [
        (r, generations,0.15,0.6),
        # (r, generations, 0.06, 0.3),
        # (r, generations, 0.4, 0.0),
        # (r, generations, 0.0, 0.5)
    ]

    with tqdm(total=sum(map(lambda item: item[0], parameters))) as bar:
        for (r, generations, p_mutate, p_crossover) in parameters:
            algs = []
            for _ in range(r):
                # Prepare genes
                chromosomes = ga.chromosomes.Chromosome.create_random(gene_length=gene_length, n=population) 

                # Init alg
                alg = algorithm(chromosomes)

                # Simulate generations
                alg.run(generations, p_mutate, p_crossover)
                algs.append((alg, generations, p_mutate, p_crossover))
                bar.update(1)
            runs.append((r, generations, p_mutate, p_crossover, algs))

    for (r, generations, p_mutate, p_crossover, algs) in runs:
        data = []
        for (alg, _, _, _) in algs:
            d = np.array([v for k, v in sorted(alg.overall_fittest_fit.items())], dtype=np.float64)
            if not any(data):
                data = d
            else:
                data += d
        data /= len(algs)
        
        py.plot(data, label='{} ; {} ; {}'.format(generations,p_mutate,p_crossover))
        py.fill_between(data, np.percentile(data, q=0.25, axis=0), np.percentile(data, q=0.75, axis=0), alpha=0.3)
        
    py.rcParams['figure.figsize'] = [10, 8]
    py.xlabel('generation')
    py.ylabel('fitness')
    py.legend(loc='best')
    py.show()

doTheWork(EveryOther, r, generations, gene_length, population)