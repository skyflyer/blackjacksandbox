import random

class Hand(object):
    # hand is in game until in_game equals 1
    
    def __init__(self):
        self.cards = []
        self.bet_amount = 0
        self.in_game = 1
        self.isBlackJack = False
        print('Hand narjen')
        
    def add_card(self, card):
        self.cards.append(card)
        print('Dodali karto')
        print('You have: %s' %self.count_points_in_hand())

    def count_points_in_hand(self):
        # možnih različnih rezultatov je število AS-ov + 1 (AS se šteje lahko kot 1 ali 11).
        # 1. preštejem AS-e
        # 2. preštejem pike brez AS-ov
        # 3. naredim seznam z št.AS-ov + 1 elementov, vsak element ima začetno vrednost iz #2.
        # 4. naredim seznam možnih rezultatov
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

        # možnih različnih rezultatov je število AS-ov + 1 (AS se šteje lahko kot 1 ali 11).
        result = [points] * (n + 1)

        for i in range(len(result)):
            result[i] += n + ((i) * 10)

        return result

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
            self.gain_loose(bet, -1)
            return True

    def gain_loose(self, bet, factor):
        self.cash += bet * factor


        
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
        self.num_of_players = int(input('how many players are there eager to play: ?\n'))
        packs = int(input('How many packs of cards do you want to use?: \n'))
        '''
        self.players = []
        
        self.num_of_players = 2
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
        # Check for BlackJack   

        for player in self.players:
            # Time for players to make their decisions
            if player.player_type == 'P':
                print('%s (%s), you have %s in hand. \n' %(player.name, player.player_type, player.hands[0].cards))
                self.choose_move(player, 0)

        self.house_turn()

    def house_turn(self):
        # house shows hidden card and hits till 17
        print('House has %s in hand.' %self.players[self.num_of_players].hands[0].cards)
        # check if is BlackJack
        self.blackJack(self.players[self.num_of_players], 0)
        house_BlackJack = self.players[self.num_of_players].hands[0].isBlackJack
        print('House BJ = ', house_BlackJack)
        print('Is house: ', self.players[self.num_of_players].name )
        if house_BlackJack is False:
            a = self.best_option(self.players[self.num_of_players], 0)
            print('House best option = ' , a)
            while a < 17 and a > 0:
                self.hit(self.players[self.num_of_players], 0)
                a = self.best_option(self.players[self.num_of_players], 0)
                print('While a = ', a)
            print('House turn: ', self.players[self.num_of_players].hands[0].cards)

        self.who_wins()

    def bets(self, hand_idx):
        print('Players, place your bets: \n')

        for player in self.players: 
            a = int(input('%s, place your bet. You have %s available: ' % (player.name, player.cash)))
            while player.try_bet(a) is False:
                a = int(input('Try again. Lower thy bet!'))
            
            player.hands[hand_idx].bet_amount = a

    def choose_move(self, player, hand_idx):

        if len(player.hands[hand_idx].cards) == 2 and self.blackJack(player, hand_idx) == True:
            pass
        else: 
            available_moves = ['H - hit \n', 'S - stand \n']
            
            # try to list only available moves 
            if len(player.hands[hand_idx].cards) == 2 and \
                player.hands[hand_idx].cards[0][0] == player.hands[hand_idx].cards[1][0] and \
                player.cash - player.hands[hand_idx].bet_amount > 0:
                available_moves.append('P - split \n')

            if player.cash > 0:
                available_moves.append('D - double down \n')

            print('%s, you have %s points. Your best option is %s. Your available moves are: \n' \
                %(player.name, player.hands[hand_idx].count_points_in_hand(), self.best_option(player, hand_idx)))
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

        # after every hit, check if player is still below 21
        if player.player_type == 'P':
            if self.check_player_still_in_game(self.best_option(player, hand_idx))  != -1:
                self.choose_move(player, hand_idx)
            else:
                print('Too bad. You busted. You have %s left' %player.cash)
                player.hands[hand_idx].in_game = 0
        
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

    def best_option(self, player, hand_idx):
        # najboljša opcija je tista, ki je najbližje oz. enaka vsoti 21
        best = 21
        point = 0
        for p in player.hands[hand_idx].count_points_in_hand():
            if p <= 21:
                temp = 21 - p
                if temp < best:
                    best = temp
                    point = p
        return point

    def check_player_still_in_game(self, point):
        if point == 0:
            print('BUST')
            return -1


    def blackJack(self, player, hand_idx):
        if self.best_option(player, hand_idx) == 21:
            player.hands[hand_idx].isBlackJack = True


    def who_wins(self):
        # if house busts, everybody still in game wins
        house_points = self.best_option(self.players[self.num_of_players], 0) 
        print('Who wins - house points: ', self.best_option(self.players[self.num_of_players], 0) )
        if house_points > 21:
            house_points = 0

        for player in self.players:
            if player.player_type == 'P':
                for i, hand in enumerate(player.hands):
                    player_hand_points = self.best_option(player, i) 
                    print(player.name)
                    if player.hands[i].in_game == 1:
                        if player_hand_points > house_points:
                            player.gain_loose(player.hands[i].bet_amount, 2)
                            print('Great, you won %s. Now you have %s' % (player.hands[i].bet_amount * 2, player.cash))
                        elif player_hand_points == house_points: #PUSH
                            player.gain_loose(player.hands[i].bet_amount, 1)
                            print('It\'s a Push! You didn\'t loose any money! You have ', player.cash)
                        elif player.hands[i].isBlackJack == True and player[self.num_of_players - 1].hands[0].isBlackJack == False:
                            print('He hej! You\'ve got BlackJack! you won %s. Now you have %s' % (player.hands[i].bet_amount * 2.5, player.cash))
                            player.gain_loose(player.hands[i].bet_amount, 2.5)
                        elif player_hand_points < house_points:
                            print('Too bad! You lost. Now you have %s' % (player.cash))
                    else:
                        print('Sorry, you lost! Now you have %s' % (player.cash))
# BLACKJACK

g = Game()
g.initial_deal()
