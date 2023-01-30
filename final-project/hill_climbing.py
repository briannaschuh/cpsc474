import random
import sys
import csv

from policy import CompositePolicy, RandomThrower, RandomPegger, GreedyThrower, GreedyPegger
from cribbage import Game, evaluate_policies
from gene_policy import MyPolicy

class HillClimbing:
        def __init__(self, step_size):
            self.card_rankings = 13
            self.pegging_parameters = 8
            self.games = 10000
            self.step_size = step_size
            self.current_gene = None
            self.game = Game()
            self.benchmark = CompositePolicy(self.game, GreedyThrower(self.game), GreedyPegger(self.game))
            self.iterations = 0
            self.fitness_over_time = {}
        
        def initialize_pop(self): #initalize the population randomly
            params = self.card_rankings + self.pegging_parameters
            return [random.randint(0,5) for x in range(0, params)]
        
        def find_best_neighbor(self, gene): #find the best neighbor
            params = self.card_rankings + self.pegging_parameters
            neighbors = []
            for i in range(0, params):
                neighbors.extend(self.find_neighbors(gene, i))    
            best_neighbor, best_fit = max(map(lambda j: self.fitness(j), neighbors), key=lambda t: t[1])
            return (best_neighbor, best_fit)
            
        def fitness(self, gene): #evaluate a chromosome
            gene_policy = MyPolicy(self.game, gene)
            return gene, evaluate_policies(self.game, gene_policy, self.benchmark, self.games)[0]
            
        def find_neighbors(self, gene, index): #find the left and right neighbor of a chromosome
            left_gene = gene.copy()
            right_gene = gene.copy()
            left_gene[index] = gene[index] - self.step_size if gene[index] - self.step_size > 0 else 0
            right_gene[index] = gene[index] + self.step_size if gene[index] + self.step_size < 6 else 6
            return (left_gene, right_gene)
        
        def dict_to_csv(self, dictionary, name): #write to csv
            w = csv.writer(open(name, "w"))
            for key, val in dictionary.items():
                w.writerow([key, val])

def hillclimbing(step_size):
    genes = HillClimbing(step_size)
    genes.current_gene = genes.initialize_pop()
    gene_pol = MyPolicy(genes.game, genes.current_gene)
    best_fit = evaluate_policies(genes.game, gene_pol, genes.benchmark, genes.games)[0]
    no_best_neighbor = False
    while not no_best_neighbor:
        print("Iteration: ", genes.iterations)
        print("Best Fit", best_fit)
        print("Current gene", genes.current_gene)
        genes.fitness_over_time[genes.iterations] = best_fit
        genes.iterations += 1
        best_neighbor, best_neighbor_fit = genes.find_best_neighbor(genes.current_gene)
        if best_neighbor_fit > best_fit:
            best_fit = best_neighbor_fit
            genes.current_gene = best_neighbor
        else:
            no_best_neighbor = True

    genes.dict_to_csv(genes.fitness_over_time, "hillclimbing_fitnesschanges")
    return genes.current_gene, best_fit