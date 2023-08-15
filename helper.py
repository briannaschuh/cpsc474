from scoring import score
import itertools as it

def expected_value(game, hand, indices, crib, other_rank, other_suit, other_value_count):
    
    #organize cards into keep and throw pile
    keep = []
    throw = []
    for i in range(len(hand)):
        if i in indices:
            throw.append(hand[i])
        else:
            keep.append(hand[i])


    #create dictionaries to keep track of the different cards in your keep pile
    rank_count = {}
    suit_count = {}
    value_count = {}
    for card in keep:
        if card.rank() not in rank_count:
            rank_count[card.rank()] = 1
        else:
            rank_count[card.rank()] += 1
        if card.suit() not in suit_count:
            suit_count[card.suit()] = 1
        else:
            suit_count[card.suit()] += 1
        if game.rank_value(card.rank()) not in value_count:
            value_count[game.rank_value(card.rank())] = 1
        else:
            value_count[game.rank_value(card.rank())] += 1
            
        
    #calculate pairs you can get with all other turn cards    
    pairs = 0
    for card in keep:
        pairs += 2 * other_rank[card.rank()]
    
    #calculate the pairs in your keep pile    
    pairs_in_hand = 0
    for key, value in rank_count.items():
        if value < 2:
            pairs_in_hand += 0
        elif value == 2:
            pairs_in_hand += 2
        elif value == 3:
            pairs_in_hand += 6
        elif value == 4:
            pairs_in_hand += 12
    
    # calculate 15s with all other turn cards    
    fifteens = 0
    fifteens_in_hand = 0 #calculate the 15s that are in your hand
    for k in range(1, 5):
        for cards in it.combinations(keep, k):
            combo_sum = sum(game.rank_value(c.rank()) for c in cards)
            if combo_sum < 15 and combo_sum > 4:
                fifteens += 2*other_value_count[15-combo_sum]
            elif combo_sum == 15:
                fifteens_in_hand += 2
                
                
    #calculate nob            
    nob = 0 
    if 11 in rank_count:
        for card in keep:
            if card.rank() == 11:
                nob += other_suit[card.suit()]
    
    #calculate nob points in your crib            
    nob_crib = 0
    for card in throw:
        if card.rank() == 11:
            nob_crib += other_suit[card.suit()]
    
    #the start of my sequence calculation. It is kind of chaotic and could definitily be improved
    #but I have tested it over 1000 times and compared results with the score function provided by the code and it gets the same results every time.             
    sq_points = 0
    unique = []
    for card in keep:
        if card.rank() not in unique:
            unique.append(card.rank())
    unique.sort() #get a unique sorted list of ranks
    
    #look for sequences in your keep pile
    dif = []
    seq_tracker = 0
    times = 0
    final_index = 0
    for i in range(0, len(unique) - 1):
        d = unique[i+1] - unique[i]
        if d == 1:
            if seq_tracker == 0:
                seq_tracker += 1
            else:
                seq_tracker += 1
                times = max(times, seq_tracker)
                final_index = i + 1
        else:
            seq_tracker = 0
            
    if times != 0:
        seq = unique[final_index-times:final_index+1]
        seq_dict = {i:rank_count[i] for i in seq} #create a dic so we know what appears in the seq

    else: 
        seq = []
        seq_dict = {}
    
    pts = 0
    dup_seq = 1
    if seq != []:
        for i in range(0, len(seq)):
            pts += 1
            dup_seq *= rank_count[seq[i]] #keep track of duplicate cards so we can calculate the points
        
    str_pts = pts*dup_seq #total points
        
    unique_dict = {i:i for i in unique} #random dict. I just wanted it to so I can access the keys faster
    
    #now we will see how many sequences we can get with all other turn cards
    sequence = 0
    for r in game.all_ranks():
        if r in seq_dict:
            con = 1 #if we already have this card in our sequence, count it
            for key in seq_dict:
                if key != r:
                    con *= seq_dict[key]
            sequence += pts*other_rank[r]*con
        else: #else we need to see if adding this card creates a sequence
            temp = unique + [r]
            temp.sort()
            seq_tracker = 0
            times = 0
            final_index = 0
            for i in range(0, len(temp) - 1):
                d = temp[i+1] - temp[i]
                if d == 1:
                    if seq_tracker == 0:
                        seq_tracker += 1
                    else:
                        seq_tracker += 1
                        times = max(times, seq_tracker)
                        final_index = i+1
                else:
                    seq_tracker = 0
            add_pts = 0
            dup_tc = 1
            dup_con = 1
            if times != 0:
                seq_with_tc = temp[final_index-times:final_index+1]
                for i in range(0, len(seq_with_tc)):
                    if seq_with_tc[i] not in unique:
                        dup_tc *= other_rank[seq_with_tc[i]]
                        dup_tc *= dup_seq
                        add_pts += 1
                    elif seq_with_tc[i] not in seq_dict:
                        dup_con *= rank_count[seq_with_tc[i]]
                        add_pts += 1
                    
                add_pts *= dup_con*dup_tc
                sequence += add_pts
            
    #check for flushes in hand and all other potential flushes        
    flush_check = keep[0].suit()
    if suit_count[flush_check] == 4:
        flush_in_hand = 4
        flush = other_suit[flush_check]
    else:
        flush_in_hand = 0
        flush = 0
        
    
    fifteen_crib = 0 #15s in the crib only with other turn cards
    fifteen_crib_gauranteed = 0 #15s in the crib
    lstcombos = [game.rank_value(throw[0].rank()), game.rank_value(throw[1].rank())]
    lstcombos.append(sum(lstcombos))
    for i in lstcombos:
        if i < 15 and i > 4:
            fifteen_crib += 2*other_value_count[15-i]
        elif i == 15:
            fifteen_crib_gauranteed = 2
    
    #see how many pairs you can get in your crib only with the turn cards
    pairs_crib = 0
    for card in throw:
        pairs_crib += 2 * other_rank[card.rank()]
    
    #see how many pairs you can get with your crib    
    pairs_crib_gauranteed = 0
    if throw[0].rank() == throw[1].rank():
        pairs_crib_gauranteed = 2
        
    sequence_crib = 0
    
    #see how many sequences you can get in your crib with the other turn cards
    throw_ranks = [c.rank() for c in throw]
    throw_ranks.sort()
    if throw_ranks[1] - throw_ranks[0] == 1:
        if throw_ranks[0] != 1:
            sequence_crib += 3*other_rank[throw_ranks[0] - 1]
        if throw_ranks[1] != 13:
            sequence_crib += 3*other_rank[throw_ranks[1] + 1]
    elif throw_ranks[1] - throw_ranks[0] == 2:
        mid = (throw_ranks[1] + throw_ranks[0])/2
        sequence_crib += 3*other_rank[mid]
    
        
    return pairs + fifteens + nob + sequence + flush, fifteen_crib + pairs_crib + sequence_crib + nob_crib, str_pts + pairs_in_hand + fifteens_in_hand + flush_in_hand, pairs_crib_gauranteed + fifteen_crib_gauranteed
        
            
        
    