import random

class Hand(object):
    
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

        # number of possible outcomes = number of aces + 1 (value of ace is eathen 1 or 11).
        result = [points] * (n + 1)

        for i in range(len(result)):
            result[i] += n + ((i) * 10)

        return result

class Player(object):

    def __init__(self, player_type, name, cash = 10):
        #player 
        self.player_type = player_type
        self.name = name
        self.cash = cash
        self.hands = []
        self.hands.append(Hand())
    
    def split_hand(self, hand_idx):
        # if player goes for a split, 
        self.hands.append(Hand())    
        split_card = self.hands[hand_idx].cards.pop()
        self.hands[self.h].cards.append(split_card)
        self.hands[self.h].bet_amount = self.hands[0].bet_amount

    def try_bet(self, bet):
        if self.cash - bet < 0:
            print('You don\'t have enough money for that. You have %s available'  %self.cash)
            return False
        else:
            self.gain_loose(bet, -1)
            return True

    def gain_loose(self, bet, factor):
        self.cash += bet * factor

    def restart_game(self):
        self.hands = []
        self.hands.append(Hand())

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
        self.number_of_cards = len(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_a_card(self, turn, player):
        # turn:
        # 0 for initial deal
        # 1 for deals in game
        # Player:
        # P - player
        # H - house
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
        self.deck.append(card)

class Game(object):

    def __init__(self):
        
        print('Welcome to the game of BLACKJACK!\n')
        self.num_of_players = int(input('How many players are there eager to play: ?\n'))
        packs = int(input('How many packs of cards do you want to use?: \n'))
        
        self.players = []
        self.aim_of_the_game = 21
        self.mode_of_the_game = True

        '''
        self.num_of_players = 2
        packs = 1
        
        '''
        for i in range(self.num_of_players):

            name = input('What is your name, player%s?\n' % (i + 1)) 
            while len(name) < 1:
                name = ('For name, please input something at least 1 char long:\n')
            
            while True:
                try:
                    cash = int(input('With how much money do you want to play?'))
                except:
                    print('There is something wrong. Are you sure you inserted a number? Try again:')
                    continue
                else:
                    if cash <= 0:
                        print('That\'s not valid amount. It has to be greater than 0.')
                        continue
                    else:
                        break

            self.players.append(Player('P', name, cash))
          
        # Append player 'HOUSE'
        self.players.append(Player('H', 'HOUSE', 0))  

        print('Število igralcev: %s' %(len(self.players)))     
        
        '''
        self.players.append(Player('P', 'Maja', 200))
        self.players.append(Player('P', 'Aleš', 200))
        '''

        self.deck = Deck(packs, Classic_cards())

    def game_on(self):

         # reshuflle trigger

        print('Let\'s play BLACKJACK! \n')
        print('Shuffleing\n')
        self.deck.shuffle()

        trigger = (self.num_of_players + 1) * 5

        while self.mode_of_the_game == True: 
            if self.deck.number_of_cards < trigger:
                print('Time to reshuffle!\n')
                self.deck.number_of_cards = len(self.deck.deck)
                self.deck.shuffle()

            self.bets(0)

            self.initial_deal()

            self.first_show_of_cards()

            self.players_turn()

            self.house_turn()

            self.refill_shoe()

            self.is_player_in_game()

            print('\nGAME OVER!\n')

            if len(self.players) > 1:
                a = input('Do you want another go? (Y - yes, N - no) \n').upper()
                if a not in ['Y', 'N']:
                    input('That is not a valid input. Please choose Y for yes or N for no. \n')
                elif a == 'Y':
                    self.mode_of_the_game = True
                    for player in self.players:
                        player.restart_game()
                else:
                    self.mode_of_the_game = False
            else:
                self.mode_of_the_game = False


    def initial_deal(self):

        # first deal of cards to all players

        for i in range(len(self.players) * 2): 
            print('%s-ta karta' % i)
            self.players[(i) % len(self.players)].hands[0].add_card(self.deck.deal_a_card(0, ''))

            
    def players_turn(self):

        for player in self.players:
            self.blackJack(player, 0)
            self.check_players_hand_still_in_game(player, 0)
            # Time for players to make their decisions
            if player.player_type == 'P' and player.hands[0].in_game == False:
                print('%s, your turn: \n' % player.name)
                self.show_of_cards_points(player, 0)
                self.choose_move(player, 0)
                print('################################################\n')
    
    def first_show_of_cards(self):

        print('################################################\n')
        for player in self.players:
            # for players we show all cards, for house only one
            if player.player_type == 'P':
                crds = player.hands[0].cards
            else:
                crds = player.hands[0].cards[1]
            print('Player %s has %s in hand \n' %(player.name, crds))
        print('################################################\n')

    def house_turn(self):
        # house shows hidden card and hits till 17
        print('HOUSE\'S TURN\n')
        print(self.players[self.num_of_players].name)
        self.show_of_cards_points(self.players[self.num_of_players], 0)
        # check if is BlackJack
        self.blackJack(self.players[self.num_of_players], 0)
        
        if self.players[self.num_of_players].hands[0].isBlackJack is False:
            a = self.best_option(self.players[self.num_of_players], 0)
            while a < 17 and a > 0:
                self.hit(self.players[self.num_of_players], 0)
                a = self.best_option(self.players[self.num_of_players], 0)

        self.who_wins()

    def bets(self, hand_idx):
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

        if len(player.hands[hand_idx].cards) == 2 and player.hands[hand_idx].isBlackJack == True:
            pass
        else: 
            available_moves = ['H - hit \n', 'S - stand \n']
            am = ['H', 'S']
            
            # try to list only available moves 
            if len(player.hands[hand_idx].cards) == 2 and \
                player.cash - player.hands[hand_idx].bet_amount > 0:
                available_moves.append('D - double down \n')
                am.append('D')
                # condition for split
                if player.hands[hand_idx].cards[0][0] == player.hands[hand_idx].cards[1][0]:
                    available_moves.append('P - split \n')
                    am.append('P')
                

            print('Your available moves are: \n')
            for m in available_moves: 
                print(m)

            move = input('%s, what is your move?:' %(player.name)).upper()

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

        player.hands[hand_idx].add_card(self.deck.deal_a_card(1, player.player_type))

        self.show_of_cards_points(player, hand_idx)

        self.check_players_hand_still_in_game(player, hand_idx)
        
        if player.player_type == 'P' and player.hands[hand_idx].in_game is True:
                self.choose_move(player, hand_idx)
            
        
    def split(self, player, hand_idx):

        for number, hand in enumerate(player.hands):
            if number >= hand_idx:
                card = player.hands[hand_idx].add_card(self.deck.deal_a_card(1, player.player_type))
                self.show_of_cards_points(player, hand_idx)
                self.choose_move(player, number)
        
    def stand(self):
        pass

    def doubledown(self, player, hand_idx):
        # checking if there is enough money - took care of in choose_move
        player.try_bet(player.hands[hand_idx].bet_amount)
        player.hands[hand_idx].bet_amount += player.hands[hand_idx].bet_amount
        player.hands[hand_idx].add_card(self.deck.deal_a_card(1, player.player_type))
        player.hands[hand_idx].in_game = False
        self.show_of_cards_points(player, hand_idx)
        
    def best_option(self, player, hand_idx):
        # najboljša opcija je tista, ki je najbližje oz. enaka vsoti 21 (oziroma ciljni vsoti)
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
        # if player exceedes aim of the game, or reaches it, there are no more moves for him/her

        a = self.best_option(player, hand_idx)
        if a == 0:
            print('It\'s a bust. Game over.')
            player.hands[hand_idx].in_game = False
        elif  a == self.aim_of_the_game:
            print('You reached %s!' % self.aim_of_the_game)
            player.hands[hand_idx].in_game = False

    def blackJack(self, player, hand_idx):
        if self.best_option(player, hand_idx) == self.aim_of_the_game:
            print('WOOP WOOP, %s got BLACK JACK! \n' % player.name)
            player.hands[hand_idx].isBlackJack = True
            player.hands[hand_idx].in_game = False


    def who_wins(self):
        print('################################################\n')
        print('WHO WON and WHO LOST \n')
        print('################################################\n')
        # 

        house_points = self.best_option(self.players[self.num_of_players], 0)

        for player in self.players:
            if player.player_type == 'P':
                for i, hand in enumerate(player.hands):
                    player_hand_points = self.best_option(player, i) 
                    print('-------------------------------------------\n')
                    print(player.name.upper())
                    print('House has %s, you have %s \n' % (house_points, player_hand_points))

                    if player_hand_points > house_points:
                        player.gain_loose(player.hands[i].bet_amount, 2)
                        print('Great, you won %s. Now you have %s' % (player.hands[i].bet_amount * 2, player.cash))
                        # House cash:
                        self.players[self.num_of_players].gain_loose(player.hands[i].bet_amount, -1)
                    elif (player_hand_points == house_points and house_points != 0 and player.hands[i].isBlackJack is False) or \
                        player.hands[i].isBlackJack is True and self.players[self.num_of_players].isBlackJack is True: #PUSH
                        player.gain_loose(player.hands[i].bet_amount, 1)
                        print('It\'s a Push! You didn\'t loose any money! You have ', player.cash)
                    elif player.hands[i].isBlackJack == True and player[self.num_of_players].hands[0].isBlackJack == False:
                        print('He hej! You\'ve got BlackJack! you won %s. Now you have %s' % (player.hands[i].bet_amount * 2.5, player.cash))
                        player.gain_loose(player.hands[i].bet_amount, 2.5)
                        self.players[self.num_of_players].gain_loose(player.hands[i].bet_amount, -1.5)
                    elif (player_hand_points < house_points) or (player_hand_points == 0 and house_points == 0):
                        print('Too bad! You lost. Now you have %s' % (player.cash))
                        self.players[self.num_of_players].gain_loose(player.hands[i].bet_amount, 1)
                    elif player_hand_points > self.aim_of_the_game:
                        print('Sorry, you lost! Now you have %s' % (player.cash))
                        self.players[self.num_of_players].gain_loose(player.hands[i].bet_amount, 1)

        print('\nHouse has: ', self.players[self.num_of_players].cash)


    def refill_shoe(self):
        for player in self.players:
            for i, hand in enumerate(player.hands):
                for card in player.hands[i].cards:
                    self.deck.insert_a_card(card)

    def is_player_in_game(self):
        for i, player in enumerate(self.players):
            if player.cash == 0 and player.player_type == 'P':
                print('Sorry, %s, you lost all your money. You can\'t play anymore.' % player.name)
                self.players.pop(i)
                self.num_of_players = len(self.players) - 1



g = Game().game_on()
