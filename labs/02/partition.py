import random
import numpy as np
import functools

import utils

K = 10  # number of piles
POP_SIZE = 1024  # population size
MAX_GEN = 20*1024  # maximum number of generations
CX_PROB = 0.0  # crossover probability
DIV_CON_PROB = 0.00  # probability of divide and conquer mutation
MUT_PROB = 0.1  # mutation probability (flip)
MUT_PROB_2 = 0.00  # mutation probability (switch)
MUT_FLIP_PROB = 1/500  # probability of chaninging value during mutation
MUT_SWITCH_PROB = 0.15  # probability of chaninging value during mutation
REPEATS = 10  # number of runs of algorithm (should be at least 10)
SURVIVES = 10  # number of survivors
OUT_DIR = 'final_bad_but_better'  # output directory for logs
# the ID of this experiment (used to create log names)
EXP_ID = 'k{}-p{}-g{}-s{}-x{}-m{}-mf{}-ms{}-dc{}-r{}(tuned)'.format(
    K, POP_SIZE, MAX_GEN, SURVIVES, CX_PROB, MUT_PROB, MUT_FLIP_PROB, MUT_SWITCH_PROB, DIV_CON_PROB, REPEATS)

# reads the input set of values of objects

# Vymena namisto presunu
# Zamena zatizena pravdepodobnosti - zalezi na vaze hromadky
# Mutace predmetu zatizena pravdepodobnosti vahou predmetu ? netestovano yet ?

# ~Rozdeleni a slouceni hromadek ? nejlehci a nejtezsi ?~
# ~Inteligentni inicializace hromadek (s lehkou randomizaci)~
# ~Informovane prehozeni z tezke hromadky na lehkou~


def read_weights(filename):
    with open(filename) as f:
        return list(map(int, f.readlines()))

# computes the bin weights
# - bins are the indices of bins into which the object belongs


def bin_weights(weights, bins):
    bw = [0]*K
    for w, b in zip(weights, bins):
        bw[b] += w
    return bw

# the fitness function


def fitness(ind, weights):
    bw = bin_weights(weights, ind)
    return utils.FitObjPair(fitness=1/(max(bw) - min(bw) + 1),
                            objective=max(bw) - min(bw))


def better_fitness(ind, weights):
    bw = bin_weights(weights, ind)
    M = sum(bw)/len(bw)
    S = sum(map(lambda w: (w-M)**2, bw)) ** (1/len(bw))
    return utils.FitObjPair(fitness=1/(S+1),
                            objective=max(bw) - min(bw))


def best_fitness(ind, weights):
    bw = bin_weights(weights, ind)
    M = sum(bw)/len(bw)
    S = sum(map(lambda w: abs(w-M), bw))
    F = 0.99**S
    return utils.FitObjPair(fitness=F,
                            objective=S)

# creates the individual


def create_ind(ind_len):
    return [random.randrange(0, K) for _ in range(ind_len)]


def create_ind_intelligent(ind_len, weights, bins, indx):
    r = np.ones((ind_len,), dtype=np.int16) * -1
    b = np.zeros((bins,))
    B = list(range(bins))

    for idx in indx:
        S = max(b)
        SS = sum(np.abs(b - S) ** 1.5)
        c = np.random.choice(B, 1, p=(np.abs(
            b - S) ** 1.5)/SS if S != 0 else [1/bins]*bins)
        b[c] += weights[idx]
        r[idx] = c

    return r

# creates the population using the create individual function


def create_pop(pop_size, create_individual):
    return [create_individual() for _ in range(pop_size)]

# the roulette wheel selection


def roulette_wheel_selection(pop, fits, k):
    return random.choices(pop, fits, k=k)


# implements the one-point crossover of two individuals


def one_pt_cross(p1, p2):
    point = random.randrange(1, len(p1))
    o1 = p1[:point] + p2[point:]
    o2 = p2[:point] + p1[point:]
    return o1, o2

# implements the "bit-flip" mutation of one individual


def flip_mutate(p, prob, upper):
    return [random.randrange(0, upper) if random.random() < prob else i for i in p]


def switch_mutate(p, prob, weights):
    W = bin_weights(weights, p)
    L = np.argmin(W)
    H = np.argmax(W)

    return [i if (i != L and i != H) or random.random() > prob else L for i in p]


def divide_and_conquer(p, weights):
    W = bin_weights(weights, p)
    L = np.argmin(W)
    H = np.argmax(W)

    items = []
    for i in range(len(p)):
        if p[i] == L or p[i] == H:
            items.append(i)
    items.sort(key=lambda item: weights[item])

    lW = 0
    hW = 0
    for i in range(len(items)):
        if lW <= hW:
            p[items[i]] = L
            lW += weights[items[i]]
        else:
            p[items[i]] = H
            hW += weights[items[i]]


# applies a list of genetic operators (functions with 1 argument - population)
# to the population


def mate(pop, operators):
    for o in operators:
        pop = o(pop)
    return pop

# applies the cross function (implementing the crossover of two individuals)
# to the whole population (with probability cx_prob)


def crossover(pop, cross, cx_prob):
    off = []
    for p1, p2 in zip(pop[0::2], pop[1::2]):
        if random.random() < cx_prob:
            o1, o2 = cross(p1, p2)
        else:
            o1, o2 = p1[:], p2[:]
        off.append(o1)
        off.append(o2)
    return off

# applies the mutate function (implementing the mutation of a single individual)
# to the whole population with probability mut_prob)


def mutation(pop, mutate, mut_prob):
    return [mutate(p) if random.random() < mut_prob else p[:] for p in pop]

# implements the evolutionary algorithm
# arguments:
#   pop_size  - the initial population
#   max_gen   - maximum number of generation
#   fitness   - fitness function (takes individual as argument and returns
#               FitObjPair)
#   operators - list of genetic operators (functions with one arguments -
#               population; returning a population)
#   mate_sel  - mating selection (funtion with three arguments - population,
#               fitness values, number of individuals to select; returning the
#               selected population)
#   map_fn    - function to use to map fitness evaluation over the whole
#               population (default `map`)
#   log       - a utils.Log structure to log the evolution run


def evolutionary_algorithm(pop, max_gen, fitness, operators, mate_sel, *, map_fn=map, log=None):
    evals = 0
    for _ in range(max_gen):
        fits_objs = list(map_fn(fitness, pop))
        evals += len(pop)
        if log:
            log.add_gen(fits_objs, evals)
        fits = np.array([f.fitness for f in fits_objs])
        max_fit = max(fits)
        fits /= max_fit
        _ = [f.objective for f in fits_objs]

        sample = list(range(len(fits)))
        sample.sort(key=lambda k: -fits[k])

        survivors = []
        for i in range(SURVIVES):
            survivors.append(pop[sample[i]])

        mating_pool = mate_sel(pop, fits, POP_SIZE)
        offspring = mate(mating_pool, operators)
        pop = offspring[:]
        pop += survivors

    return pop


if __name__ == '__main__':
    # read the weights from input
    weights = read_weights('inputs/partition-easy.txt')

    # use `functool.partial` to create fix some arguments of the functions
    # and create functions with required signatures
    indx = list(range(len(weights)))
    indx.sort(key=lambda item: weights[item])

    cr_ind = functools.partial(
        create_ind_intelligent, ind_len=len(weights), weights=weights, bins=K, indx=indx)
    fit = functools.partial(better_fitness, weights=weights)
    xover = functools.partial(crossover, cross=one_pt_cross, cx_prob=CX_PROB)
    mut = functools.partial(mutation, mut_prob=MUT_PROB,
                            mutate=functools.partial(flip_mutate, prob=MUT_FLIP_PROB, upper=K))
    mut2 = functools.partial(mutation, mut_prob=MUT_PROB_2,
                             mutate=functools.partial(switch_mutate, prob=MUT_SWITCH_PROB, weights=weights))
    mut3 = functools.partial(mutation, mut_prob=DIV_CON_PROB, mutate=functools.partial(
        divide_and_conquer, weights=weights))

    # we can use multiprocessing to evaluate fitness in parallel
    import multiprocessing
    pool = multiprocessing.Pool()

    import matplotlib.pyplot as plt

    # run the algorithm `REPEATS` times and remember the best solutions from
    # last generations
    best_inds = []
    for run in range(REPEATS):
        # initialize the log structure
        log = utils.Log(OUT_DIR, EXP_ID, run,
                        write_immediately=True, print_frequency=5)
        # create population
        pop = create_pop(POP_SIZE, cr_ind)
        # run evolution - notice we use the pool.map as the map_fn
        pop = evolutionary_algorithm(pop, MAX_GEN, fit, [
                                     xover, mut, mut2], roulette_wheel_selection, map_fn=pool.map, log=log)
        # remember the best individual from last generation, save it to file
        bi = max(pop, key=fit)
        best_inds.append(bi)

        with open(f'{OUT_DIR}/{EXP_ID}_{run}.best', 'w+') as f:
            for w, b in zip(weights, bi):
                f.write(f'{w} {b}\n')

        # if we used write_immediately = False, we would need to save the
        # files now
        # log.write_files()

    # print an overview of the best individuals from each run
    for i, bi in enumerate(best_inds):
        print(
            f'Run {i}: difference = {fit(bi).objective}, bin weights = {bin_weights(weights, bi)}')

    # write summary logs for the whole experiment
    utils.summarize_experiment(OUT_DIR, EXP_ID)

    # read the summary log and plot the experiment
    evals, lower, mean, upper = utils.get_plot_data(OUT_DIR, EXP_ID)
    plt.figure(figsize=(12, 8))
    utils.plot_experiment(evals, lower, mean, upper,
                          legend_name=EXP_ID)
    plt.legend()
    plt.show()

    # you can also plot mutiple experiments at the same time using
    # utils.plot_experiments, e.g. if you have two experiments 'default' and
    # 'tuned' both in the 'partition' directory, you can call
    # utils.plot_experiments('partition', ['default', 'tuned'],
    #                        rename_dict={'default': 'Default setting'})
    # the rename_dict can be used to make reasonable entries in the legend -
    # experiments that are not in the dict use their id (in this case, the
    # legend entries would be 'Default settings' and 'tuned')
