#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 14:36:59 2022

@author: arjunbhat
"""

import cards
from operator import itemgetter
        
def get_names():
    num = int(input('How many players(Max 8): '))
    while num>8:
        print('8 players max')
        num = int(input('How many players(Max 8): '))
    players_list = []
    for i in range(1,num+1):
        temp_inp = 'Player {:d} Name (Max 10 characters): '.format(i)
        name=input(temp_inp)
        while len(name)>10:
            print('Name over 10 characters.')
            name=input(temp_inp)
        players_list.append(name)
    return players_list
    
def players(players):
    deck = cards.Deck()
    deck.shuffle()
    num_players = len(players)
    hands=[]
    for i in range(num_players):
        hands.append([players[i],deck.deal()])
    for i in range(num_players):
        hands[i].append(deck.deal())
    return hands,deck
def get_flop(deck):
    deck.deal()
    return (deck.deal(),deck.deal(),deck.deal()),deck
def get_turn(deck):
    deck.deal()
    return deck.deal(),deck
def get_river(deck):
    deck.deal()
    return deck.deal(),deck
def get_hand_rank(hand,flop,turn,river):
    hand_list = []
    hand_list.extend([hand[1],hand[2],flop[0],flop[1],flop[2],turn,river])
    rank_list = [card.rank() for card in hand_list]
    suit_list = [card.suit() for card in hand_list]
    count_list = []
    for i in range(1,5):
        count_list.append((suit_list.count(i),i))
    rank_list.sort(reverse=True),count_list.sort(reverse=True)
    ace_list = rank_list
    if 1 in ace_list:
        ace_list.insert(0,14)
    straight_list = list(set(ace_list))
    straight_list.sort(reverse=True)
    straight_count = 0
    full_straight_list = []
    for i in range(0,len(straight_list)-1):
        if straight_list[i]-1 == straight_list[i+1]:
            if straight_count==0:
                top_straight = straight_list[i]
            straight_count+=1
            if straight_list[i+1] not in full_straight_list:
                full_straight_list.extend([straight_list[i],straight_list[i+1]])
        elif straight_list[i]-1 != straight_list[i+1]and straight_count <4:
            straight_count = 0
            full_straight_list = []
    pair_list = []
    for i in range(1,14):
        if i ==1:
            pair_list.append((rank_list.count(i),14))
        else:
            pair_list.append((rank_list.count(i),i))
    pair_list.sort(reverse=True)
    flush_list = [card.rank() for card in hand_list if card.suit()==count_list[0][1]]
    flush_list = [14 if card ==1 else card for card in flush_list]
    flush_list.sort(reverse=True)
    five_flush_list = flush_list[:5]
    kick_rank_list = rank_list
    if 14 in kick_rank_list:
        kick_rank_list.remove(14)
    kick_rank_list = [14 if card ==1 else card for card in kick_rank_list]
    trips_kick = [card for card in kick_rank_list if card != pair_list[0][1]]
    trips_kick.sort(reverse=True)
    trips_kick = trips_kick[:2]
    two_pair_kick = [card for card in kick_rank_list if card != pair_list[0][1] and card!=pair_list[1][1]]
    two_pair_kick.sort(reverse=True)
    two_pair_kick = two_pair_kick[0]
    pair_kick = [card for card in kick_rank_list if card != pair_list[0][1]]
    pair_kick.sort(reverse=True)
    pair_kick = pair_kick[:3]
    high_kick = [card for card in kick_rank_list]
    high_kick.sort(reverse=True)
    high_kick = high_kick[:5]
    quad_kick = [card for card in kick_rank_list if card!= pair_list[0][1]]
    quad_kick.sort(reverse=True)
    quad_kick=quad_kick[0]
    straight_set = set(full_straight_list)
    flush_set = set(flush_list)
    if five_flush_list == [14,13,12,11,10]:
        return ('Royal Flush',1,None)
    #straight flush
    if len(flush_set)>=5 and flush_set < straight_set:
        return ('Straight Flush',2,(top_straight))
    #quads
    if pair_list[0][0]==4:
        return ('Quads',3,(pair_list[0][1],quad_kick))
    #full house
    if pair_list[0][0]==3 and pair_list[1][0]==2 or pair_list[1][0]==3:
        return ('Full House',4,(pair_list[0][1],pair_list[1][1]))
    #flush
    if count_list[0][0]>=5:
        return ('Flush',5,five_flush_list)
    #straight
    if straight_count>=4:
        return ('Straight',6,(top_straight))
    #trips
    if pair_list[0][0]==3:
        return ('Three of a Kind',7,(pair_list[0][1],trips_kick))
    #2 pair
    if pair_list[0][0]==2 and pair_list[1][0]==2:
        return ('Two Pair',8,(pair_list[0][1],pair_list[1][1],two_pair_kick))
    #pair
    if pair_list[0][0]==2:
        return ('Pair',9,(pair_list[0][1],pair_kick))
    #high card
    else:
        return ('High Card',10,(high_kick))
def winning_hand(hands_list):
    hands_list.sort(key=itemgetter(3))
    max_hand = hands_list[0][3]
    high_hands = []
    for hand in hands_list:
        if hand[3] == max_hand:
            high_hands.append(hand[0:3])

    return high_hands
def display(players_list,flop=['[ ]','[ ]','[ ]'],turn='[ ]',river='[ ]'):
    player1,player2,player3,player4,player5,player6,player7,player8 = ['EMPTY SEAT','[] ',' []'],['EMPTY SEAT','[] ',' []'], ['EMPTY SEAT','[] ',' []'], ['EMPTY SEAT','[] ',' []'], ['EMPTY SEAT','[] ',' []'],['EMPTY SEAT','[] ',' []'], ['EMPTY SEAT','[] ',' []'],['EMPTY SEAT','[] ',' []']
    player_list = [player1,player2,player3,player4,player5,player6,player7,player8 ]
    for i in range(0,len(players_list)):
        for n in range(0,3):
            player_list[i][n] = players_list[i][n]
   
    print('-'*95,'\n')
    print(' '*10,'~'*84,' '*10)
    print(' '*10,'~'*16,'{:^10}'.format(player_list[0][0]),'~'*8,'{:^10}'.format(player_list[1][0]),'~'*8,'{:^10}'.format(player_list[2][0]),'~'*16)
    print(' '*10,'~'*15,'-',player_list[0][1],player_list[0][2],'-','~'*8,'-',player_list[1][1],player_list[1][2],'-','~'*7,'-',player_list[2][1],player_list[2][2],'-','~'*15)
    print(' '*10,'~'*84,' '*10)
    print(' '*10,'~'*25,' '*32,'~'*25,' '*10)
    print(' '*10,'~'*5,'{:^10}'.format(player_list[3][0]),'~'*8,' '*32,'~'*8,'{:^10}'.format(player_list[4][0]),'~'*5,' '*10)
    print(' '*10,'~'*5,'-',player_list[3][1],player_list[3][2],'-','~'*7,' '*1,'-',flop[0],flop[1],flop[2],'-',turn,'-',river,'-',' '*2,'~'*7,'-',player_list[4][1],player_list[4][2],'-','~'*5,' '*10)
    print(' '*10,'~'*25,' '*32,'~'*25,' '*10)
    print(' '*10,'~'*84,' '*10)
    print(' '*10,'~'*16,'{:^10}'.format(player_list[5][0]),'~'*8,'{:^10}'.format(player_list[6][0]),'~'*8,'{:^10}'.format(player_list[7][0]),'~'*16)
    print(' '*10,'~'*15,'-',player_list[5][1],player_list[5][2],'-','~'*8,'-',player_list[6][1],player_list[6][2],'-','~'*7,'-',player_list[7][1],player_list[7][2],'-','~'*15)
    print(' '*10,'~'*84,' '*10,'\n')
    
def winner(winners):
    hand =winners[0][1] 
    
    winners_list = []
    if hand =='Royal Flush':
        winners_list = winners
    elif hand == 'Straight Flush':
        winners.sort(key=itemgetter(2),reverse=True)
        max_straight = winners[0][2]
        for winner in winners:
            if winner[2] == max_straight:
                winners_list.append(winner)
    elif hand == 'Quads':
        win_l = []
        winners.sort(key=itemgetter(2),reverse=True)
        max_quads = winners[0][2][0]
        for winner in winners:
            if winner[2][0]==max_quads:
                win_l.append(winner)
        quad_kick = 0
        for win in win_l:
            if win[2][1] > quad_kick:
                quad_kick = win[2][1]
        for win in win_l:
            if win[2][1] == quad_kick:
                winners_list.append(win)
    elif hand == 'Full House':
        win_l = []
        winners.sort(key=itemgetter(2),reverse=True)
        max_full = winners[0][2][0]
        for winner in winners:
            if winner[2][0]==max_full:
                win_l.append(winner)
        full_kick = 0
        for win in win_l:
            if win[2][1] > full_kick:
                full_kick = win[2][1]
        for win in win_l:
            if win[2][1] == full_kick:
                winners_list.append(win)
    elif hand == 'Flush':
        winners.sort(key=itemgetter(2),reverse=True)
        max_flush = winners[0][2]
        for winner in winners:
            if winner[2] == max_flush:
                winners_list.append(winner)
    elif hand == 'Straight':
        winners.sort(key=itemgetter(2),reverse=True)
        max_straight = winners[0][2]
        for winner in winners:
            if winner[2]==max_straight:
                winners_list.append(winner)
    elif hand == 'Three of a Kind':
        win_l = []
        winners.sort(key=itemgetter(2),reverse=True)
        max_trips = winners[0][2][0]
        for winner in winners:
            if winner[2][0] == max_trips:
                win_l.append(winner)
        trips_kick = [0,0]
        for win in win_l:
            if win[2][1] > trips_kick:
                trips_kick=win[2][1]
        for win in win_l:
            if win[2][1] == trips_kick:
                winners_list.append(win)
    elif hand == 'Two Pair':
        win_l = []
        winny_l = []
        winners.sort(key=itemgetter(2),reverse=True)
        max_twop = winners[0][2][0]
        for winner in winners:
            if winner[2][0] == max_twop:
                win_l.append(winner)
        twop_ = 0
        for win in win_l:
            if win[2][1] > twop_:
                twop_=win[2][1]
        for win in win_l:
            if win[2][1] == twop_:
                winny_l.append(win)
        twop_kick = 0
        for win in winny_l:
            if win[2][2] > twop_kick:
                twop_kick=win[2][2]
        for win in winny_l:
            if win[2][2] == twop_kick:
                winners_list.append(win)
    elif hand == 'Pair':
        win_l = []
        winners.sort(key=itemgetter(2),reverse=True)
        max_pair = winners[0][2][0]
        for winner in winners:
            if winner[2][0] == max_pair:
                win_l.append(winner)
        pair_kick = [0,0,0]
        for win in win_l:
            if win[2][1] > pair_kick:
                pair_kick = win[2][1]
        for win in win_l:
            if win[2][1]==pair_kick:
                winners_list.append(win)
    elif hand == 'High Card':
        winners.sort(key=itemgetter(2),reverse=True)
        max_high = winners[0][2]
        for winner in winners:
            if winner[2]==max_high:
                winners_list.append(winner)
    else:
        return 'ERROR'
    return winners_list
def convert_num(hands_list):
    D = {14:'Ace',13:'King',12:'Queen',11:'Jack',10:'Ten',9:'Nine',8:'Eight',7:'Seven',6:'Six',5:'Five',4:'Four',3:'Three',2:'Two'}
    hands = []
    for hand in hands_list:
        if hand[1] == 'Royal Flush':
            hands.append(hand[0],'Royal Flush')
        elif hand[1] == 'Straight Flush':
            hands.append((hand[0],'{} high straight flush'.format(D[hand[2]])))
        elif hand[1] == 'Quads':
            hands.append((hand[0],"Quad {}s with {} kicker".format(D[hand[2][0]],D[hand[2][1]])))
        elif hand[1] == 'Full House':
            hands.append((hand[0],"{}s full of {}s".format(D[hand[2][0]],D[hand[2][1]])))
        elif hand[1] == 'Flush':
            hands.append((hand[0],"{} high flush".format(D[hand[2][0]])))
        elif hand[1] == 'Straight':
            hands.append((hand[0],'{} high straight'.format(D[hand[2]])))
        elif hand[1] == 'Three of a Kind':
            hands.append((hand[0],"Trip {}s with {}, {} kickers".format(D[hand[2][0]],D[hand[2][1][0]],D[hand[2][1][1]])))
        elif hand[1] == 'Two Pair':
            hands.append((hand[0],"{}, {} two pair with {} kicker".format(D[hand[2][0]],D[hand[2][1]],D[hand[2][2]])))
        elif hand[1] == 'Pair':
            hands.append((hand[0],"Pair of {}s with {}, {}, {} kickers".format(D[hand[2][0]],D[hand[2][1][0]],D[hand[2][1][1]],D[hand[2][1][2]])))
        elif hand[1] == 'High Card':
            hands.append((hand[0],"{} high with {}, {}, {}, {} kickers".format(D[hand[2][0]],D[hand[2][1]],D[hand[2][2]],D[hand[2][3]],D[hand[2][4]])))
    return hands
def display_hands(final_hands):
    print('-'*95,'\n')
    for hand in final_hands:
        print(' '*10,'-'*84)
        print(' '*10,'| ','{:10}'.format(hand[0]),' | ','{:63}'.format(hand[1]),' |')
    print(' '*10,'-'*84,'\n')
def display_winning_hands(final_hands):
    print(' '*31,'~'*42)
    print(' '*31,'|','{:^38}'.format('WINNING HANDS'),'|')
    for hand in final_hands:
        print(' '*10,'-'*84)
        print(' '*10,'| ','{:10}'.format(hand[0]),' | ','{:63}'.format(hand[1]),' |')
    print(' '*10,'-'*84)
    
def main():   
    players_list = get_names()    
    answer = None
    while answer != 'q':
        hands,deck= players(players_list)
        display(hands)
        see_flop = input('Press any button to see flop: ')
        if see_flop != '8========================D':
            flop,deck = get_flop(deck)
            display(hands,flop)
            see_turn = input('Press any button to see turn: ')
            if see_turn != '8========================D':
                turn,deck = get_turn(deck)
                display(hands,flop,turn)
                see_river = input('Press any button to see river: ')
                if see_river != '8========================D':
                    river,deck = get_river(deck)
                    display(hands,flop,turn,river)
                    winning_hands=[]
                    for hand in hands:
                        hand_list = get_hand_rank(hand,flop,turn,river)
                        winning_hands.append((hand[0],hand_list[0],hand_list[2],hand_list[1]))
                    final_hands = convert_num(winning_hands)
                    winners = winning_hand(winning_hands)
                    final_winner = winner(winners)
                    final = convert_num(final_winner)
                    see_hands = input('Press any button to view hands: ')
                    if see_hands != '8========================D':
                        display_hands(final_hands)
                        display_winning_hands(final)
        
        
        
        answer = input('Another game? q to quit: ').lower()

if __name__ == '__main__':
     main()
