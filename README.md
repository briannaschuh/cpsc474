# Applications of Genetic Algorithms to Cribbage


In this project, I explore the application of genetic algorithms to optimize the pegging heuristic in the game of cribbage. By leveraging genetic algorithms and hill climbing techniques, I aim to enhance the performance of the AI agent's decision-making processes.

## Table of Contents
- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Algorithm Details](#algorithm-details)
- [Files](#files)
- [Results](#results)
- [Video Presentation](#video-presentation)
- [License](#license)

## Introduction
Cribbage is a card game that demands strategic thinking during the pegging and discard phases. This project delves into optimizing both the pegging and discard policies using genetic algorithms. Ultimately, the goal is to create an agent that plays cribbage at its optimal performance. 

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
- [final-project/gene_policy.py](final-project/gene_policy.py): Cribbage pegging, and discard policies. 
- [final-project/genetic_algo.py](final-project/genetic_algo.py): Genetic algorithm functions.
- [final-project/hill_climbing.py](final-project/hill_climbing.py): Hill climbing algorithm.
- [final-project/test_algo.py](final-project/test_algo.py): Script to run and compare genetic and hill climbing algorithms' performance.

## Results
The best chromosome found using the genetic algorithm had a fitness score of 0.2854 and its encoding is: [1.4152991466587599, 3.061374683412262, 2.1090475749414446, 3.3355579089036342, 1.5340859065920087, 2.073194506158668, 3.266679729245218, 2.96530792993779, 0.2896387826620216, 3.9769388023990926, 3.1869215396095063, 2.7729094415923203, 2.6236588203521403, 2.956640912706063, 2.5462872777631693, 2.8826268718360066, 2.9814119401938166, 1.830738749756002, 3.7306055677752568, 2.8875040965981142, 2.127343945441646]

Normally, my genetic algorithm can find a chromosome with a fitness score of about 0.28. 

## Video Presentation
For more information, please feel free to watch the [project presentation video](https://www.youtube.com/watch?v=h_wqpSOJAPg).

## License
This project is licensed under the [MIT License](LICENSE).

---

