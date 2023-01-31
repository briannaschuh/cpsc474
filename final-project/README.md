For my final project, I programmed a genetic algorithm to tune the parameters on my assignment 1 cribbage pegging heurisitc. I used value encoding for the chromosomes. There are 21 paramaters in my hueristic, so each chromosome is a list of length 21, where each element in the list represents the value of a specific parameter. I also programmed a hill climbing algorithm to see how that would compare to the genetic algorithm. I used the cribbage code from assignment 1. test_algo.py  is the test script. gene_policy.py is my cribbage policy that works with both my genetic algorithm and my hill climbing algorithm. genetic_algo.py is my genetic algorithm, hill_climbing.py is my hill climbing algorithm, and helper.py is a helper function that I used for my discard policy. The rest of the files are from assignment 1 of cribbage and I did not modify any of them (except for the correction in Flush Scores). 

In short, the first 13 parameters represent the value of starting a pegging phase with that specific rank. They are imported into a dictionary where the key is the rank and the value is essentially how good that card is for starting. This is an example of such a dictionary: 
startingcardvalues = {1: 1, 2: 1, 3: 1, 4: 1, 5: 0, 6: 3, 7: 3, 8: 4, 9: 4, 10: 2, 11: 2, 12: 2, 13: 2}
As we can see, this dictionary values 5's very lowly, meaning that it is highly unlikely that the agent will ever start with a 5 (the only case where an agent would start with a 5 is when all four cards in their hands are 5's).

When starting the pegging phase, the agent will look at their hand and choose the card with the highest value. If more than two cards have the same value, they will pick one of them at random. If the agent is not starting the pegging phase, this means that agent is putting down another card to the existing sequence. In this case, the agent will iterate through each card in their hand and calculate the score that would be earned for playing that card. However, the score is adjusted based on certain conditions, as specified below. 

Below describes what each element in an encoding represents:
Index 0: Value of starting with an Ace
Index 1: Value of starting with a 2
Index 2: Value of starting with a 3
Index 3: Value of starting with a 4
Index 4: Value of starting with a 5
Index 5: Value of starting with a 6
Index 6: Value of starting with a 7
Index 7: Value of starting with a 8
Index 8: Value of starting with a 9
Index 9: Value of starting with a 10
Index 10: Value of starting with a Jack
Index 11: Value of starting with a Queen
Index 12: Value of starting with a King
Index 13: Adjustment made if the points history + card value < 15
Index 14: Adjustment made if the points history + card value + 10 == 15
Index 15: Adjustment made if the points history + card value + 10 == 31
Index 16: Adjustment made if the points history + card value == 27 and if there is another card in your hand of value 1 or value 2 or value 3 or value 4
Index 17: Adjustment made if the points history + card value == 28 and if there is another card in your hand of value 1 or value 2 or vlaue 3
Index 18: Adjustment made if the points history + card value == 29 and if there is another card in your hand of value 1 or value 2
Index 19: Adjustment made if the points history + card value == 30 and if there is another card in your hand of value 1
Index 20: Adjustment made if the points hisotry + card value == 31 (essetially just placing a bigger emphasize on having a sum of 31)

I am going to use the same discard policy that I used in assigment 1. I iterated over each possible keep/throw combo, and inside that iteration I iterated through each possible turn card and calculated the points that would be earned with that turn card and summed of those points up. I chose the keep/throw combo with the highest sum. Essentially, I picked the keep/throw combo with the highest value. In assignment 1, it took about 80 seconds for my program to run 1000 games. I rewrote discard policy code for this assignment and now it takes about 7.5 seconds to run 1000 games, so this should help my genetic algorithm iterate through all of the generations at a faster pace. 

For my genetic algorithm, there are 20 chromosomes in each generation, and we will iterate through 25 generations. The crossover probability is 80% and the mutation probability is 40%. I initialized the population at random. For my fitness function, I evaluated how well a chromosome played against a greedy agent for 10,000 games. I chose this number because I wanted the variance to be minimized, but I also did not want to run this program on my laptop for a long time. (With the way I have the code set up, it takes about 12 hours to run through my genetic algorithm and my hill climbing algorithm). For parent selection, I used both elitism and roullete. For eltisim, I made sure the next generation of parents will contain the best two chromosomes of this current generation as they are. They did not crossover or were not mutated. For the 18 remaining spots, I used roullete to select from all 20 parents of the current generation. Essentially, I just wanted to make sure that the best performing chromosomes were not lost in crossover or mutation. For crossover, there was a 80% chance is two parents crossover. If the outcome was to crossover, I chose a random weight between 0 - 1, let us call this W. W represented how much impact parent one would have and (1-W) represented how much impact parent two would have. Please see the code for more details. If the outcome was to not crossover, the offspring was just exact copies of the parents. For mutation, if mutation was the outcome, I chose a random index and mutated it by a constant. I used a while loop to repeat this process until we recieved a probability that decided that mutation was not the outcome. 

all_fits is a dictionary where the key is the generation number and the value is a list of fitness evaluations for the chromosomes in that respective generation. all_pop is a dictionary where the key is the generation number and the value is a list of chromosomes for that generation. The index numbers of the kth generation lists in both dictionaries correspond to each other. In other words, in key 0 of the all_fits dictionary, the first value in that list corresponds to the first chromosome in the list of key 0 in the all_pops dictionary. 

At the end of the maximum number of generations, both of these dictionaries are written to csv files so that further analysis can be done if desired. 

In my hill climbing, I randomly generated the initial chromosome. I then generated all of its neighbors and evaluated each one, using the same fitness function from the genetic algorithm. If the maximum fitness value was higher than the fitness of the current chromosome, I updated the current chromosome to be the neighbor with the highest score and repeated this process until none of the neighbhors had a better score than the current chromosome. At the end of this process, this program writes a csv file with the max fitness score from each iteration. 

My performance on assignment one against a greedy agent was about 0.22. With my genetic algorithm, I have been able to generate chromosomes with a fitness score about 0.28 in the last generation, which is higher than my assignment 1 performance. The best chromosome found using the genetic algorithm had a fitness score of 0.2854 and its encoding is: 
[1.4152991466587599, 3.061374683412262, 2.1090475749414446, 3.3355579089036342, 1.5340859065920087, 2.073194506158668, 3.266679729245218, 2.96530792993779, 0.2896387826620216, 3.9769388023990926, 3.1869215396095063, 2.7729094415923203, 2.6236588203521403, 2.956640912706063, 2.5462872777631693, 2.8826268718360066, 2.9814119401938166, 1.830738749756002, 3.7306055677752568, 2.8875040965981142, 2.127343945441646]
On the other hand, the performance of hill climbing depends greatly on the initilized chromosome. Overall, I have not seen hill climibing to be able to go past three iterations. In other words, I have seen that it takes at most three iterations before the program stops. Increase in perforamnce is quite miniscule, although there was one instance of hill climbing that took me by surprise. The programmed randomly initialized paramaters that resulted in a 0.287 performance, which is higher than anything I have seen in the genetic algorithm. Moreover, hill climbing was able to find a neighbor with a 0.294 performance before it was terminated. This shows that although I am able to get pretty good results with my genetic algorithm, there is room for improvement. 

More info here: https://www.youtube.com/watch?v=h_wqpSOJAPg

