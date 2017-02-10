#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time

'''
Blackjack is a comparing card game between a player and dealer (House), meaning players compete 
against the dealer but not against other players. It is played with one or more decks of 52 cards. 
The objective of the game is to beat the dealer in one of the following ways:
 - Get 21 points on the player's first two cards (called a "blackjack" or "natural"), 
   without a dealer blackjack;
 - Reach a final score higher than the dealer without exceeding 21; 
 - Let the dealer draw additional cards until his or her hand exceeds 21.

The player or players are dealt a two-card hand and add together the value of their cards. 
Face cards (kings, queens, and jacks) are counted as ten points. A player and the dealer 
can count an ace as 1 point or 11 points. All other cards are counted as the numeric value 
shown on the card. After receiving their first two cards, players have the option of 
getting another card (Hit), not choosing another card (Stand), doubleing down (increasing initial bet),
of if conditions aplly - splitting (getting another hand). In a given round, the player or the 
dealer wins by having a score of 21 or by having the higher score that is less than 21. 
Scoring higher than 21 (called "busting" or "going bust") results in a loss. A player may win 
by having any final score equal to or less than 21 if the dealer busts.
'''

class Hand(object):
    # each player can have one or more hands. This class handels ONE hand
    # player is in game until he/she busts, reaches aim of the game, stands, double downs (and gets one card)
    
    def __init__(self):
        self.cards = []
        self.bet_amount = 0
        self.in_game = True
        self.isBlackJack = False
        self.is_double_down = False
        
    def add_card(self, card):
        # add card to a hand

        self.cards.append(card)

    def count_points_in_hand(self):
        # there are more possible outcomes - it depends on how many Aces are in hand
        # 1. count number of aces
        # 2. count points without aces
        # 3. make a list with number of items that equals number of aces. Each item equals
        #    points of a hand without aces
        # 4. make a list with possible outcomes ()
        points = 0

        # count the number od Aces in one's hand
        # the number of Aces sets the number of possible results
        n = [x[0] for x in self.cards].count('A')

        for card in self.cards:
            if card[0] in ['J', 'K', 'Q']:
                points += 10
            elif card[0] == 'A':
                pass
            else:
                points += int(card[0])

        # number of possible outcomes = number of aces + 1 (value of ace is eather 1 or 11).
        result = [points] * (n + 1)

        for i in range(len(result)):
            result[i] += n + ((i) * 10)

        return result

class Player(object):
    # player  has a name, type (P - player, H - house) and a money (cash)
    # player can have one or more hands (if he/she splits a hand can have more hands)      

    def __init__(self, player_type, name, cash):
        self.player_type = player_type
        self.name = name
        self.cash = cash
        self.hands = []
        self.hands.append(Hand())
    
    def split_hand(self, hand_idx):
        # if player goes for a split, another hand appends to the list of hands
        # last card of a split hand goes into newly created hand
        # newly created hand gets a bet that is equal to te bet of a split hand 

        self.hands.append(Hand())    
        split_card = self.hands[hand_idx].cards.pop()
        self.hands[self.h].cards.append(split_card)
        self.hands[self.h].bet_amount = self.hands[0].bet_amount

    def try_bet(self, bet):
        # method for testing if player has enough money to place a bet

        if self.cash - bet < 0:
            print('You don\'t have enough money for that. You have %s available'  %self.cash)
            return False
        else:
            self.gain_loose(bet, -1)
            return True

    def gain_loose(self, bet, factor):
        # method for handeling winning and loosing. If player/house wins some money, the 
        # formula goes: bet times factor. Factor is positive in case of a win, or -1 in case
        # of loosing

        self.cash += bet * factor

    def restart_game(self):
        # method for restarting a game. Player has to have an empty hand

        self.hands = []
        self.hands.append(Hand())

class Classic_cards(object):
    # creating a classic pack of cards

    def __init__(self):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'K', 'Q']
        suits = ['CLUB', 'DIAMOND', 'HEART', 'SPADE']
        self.pack = [[rank, suit] for rank in ranks for suit in suits]

class Deck(object):
    # deck is a one or more packs of cards

    def __init__(self, num_of_packs, cards):
        self.num_of_packs = num_of_packs
        self.deck = self.num_of_packs * cards.pack
        self.number_of_cards = len(self.deck)

    def shuffle(self):
        # method for shuffeling cards
        random.shuffle(self.deck)

    def deal_a_card(self, turn, player):
        # method for dealing cards
        # On initial deal we don't show each individual card that gets delt, we show both cards
        # of a player
        # When player/house hits, or doubles down, wh show what card was given. Output is costumised
        # for player and for house (that's whay the parameter 'player')
        # turn:
        # 0 for initial deal
        # 1 for deals in game
        # Player:
        # P - player
        # H - house

        # method returns a dealt card
        # it also couts how many cards were dealt (for reshufleing purposes)

        a = self.deck.pop(0)
        self.number_of_cards -= 1
        if turn > 0:
            if player == 'P':
                p = 'Your card: '
            else:
                p = 'House gets: '
            print('%s %s\n' % (p, a))
        
        return a

    def insert_a_card(self, card):
        # after each ended game, we return cards back to a shoe

        self.deck.append(card)

class Game(object):
    # Game class controls the flow of the game
    # initially gets data about number of players (name, cash), number of packs of cards to 
    # fill in a shoe.
    # Name of a player must be at least one char long (whitespace is ok, all players can have same name
    # in propper game one shoud take care of this).
    # Player can play with 1 unit of money minimum.
    # Aim of the game can be set (aim_of_the_game). It's set to 21
    # players are listed in a list od players. House is the last player of a list
    # deck gets initialised

    def __init__(self):
        
        self.players = []
        self.aim_of_the_game = 21
        self.mode_of_the_game = True
        self.num_of_players = 0
        self.packs = 1
        self.deck = Deck(self.packs, Classic_cards())
        self.game_number = 1

        print('Welcome to the game of BLACKJACK!\n')

    def game_on(self):
    # method for flow of the game
    # it has reshuflle triger. Shoe gets reshuffled when there was certain amount of 
    # cards dealt (in deck must be at least enough cards that each player can draw 5 cards)
    # After first shuffle, game gets in continious loop. Game goes on until game is over 
    # and is eather chosen that players don't want to play any more or all players lost 
    # all their money
    # after an initial deal, bets are set, players make their moves, house hits until at least 17
    # shoe gets refilled and player status is checked (if there is enough money to continue)

        print('Let\'s play BLACKJACK! \n')
        print('Shuffleing\n')
        self.deck.shuffle()

        # reshuflle trigger
        trigger = (self.num_of_players + 1) * 5


        while self.mode_of_the_game == True: 
            if self.deck.number_of_cards < trigger:
                print('Time to reshuffle!\n')
                self.deck.number_of_cards = len(self.deck.deck)
                self.deck.shuffle()

            self.num_of_players = len(self.players)

            self.call_for_players()
            if self.mode_of_the_game == False: 
                print('Thank you for playing. Good bye!')
                break

            self.bets(0)

            self.initial_deal()

            self.first_show_of_cards()

            self.players_turn()

            self.house_turn()

            self.refill_shoe()

            self.is_player_in_game()

            print('\nGAME OVER!\n')

            self.game_number += 1

            if len(self.players) > 1:
                a = self.check_y_n_answer('Do you want another go? (Y - yes, N - no) \n')
                if a == 'Y':
                    self.mode_of_the_game = True
                    for player in self.players:
                        player.restart_game()
                else:
                    self.mode_of_the_game = False

    def call_for_players(self):

        if self.game_number == 1:
            add_players = True
            self.num_of_players = self.check_number_input('How many players are there eager to play? \n')
            n = self.num_of_players
            self.packs = self.check_number_input('How many packs of cards do you want to use? \n')
            prep = '' # for print out of 'player call'
        else:
            # remove House - will add it after all players are inserted. 
            # House is last player in list
            a = self.check_y_n_answer('Are there any new players: \n')
            if a == 'Y':
                n = self.check_number_input('How many: \n')
                prep = 'new ' # for print out of 'player call'
                add_players = True
                self.players.pop()
            else: # no new players 
                add_players = False
                # if only house is in list of players it's game over
                if len(self.players) == 1:
                    self.mode_of_the_game = False        

        if self.mode_of_the_game is True and add_players is True:
            for i in range(n):
                # 'player call'
                name = input('What is your name, %splayer%s? \n' % (prep, (i + 1)))
                while len(name) < 1:
                    name = ('For name, please input something at least 1 char long:\n')
                
                cash = self.check_number_input('With how much money do you want to play? \n')

                self.players.append(Player('P', name, cash))
          
            # Append player 'HOUSE'
            self.players.append(Player('H', 'HOUSE', 0))  
            self.num_of_players = len(self.players)

    def check_number_input(self, input_text):
       
        while True:
            try:
                a = int(input(input_text))
            except:
                print('There is something wrong. Are you sure you inserted a number? Try again:')
                continue
            else:
                if a <= 0:
                    print('That\'s not valid amount. It has to be greater than 0.')
                    continue
                else:
                    return a
    
    def check_y_n_answer(self, text):
        # testing validity of Y/N answer
        
        a = input(text).upper()
        while a not in ('Y', 'N'):
            a = input('That is not a valid answer. Please choose Y for yes or N for no: ').upper()
        
        return a

    def initial_deal(self):
        # first deal of cards to all players

        for i in range(len(self.players) * 2): 
            self.players[(i) % len(self.players)].hands[0].add_card(self.deck.deal_a_card(0, ''))

            
    def players_turn(self):
     # Time for players to make their decisions
     # first check: did any of players get BlackJack
     # if not, player decides on their move

        for player in self.players:
            self.blackJack(player, 0)
            self.check_players_hand_still_in_game(player, 0)
            if player.player_type == 'P' and player.hands[0].in_game == True:
                print('%s, your turn: \n' % player.name)
                self.show_of_cards_points(player, 0)
                self.choose_move(player, 0)
                print('\n################################################\n')
                time.sleep(3)
    
    def first_show_of_cards(self):
        # for players we show all cards, for house only one    

        print('################################################\n')
        for player in self.players:
            if player.player_type == 'P':
                crds = player.hands[0].cards
            else:
                crds = player.hands[0].cards[1]
            print('Player %s has %s in hand \n' %(player.name, crds))
        print('################################################\n')

    def house_turn(self):
        # house shows hidden card, check if it has Black Jack on first two cards. 
        # if not, hits till 17

        print('HOUSE\'S TURN\n')
        # house is the last player in list of players
        house = self.players[len(self.players) - 1]
        house_hand = house.hands[0]

        self.show_of_cards_points(house, 0)
        # check if is BlackJack
        self.blackJack(house, 0)
        
        if house_hand.isBlackJack is False:
            a = self.best_option(house, 0)
            while a < 17 and a > 0:
                self.hit(house, 0)
                a = self.best_option(house, 0)

        time.sleep(3)

        self.who_wins()

    def bets(self, hand_idx):
        # method for handeling initial bets

        print('Players, place your bets: \n')

        for player in self.players: 
            if player.player_type == 'P':
                while True:
                    try:
                        a = int(input('%s, place your bet. You have %s available: \n' % (player.name, player.cash)))
                    except:
                        print('There is something wrong. Are you sure you inserted a number? Try again:')
                        continue
                    else:
                        if player.try_bet(a) is False:
                            continue
                        else:
                            break
                
            player.hands[hand_idx].bet_amount = a

    def choose_move(self, player, hand_idx):
        # method for handeling available moves of a player
        # player can always hit or stand, until he/she busts, or gets Black Jack
        # in first two dealt cards. If he/she chooses doubledown one hit is taken care of
        # (player does not need to hit)
        # player can split if he/she holds only two cards in hand and they are of the same value

        # each time, only available moves gets printed out and only available moves are alowed to
        # enter

        player_hand = player.hands[hand_idx]

        if len(player_hand.cards) == 2 and player_hand.isBlackJack == True:
            pass
        else: 
            available_moves = ['H - hit \n', 'S - stand \n']
            am = ['H', 'S']
            
            # try to list only available moves 
            if len(player_hand.cards) == 2 and \
                player.cash - player_hand.bet_amount >= 0:
                available_moves.append('D - double down \n')
                am.append('D')
                # condition for split
                if player_hand.cards[0][0] == player_hand.cards[1][0]:
                    available_moves.append('P - split \n')
                    am.append('P')
                

            print('Your available moves are: \n')
            for m in available_moves: 
                print(m)

            move = input('%s, what is your move?: ' % (player.name)).upper()

            while move not in am:
                print('This is not a valid move. Please choose one of the available moves: \n')
                for m in available_moves: 
                    print(m)
                move = input()

            if move == 'H':
                self.hit(player, hand_idx)
            elif move == 'S':
                self.stand()
            elif move == 'P':
                player.split_hand(hand_idx)
                #print('h =', a)
                self.split(player, hand_idx)
            elif move == 'D':
                self.doubledown(player, hand_idx)
        
    def hit(self, player, hand_idx):
        # method for hitting
        # after a dealt card, points and best option is shown
        # check for bust
        # if player is still in the game, he/she gets to choose another move

        player_hand = player.hands[hand_idx]

        player_hand.add_card(self.deck.deal_a_card(1, player.player_type))

        self.show_of_cards_points(player, hand_idx)

        self.check_players_hand_still_in_game(player, hand_idx)
        
        if player.player_type == 'P' and player_hand.in_game is True:
                self.choose_move(player, hand_idx)
            
        
    def split(self, player, hand_idx):
        # if a player splits a hand, split method goes in each hand individualy
        # if deals another card, shows points and best value of a hand, 
        # calls for a choose_move method (that checks for BlackJack and so forth)

        for number, hand in enumerate(player.hands):
            if number >= hand_idx:
                card = player.hands[hand_idx].add_card(self.deck.deal_a_card(1, player.player_type))
                self.show_of_cards_points(player, hand_idx)
                self.choose_move(player, number)
        
    def stand(self):
        # it does not do anything =)
        pass

    def doubledown(self, player, hand_idx):
        # the initial bet is doubled
        # one card is dealt
        # player is not in game any more (can not make any more moves)
        # checking if there is enough money - taken care of in choose_move
        player.try_bet(player.hands[hand_idx].bet_amount)
        player.hands[hand_idx].bet_amount += player.hands[hand_idx].bet_amount
        player.hands[hand_idx].add_card(self.deck.deal_a_card(1, player.player_type))
        player.hands[hand_idx].in_game = False
        self.show_of_cards_points(player, hand_idx)
        
    def best_option(self, player, hand_idx):
        # best option is the one that is closest to aim of the game (21)
        aim = self.aim_of_the_game
        best = 0

        l = player.hands[hand_idx].count_points_in_hand()

        if l.count(aim) > 0:
            return aim
        else:
            for p in l:
                if p < aim and p > best:
                    best = p
            return best

    def show_of_cards_points(self, player, hand_idx):
        # method for printing out hands, points and best options
        
        if player.player_type == 'P':
            title = 'You have'
            possessive = 'Your '
            score_begining = 's'
        else:
            title = 'House has'
            possessive = ''
            score_begining = 'S'

        print('%s %s in hand.' % (title, player.hands[hand_idx].cards))
        print('%s%score is %s, best option is %s \n' \
            % (possessive, score_begining, 
                player.hands[hand_idx].count_points_in_hand(), 
                self.best_option(player,hand_idx)))

    def check_players_hand_still_in_game(self, player, hand_idx):
        # if player exceedes aim of the game, or reaches it, 
        # there are no more moves for him/her. He/she is not in game any more

        a = self.best_option(player, hand_idx)
        if a == 0:
            print('It\'s a bust. Game over.')
            player.hands[hand_idx].in_game = False
        elif  a == self.aim_of_the_game:
            print('You reached %s!' % self.aim_of_the_game)
            player.hands[hand_idx].in_game = False

    def blackJack(self, player, hand_idx):
        # check if Black Jack method:
        # One can get BlackJack if best option on first two cards is
        # aim of the game (21)

        if self.best_option(player, hand_idx) == self.aim_of_the_game:
            print('WOOP WOOP, %s got BLACK JACK! \n' % player.name)
            player.hands[hand_idx].isBlackJack = True
            player.hands[hand_idx].in_game = False


    def who_wins(self):
        # method for figuring out who won and who lost:
        # A player may win by having any final score equal to or less than 21 if the House busts
        # House loses by busting or having a lesser hand than the player who has not busted. 
        # If the Player and House have the same total, it is a "push", and the player does not win 
        # or lose money on that hand. If the Player and House busts, House wins

        print('################################################\n')
        print('WHO WON and WHO LOST \n')
        print('################################################\n')

        # house is the last player in the list of players
        house = self.players[len(self.players) - 1]
        house_hand = house.hands[0]
        house_points = self.best_option(house, 0)

        for player in self.players:
            if player.player_type == 'P':
                for i, hand in enumerate(player.hands):
                    player_hand_points = self.best_option(player, i) 
                    player_hand = player.hands[i]
                    print('-------------------------------------------\n')
                    print(player.name.upper())
                    print('House has %s, you have %s \n' % (house_points, player_hand_points))

                    if player_hand.isBlackJack is True and house_hand.isBlackJack is False:
                        player.gain_loose(player_hand.bet_amount, 2.5)
                        print('He hej! You\'ve got BlackJack! You won %s. Now you have %s' 
                            % (player_hand.bet_amount * 2.5, player.cash))
                        house.gain_loose(player_hand.bet_amount, -1.5) 
                    elif player_hand_points > house_points:
                        player.gain_loose(player_hand.bet_amount, 2)
                        print('Great, you won %s. Now you have %s' 
                            % (player_hand.bet_amount * 2, player.cash))
                        # House cash:
                        house.gain_loose(player_hand.bet_amount, -1)
                    # PUSH - equal points or both blackJack
                    elif (house_hand.isBlackJack is True and player_hand.isBlackJack is True) or \
                        (house_points == player_hand_points and house_points > 0 and house_hand.isBlackJack is False):  
                        player.gain_loose(player_hand.bet_amount, 1)
                        print('It\'s a Push! You didn\'t loose any money! You have ', player.cash)
                    elif (house_points == 0 and player_hand_points == 0) or (house_points > player_hand_points):
                        print('Too bad! You lost. Now you have %s' % (player.cash))
                        house.gain_loose(player_hand.bet_amount, 1)
                    else: 
                        print('O ou, weird situation!')
                    print('-------------------------------------------\n')
                    time.sleep(2)
            else:
                print('\nHouse has: %s cash' % house.cash)

    def refill_shoe(self):
        # after a played game, cards are returned back to a deck (shoe)

        for player in self.players:
            for i, hand in enumerate(player.hands):
                for card in player.hands[i].cards:
                    self.deck.insert_a_card(card)

    def is_player_in_game(self):
        # player is in game if he/she has more than 0 cash
        # if not, player gets deleted from players list

        i = 0
        while True:
            if self.players[i].cash == 0 and self.players[i].player_type == 'P':
                print('Sorry, %s, you lost all your money. You can\'t play anymore.\n' % self.players[i].name)
                self.players.pop(i)
                self.num_of_players = len(self.players) - 1
                i -= 1
            i += 1
            if i > len(self.players) - 1: 
                break

g = Game().game_on()
