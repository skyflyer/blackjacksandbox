import random

class Hand(object):
    
    def __init__(self):
        self.cards = []
#To je stvar igre   
#self.bet_amount = input('Place your bet: ')
        print('Narjen')
        
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
    
    def split_hand(self):
        self.hands.append(Hand())    
        self.h += 1
        split_card = self.hands[(self.h)-1].cards.pop()
        self.hands[self.h].cards.append(split_card)
        
        #Pazi BET!
        
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
        self.players.append(Player('H', 'HOUSE', 0))
        
        self.deck = Deck(packs, Classic_cards())


    def initial_deal(self):
        print('Let\'s play BLACKJACK! \n')
        print('Shuffeling')
        self.deck.shuffle()
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
            
    def choose_move(self, player, hand):


            
        move = input('%s, what is your move?: (H - hit, S - stand, P - split, D - doubledown)' %player.name)
        if move == 'H':
            self.hit(player, hand)
        elif move == 'S':
            self.stand()
        elif move == 'P':
            player.split_hand()
            self.split(player)
        elif move == 'DD':
            self.doubledown()

    def hit(self, player, hand):
        print(len(player.hands))
        player.hands[hand].add_card(self.deck.deal_a_card())
        print(player.hands[hand].cards)
        
        self.choose_move(player, hand)
        
    def split(self, player):
        h = 0
        print('Smo v splitu, h = ', h)

        for hand in player.hands:
            print('%s, you have %s in hand. h = %s' %(player.name, hand.cards, h))
            self.choose_move(player, h)
            h += 1
        
    def stand(self):
        pass

g = Game()
g.initial_deal()
