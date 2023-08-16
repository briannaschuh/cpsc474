# Applications of Genetic Algorithms to Cribbage


In this project, I explored the application of genetic algorithms to optimize the pegging heuristic in the game of cribbage. By leveraging genetic algorithms and hill climbing techniques, I enhanced the performance of the AI agent's decision-making processes.

## Table of Contents
- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Algorithm Details](#algorithm-details)
- [Files](#files)
- [Results](#results)
- [Video Presentation](#video-presentation)
- [License](#license)

## Introduction
For my CPSC 474 final project, I programmed a genetic algorithm to tune the parameters on my CPSC 474 assignment 1 cribbage pegging heurisitc. For my chromosomes, I used value encoding. There are 21 paramaters in my hueristic, so each chromosome is a list of length 21, where each element in the list represents the value for a specific parameter. I also programmed a hill climbing algorithm to see how that would compare to the genetic algorithm. I used the cribbage code from assignment 1. `test_algo.py`  is the test script, `gene_policy.py` is my cribbage policy that works with both my genetic algorithm and my hill climbing algorithm, `genetic_algo.py` is my genetic algorithm, `hill_climbing.py` is my hill climbing algorithm, and `helper.py` is a helper function that I used for my discard policy. The rest of the files are from assignment 1 of cribbage and I did not modify any of them (except for the correction in Flush Scores). 

## Project Overview
- Genetic Algorithm: I implemented a genetic algorithm to optimize the parameters of the cribbage pegging policies.
- Hill Climbing: I employed hill climbing to see how it compares to the performance of the genetic algorithms.
- Pegging Policy: The pegging policy evaluates the value of starting a pegging phase with specific card ranks.
- Discard Policy: The discard policy determines optimal cards to keep and throw based on expected game outcomes.

## Algorithm Details
- Genetic Algorithm: Iteratively evolves a population of parameter sets for both the pegging policies.
  - Parameters: Initial population size, maximum generations, crossover and mutation probabilities.
  - Fitness Function: Winning percentage against a greedy AI agent in 10,000 simulated cribbage games.
- Hill Climbing: Explores neighboring solutions to refine parameter sets for both policies.
  - Parameters: Step size for exploring neighboring solutions.
  - Fitness Function: Same as the genetic algorithm.

## Files
- [gene_policy.py](gene_policy.py): Cribbage pegging, and discard policies. 
- [genetic_algo.py](genetic_algo.py): Genetic algorithm functions.
- [hill_climbing.py](hill_climbing.py): Hill climbing algorithm.
- [test_algo.py](test_algo.py): Script to run and compare genetic and hill climbing algorithms' performance.

## Results
The best chromosome found using the genetic algorithm had a fitness score of 0.2854 and its encoding is: [1.4152991466587599, 3.061374683412262, 2.1090475749414446, 3.3355579089036342, 1.5340859065920087, 2.073194506158668, 3.266679729245218, 2.96530792993779, 0.2896387826620216, 3.9769388023990926, 3.1869215396095063, 2.7729094415923203, 2.6236588203521403, 2.956640912706063, 2.5462872777631693, 2.8826268718360066, 2.9814119401938166, 1.830738749756002, 3.7306055677752568, 2.8875040965981142, 2.127343945441646]

Normally, my genetic algorithm can find a chromosome with a fitness score of about 0.28. 

## Video Presentation
For more information, please feel free to watch the [project presentation video](https://www.youtube.com/watch?v=h_wqpSOJAPg).

## License
This project is licensed under the [MIT License](LICENSE).

---

