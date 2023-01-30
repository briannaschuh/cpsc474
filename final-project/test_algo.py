import sys

from policy import CompositePolicy, RandomThrower, RandomPegger, GreedyThrower, GreedyPegger
from cribbage import Game, evaluate_policies
from gene_policy import MyPolicy
from genetic_algo import results
from hill_climbing import hillclimbing

if __name__ == "__main__":
    
    initial_number = 20
    max_generation = 25
    probability_crossover = 80
    probability_mutation = 40 
    step_size = 0.1
    
    '''
    I used a genetic algorithm to tune the parameters on my cribbage pegging heuristic. 
    I kept the initial number, max generation, probability crossover, probability mutatio, and step size as hard-coded because these were the values that gave me the best results for my algorithm.
    The fitness score measures the winning percentage of 10,000 games against a greedy agent.
    The best chromosome found using the genetic algorithm had a fitness score of 0.2854 and its encoding is: 
    [1.4152991466587599, 3.061374683412262, 2.1090475749414446, 3.3355579089036342, 1.5340859065920087, 2.073194506158668, 3.266679729245218, 2.96530792993779, 0.2896387826620216, 3.9769388023990926, 3.1869215396095063, 2.7729094415923203, 2.6236588203521403, 2.956640912706063, 2.5462872777631693, 2.8826268718360066, 2.9814119401938166, 1.830738749756002, 3.7306055677752568, 2.8875040965981142, 2.127343945441646]
    Normally, my genetic algorithm can find a chromosome with a fitness score of about 0.28
    Please see README.md for more information.
    '''
    
    ga_best_gene, ga_best_fitness = results(initial_number, max_generation, probability_crossover, probability_mutation)
    hc_final_gene, hc_final_fitness = hillclimbing(step_size)
    print("Best Gene in GA: ", ga_best_gene)
    print("Fitness of Best Gene in GA: ", ga_best_fitness)
    print("Best Gene in HC: ", hc_final_gene)
    print("Fitness of Best Gene in HC: ", hc_final_fitness)