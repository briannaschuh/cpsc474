from policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger
import itertools as it
import random
import deck
import cribbage

import helper

class MyPolicy(CribbagePolicy):
    def __init__(self, game, gene):
        self._policy = CompositePolicy(game, GreedyThrower(game), GreedyPegger(game)) #policies for greedy
        self._game = game
        self.starting_constants = {i+1: gene[i] for i in range(0, 13)}
        self.less_than_15 = gene[13]
        self.equal_15_p1 = gene[14]
        self.equal_31_p1 = gene[15]
        self.equal_27 = gene[16]
        self.equal_28 = gene[17]
        self.equal_29 = gene[18]
        self.equal_30 = gene[19]
        self.equal_31 = gene[20]
        

    def keep(self, hand, scores, am_dealer):             
        crib = 1 if am_dealer else -1
        throw_indices = self._game.throw_indices()
        full_deck = self._game.deck()._cards
        
        rank_count = {rank: 0 for rank in self._game.all_ranks()}
        suit_count = {suit: 0 for suit in self._game.all_suits()}
        value_count = {value: 0 for value in self._game.all_values()}
        
        for card in full_deck:
            rank_count[card.rank()] += 1
            suit_count[card.suit()] += 1
            value_count[self._game.rank_value(card.rank())] += 1
        
        for card in hand:
            rank_count[card.rank()] -= 1
            suit_count[card.suit()] -= 1
            value_count[self._game.rank_value(card.rank())] -= 1

        
        ev = {} #empty dictionary that will have the throwaways as the key and the value as the score of the hand
        
        if scores[0] >= 115 and (scores[0] - scores[1] < 6 and scores[0] - scores[1] > -6):
            if am_dealer == False:
                return self._policy.keep(hand, scores, am_dealer) 
    
    
        
        for i in throw_indices: #iterate through each possible combo
            ex_hand, ev_crib, hand_points, crib_points = helper.expected_value(self._game, hand, i, crib, rank_count, suit_count, value_count)
            expectation = ex_hand + crib*ev_crib + 46*hand_points + crib*crib_points*46
            
            
            
            ev[i] = expectation #add it to the dictionary
        
        highestev = max(ev, key=ev.get) #select the hand with the highest point

        keep = []
        throw = []   
        for i in range(len(hand)):
            if i in highestev:
                throw.append(hand[i]) 
            else:
                keep.append(hand[i])
    
        return keep, throw
        


    def peg(self, cards, history, scores, am_dealer):
        #startingcardvalues = {1: 1, 2: 1, 3: 1, 4: 1, 5: 0, 6: 3, 7: 3, 8: 4, 9: 4, 10: 2, 11: 2, 12: 2, 13: 2}
        bestcard = None
        random.shuffle(cards)        
        startingvalue = -1
        if history.is_start_round():
            for card in cards:
                temp = self.starting_constants[card.rank()]
                if temp > startingvalue:
                    startingvalue = temp
                    bestcard = card
            return bestcard
        
        dealer = 0 if am_dealer else 1
        
        if not history.has_legal_play(self._game, cards, dealer):
            return None
            
        if scores[0] >= 115 and (scores[0] - scores[1] < 6 and scores[0] - scores[1] > -6):
            return self._policy.peg(cards, history, scores, am_dealer)
        
        
        bestscore = None
        
        tiecards = []
        
  
        for card in cards:
            score = history.score(self._game, card, dealer)
            lranks = [self._game.rank_value(c.rank()) for c in cards if c != card]

            if score is not None:
                if history._total + self._game.rank_value(card.rank()) < 15:
                    score -= self.less_than_15
                if history._total + self._game.rank_value(card.rank()) + 10 == 15:
                    score -= self.equal_15_p1
                if history._total + self._game.rank_value(card.rank()) + 10 == 31:
                    score -= self.equal_31_p1
                if history._total + self._game.rank_value(card.rank()) < 27:
                    score = score
                elif history._total + self._game.rank_value(card.rank()) == 27 and (1 in lranks or 2 in lranks or 3 in lranks or 4 in lranks):
                    score = score + self.equal_27
                elif history._total + self._game.rank_value(card.rank()) == 28 and (1 in lranks or 2 in lranks or 3 in lranks):
                    score = score + self.equal_28
                elif history._total + self._game.rank_value(card.rank()) == 29 and (1 in lranks or 2 in lranks):
                    score = score + self.equal_29
                elif history._total + self._game.rank_value(card.rank()) == 30 and (1 in lranks):
                    score = score + self.equal_30
                elif history._total + self._game.rank_value(card.rank()) == 31:
                    score = score + self.equal_31
            if score is not None and (bestscore is None or score >= bestscore):
                if score == bestscore:
                    tiecards.append(card)
                else:
                    tiecards = []
                    tiecards.append(card)    
                    bestscore = score
                    bestcard = card
        if len(tiecards) > 1:
            mini = 0
            for i in tiecards:
                if i.rank() > mini:
                    bestcard = i
                    mini = i.rank()
                    
        return bestcard
            



