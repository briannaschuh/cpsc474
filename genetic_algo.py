import random
import sys
import csv

from policy import CompositePolicy, RandomThrower, RandomPegger, GreedyThrower, GreedyPegger
from cribbage import Game, evaluate_policies
from gene_policy import MyPolicy

class GeneticAlgo:
    
    def __init__(self, initial_number, max_gen, prob_cross, prob_mutation):
        self.card_rankings = 13
        self.pegging_parameters = 8
        self.games = 10000
        self.game = Game()
        self.benchmark = CompositePolicy(self.game, GreedyThrower(self.game), GreedyPegger(self.game))
        self.initial_number = initial_number
        self.max_gen = max_gen
        self.prob_cross = prob_cross
        self.prob_mutation = prob_mutation
        self.parents_from_elitism = 2
        self.population = None
        self.all_fits = {}
        self.all_pop = {}
        self.counter = 0
    
    def initialize_pop(self): #initalize the population at random
        params = self.card_rankings + self.pegging_parameters
        total = self.initial_number
        pop = []
        for i in range(0, total):
            gene = [random.randint(0,5) for x in range(0, params)]#generate random gene
            pop.append(gene) #append
        return pop
    
    def evolve(self): #the evolution
        parents = self.population
        fit = self.fitness(parents)
        sorted_genes = self.elitism(parents, fit)
        selected_pop = self.selected_pop(parents, fit)
        crossover_pop = self.crossover(selected_pop)
        mutated_pop = self.mutate(crossover_pop)
        self.population = sorted_genes[0:self.parents_from_elitism] + mutated_pop
    
    def fitness (self, population): #calculate the fitness scores of the population
        N = len(population)
        f = []
        for i in range(0, N):
            gene_pol = MyPolicy(self.game, population[i]) #create a fresh policy
            results = evaluate_policies(self.game, gene_pol, self.benchmark, self.games) #evaluate 
            #print("results", results)
            f.append(results[0]) #append to fitness
        self.all_pop[self.counter] = population
        self.all_fits[self.counter] = f
        self.counter += 1
        return f #return all scores

    def selected_pop(self, population, fit): #select the parents
        parents = self.roulette(population, fit)
        return parents
            
    def crossover(self, parents): #perform crossover
        offspring = []
        N = len(parents)
        total_encodings = self.pegging_parameters + self.card_rankings
        for i in range(0, N):
            if random.randint(0, 100) < self.prob_cross:
                weight = random.randint(0, 100)/100
                p = parents[i]
                child1 = [p[0][j]*weight + p[1][j]*(1-weight) for j in range(0, total_encodings)]
                child2 = [p[1][j]*weight + p[0][j]*(1-weight) for j in range(0, total_encodings)]
                offspring.append(child1)
                offspring.append(child2)
            else:
                offspring.append(parents[i][0])
                offspring.append(parents[i][1])
        return offspring
    
    def mutate(self, children): #mutate the offspring
        N = len(children)
        total_encodings = self.pegging_parameters + self.card_rankings
        indices = total_encodings - 1
        for i in range(0, N):
            while random.randint(0, 100) < self.prob_mutation:
                mutated_index = random.randint(0, indices)
                change = random.randint(0,100)/100
                operation = random.randint(0,1)
                constant = 1 if operation else -1
                children[i][mutated_index] += constant*change
        
        return children
                
    def elitism(self, population, fit): #preserve the best two chromosomes in the population and pass them onto the next generation as they are
        return [x for _, x in sorted(zip(fit, population), reverse = True)]
    
    def roulette(self, population, fit): #Roulette selection
        fitness_sum = sum(fit) #sum up all of the fitnesses
        percents = [x/fitness_sum for x in fit]
        parents = []
        for i in range(int(self.parents_from_elitism/2), int(self.initial_number/2)):
            pair = random.choices(population, weights = percents, k = 2)
            parents.append(pair)
        return parents
    
    def dict_to_csv(self, dictionary, name): #write to csv
        w = csv.writer(open(name, "w"))
        for key, val in dictionary.items():
            w.writerow([key, val])
        
        
def results(initial_number, max_gen, prob_cross, prob_mutation):
    genes = GeneticAlgo(initial_number, max_gen, prob_cross, prob_mutation)
    genes.population = genes.initialize_pop()
    #print(genes.population)
    for i in range(0, max_gen):
        genes.evolve()
        print("Just went through generation", i)
        print("Population: ", genes.population)
    final_fitness = genes.fitness(genes.population)
    genes.all_fits[max_gen] = final_fitness
    genes.all_pop[max_gen] = genes.population
    genes.dict_to_csv(genes.all_fits, "all_fits")
    genes.dict_to_csv(genes.all_pop, "all_pop")
    
    max_fit = max(final_fitness)
    max_fit_index = final_fitness.index(max_fit)
    
    return genes.population[final_fitness.index(max_fit)], max_fit
    
    
