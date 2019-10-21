import matplotlib.pyplot as plt
import random
import pprint

import numpy as np

POP_SIZE = 100
IND_LEN = 25
CX_PROB = 0.0
MUT_PROB = 0.05
MUT_FLIP_PROB = 0.1

# creates a single individual of lenght `lenght`


def create_ind(length):
    return [random.randint(0, 1) for _ in range(length)]

# creates a population of `size` individuals


def create_population(size):
    return [create_ind(IND_LEN) for _ in range(size)]

# tournament selection
# def selection(pop, fits):
#     selected = []
#     for _ in range(len(pop)):
#         i1, i2 = random.randrange(0, len(pop)), random.randrange(0, len(pop))
#         if fits[i1] > fits[i2]:
#             selected.append(pop[i1])
#         else:
#             selected.append(pop[i2])
#     return selected

# roulette wheel selection


def selection(pop, fits):
    return random.choices(pop, fits, k=POP_SIZE)

# one point crossover


def cross(p1, p2):
    point = random.randint(0, len(p1))
    o1 = p1[:point] + p2[point:]
    o2 = p2[:point] + p1[point:]
    return o1, o2

# applies crossover to all individuals


def crossover(pop):
    off = []
    for p1, p2 in zip(pop[0::2], pop[1::2]):
        o1, o2 = p1[:], p2[:]
        if random.random() < CX_PROB:
            o1, o2 = cross(p1[:], p2[:])
        off.append(o1)
        off.append(o2)
    return off

# bit-flip mutation


def mutate(p):
    if random.random() < MUT_PROB:
        return [1 - i if random.random() < MUT_FLIP_PROB else i for i in p]
    return p[:]

# applies mutation to the whole population


def mutation(pop):
    return list(map(mutate, pop))

# applies crossover and mutation


def operators(pop):
    pop1 = crossover(pop)
    return mutation(pop1)

# evaluates the fitness of the individual


def onemax(ind):
    return sum(ind)

# Sum every other 1 in gene return both odd and even variants


def count(l):
    scoreA = 0
    scoreB = 0
    for i in range(0, len(l)):
        if i % 2 == 0:
            scoreA += l[i]
        else:
            scoreB += l[i]

    return scoreA, scoreB


def everyother(ind):
    scoreA, scoreB = count(ind)
    return max(scoreA-scoreB, scoreB-scoreA)

# implements the whole EA


def evolutionary_algorithm(fitness):
    pop = create_population(POP_SIZE)
    log = []
    for G in range(100):
        fits = list(map(fitness, pop))
        log.append((G, max(fits), sum(fits)/100, G*POP_SIZE))
        # print(G, sum(fits), max(fits)) # prints fitness to console
        mating_pool = selection(pop, fits)
        offspring = operators(mating_pool)
        # pop = offspring[:-1]+[max(pop, key=fitness)] #SGA + elitism
        pop = offspring[:]  # SGA

    return pop, log


# run the EA 10 times and aggregate the logs, show the last gen in last run
fitness = onemax
logs = []
for i in range(10):
    random.seed(i)
    pop, log = evolutionary_algorithm(fitness)
    logs.append(log)
fits = list(map(fitness, pop))

# extract fitness evaluations and best fitnesses from logs
evals = []
best_fit = []
for log in logs:
    evals.append([l[3] for l in log])
    best_fit.append([l[1] for l in log])

evals = np.array(evals)
best_fit = np.array(best_fit)

# plot the converegence graph and quartiles
# plt.plot(evals[0, :], np.median(best_fit, axis=0))
# plt.fill_between(evals[0, :], np.percentile(best_fit, q=25, axis=0),
#                  np.percentile(best_fit, q=75, axis=0), alpha=0.2)
# plt.show()

idx = evals[0, :]
mins = np.min(best_fit, axis=0)
q_25 = np.percentile(best_fit, q=25, axis=0)
medians = np.median(best_fit, axis=0)
q_75 = np.percentile(best_fit, q=75, axis=0)
maxs = np.max(best_fit, axis=0)

# Save logs to file
filename = 'sga_{}_{}_{}_{}_{}_{}'.format(fitness.__name__,
                                          POP_SIZE, IND_LEN, CX_PROB, MUT_PROB, MUT_FLIP_PROB)
with open('logs/01/{}.log'.format(filename), 'w+') as f:
    f.writelines(map(lambda t: ' '.join(map(str, t)) + '\n', zip(
        idx, mins, q_25, medians, q_75, maxs)))
