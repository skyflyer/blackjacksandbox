import random

class Hand(object):
    
    def __init__(self):
        self.cards = []
        self.bet_amount = 0
        print('Hand narjen')
        
    def add_card(self, card):
        self.cards.append(card)

class Player(object):

    def __init__(self, player_type, name, cash = 10):
        self.player_type = player_type
        self.name = name
        self.cash = cash
        self.hands = []
        self.hands.append(Hand())
        self.h = 0
        print('klas Player: h = %s, player = %s' %(self.h, self.name))
    
    def split_hand(self, hand_idx):

        self.hands.append(Hand())    
        self.h += 1
        split_card = self.hands[hand_idx].cards.pop()
        self.hands[self.h].cards.append(split_card)
        self.hands[self.h].bet_amount = self.hands[0].bet_amount

        print('metoda player.split_hand h = %s' %self.h)

    def try_bet(self, bet):
        if self.cash - bet < 0:
            print('You don\'t have enough money for that. You have %s available'  %self.cash)
            return False
        else:
            self.cash -= bet
            return True


        
class Classic_cards(object):

    def __init__(self):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'K', 'Q']
        suits = ['CLUB', 'DIAMOND', 'HEART', 'SPADE']
        self.pack = [[rank, suit] for rank in ranks for suit in suits]

    def package(self):
        print(self.pack)

    def print_card(self, card):
        print(card)

    def get_card(self, i):
        print(self.pack(i))
        
class Deck(object):

    def __init__(self, num_of_packs, cards):
        self.cards = cards
        self.num_of_packs = num_of_packs
        self.deck = self.num_of_packs * cards.pack
        self.card = Classic_cards()

    def print_cards(self):
        print(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def num_of_cards(self):
        print(len(self.deck))

    def deal_a_card(self):
        return self.deck.pop(0)

class Game(object):

    def __init__(self):
        
        '''
        num_of_players = int(input('how many players are there eager to play: ?\n'))
        packs = int(input('How many packs of cards do you want to use?: \n'))
        '''
        self.players = []
        
        num_of_players = 2
        packs = 2
        
        '''
        for i in range(num_of_players):
            name = input('What is your name, player%s?\n' %(i+1)) #what if blank?
            cash = input('With how much money do you want to play?') #what if blank
            self.players.append(Player('P', name, cash))
        '''   
        #Append player 'HOUSE'
        self.players.append(Player('P', 'Maja', 200))
        self.players.append(Player('P', 'Aleš', 200))        
        
        self.deck = Deck(packs, Classic_cards())


    def initial_deal(self):
        print('Let\'s play BLACKJACK! \n')
        print('Shuffeling')
        self.deck.shuffle()

        self.bets(0)

        self.players.append(Player('H', 'HOUSE', 0))

        for i in range(len(self.players) * 2): 
            self.players[(i) % len(self.players)].hands[0].add_card(self.deck.deal_a_card())
            
        for player in self.players:
            # for players we show all cards, for house only one
            if player.player_type == 'P':
                crds = player.hands[0].cards
            else:
                crds = player.hands[0].cards[1]
            print('Player %s has %s in hand \n' %(player.name, crds))
            
        for player in self.players:
            # Time for players to make their decisions
            if player.player_type == 'P':
                print('%s, you have %s in hand. \n' %(player.name, player.hands[0].cards))
                self.choose_move(player, 0)

    def bets(self, hand_idx):
        print('Players, place your bets: \n')

        for player in self.players: 
            a = int(input('%s, place your bet: ' %player.name))
            while player.try_bet(a) is False:
                a = int(input('Try again. Lower thy bet!'))
            
            player.hands[hand_idx].bet_amount = a
            player.cash -= a

    def choose_move(self, player, hand_idx):

        available_moves = ['H - hit \n', 'S - stand \n']
        
        # try to list only available moves 
        if len(player.hands[hand_idx].cards) == 2 and \
            player.hands[hand_idx].cards[0][0] == player.hands[hand_idx].cards[1][0] and \
            player.cash - player.hands[hand_idx].bet_amount > 0:
            available_moves.append('P - split \n')

        if player.cash > 0:
            available_moves.append('D - double down \n')

        print('%s, your available moves are: \n' %player.name)
        for m in available_moves: 
            print(m)

        move = input('%s, what is your move?:' %(player.name))

        if move == 'H':
            self.hit(player, hand_idx)
        elif move == 'S':
            self.stand()
        elif move == 'P':
            player.split_hand(hand_idx)
            #print('h =', a)
            self.split(player, hand_idx)
        elif move == 'DD':
            self.doubledown()

        
    def hit(self, player, hand_idx):
        print('metoda hit: Player %s ima %s handov. Tole je %s -i hand' %(player.name, len(player.hands), hand_idx))
        player.hands[hand_idx].add_card(self.deck.deal_a_card())
        print(player.hands[hand_idx].cards)
        
        self.choose_move(player, hand_idx)
        
    def split(self, player, hand_idx):

        # add conditions when split is possible:
        # only two cards
        # same value
        # enough money
        print('Smo v splitu, hand_idx = ', hand_idx)

        for number, hand in enumerate(player.hands):
            if number >= hand_idx:
                print('metoda split: num = %s, cards = %s' %(number,hand.cards))
                print('metoda split: %s, you have %s in hand. h = %s, bet = %s' %(player.name, hand.cards, number, player.hands[hand_idx].bet_amount))
                self.choose_move(player, number)
        
    def stand(self):
        pass

g = Game()
g.initial_deal()
