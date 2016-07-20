#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
'''
 Igra Black Jack
 Igra se s kartami - en ali več deck-ov (1 deck ima 54 kart)
 igralec igra proti Hiši
 1. Igralec postavi stavo
 2. Igralec in Hiša dobita vsak po dve karti - igralec ima obe odkriti, Hiša le eno
 3. Igralec se odloči, ali bo vzel še eno karto, ali je zadovoljen s tem, kar ima v roki
 4. Če ima igralec v prvem potegu 21  = Black Jack. Black Jack vedno zmaga, razen v primeru, ko ima hiša v prvem
    potegu tudi 21. V tem primeru je 'push', kar pomeni, da se stava vrne igralcu. Nič ne izgubi, niti ne dobi.
 5. Igalec lahko 'hit-a'toliko časa, dokler ne nabere kart za 21 pik. Ali pa se odloči, da je zadovoljen s tem , kar
    ima v roki. Če preseže 21 je izgubil (bust)
 6. Ko je igralec zadovoljen z naborom - stand-a. Delilec takrat pokaže drugo karto. Če ima delilec pik manj kot 17,
    vleče karte toliko časa, dokler ne dobi 21 ali bust-a
 7. Zmaga tisti (igralec ali hiša), ki ima skupno vsoto kart v roki čim bližje oziroma enako 21
 8. Karte vredne toliko kot je številka, dama, pob, kralj so vredni 10, As pa je vreden 1 ali 11 - kar pride bolj prav
    Pazi, nekdo lahko potegne vse ase: pa je to lahko le 4

    #možne poteze igralca:
    #hit - dodeli novo karto
    #stand - ne naredi nič
    #TO DO
    #double down - podvoji stavo, dodeli še eno karto in konča - to do
    #split - če dobiš dve karti, ki imata enako vrednost, ju 'ločiš' - igraš dve roki + na drugo je treba postaviti isto stavo - to do
    #surrender - izgubiš pol stave in končaš igro - to do

 Varovalke:
 1. pravilni vnos stave
 TO DO
 2. pravilni vnos poteze
 3. dovolj kart v kupu - v resnici gre tako: v kup kart, ki je namenjen igri se 'vtakne' označevalna karta. Ko se
    delilec približa tej karti se karte ponovno premešajo.
'''

class Deck(object):

    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'B', 'J', 'K', 'As']
    pack = 4 * cards

    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.cards_in_game = num_decks * Deck.pack

    def deal_a_card(self):

		# dealing = choosing random card form a cards in game
        chosen_card = random.randint(0, len(self.cards_in_game) - 1)
		# info about the card - index and suit
        card = [chosen_card, self.cards_in_game[chosen_card]]
        # remove a chosen card from the deck
        del self.cards_in_game[chosen_card]
        return card[1]

    def reload_shoe(self):
        self.refill_shoe(self, self.num_decks)


class Oseba(object):
    def __init__(self, ime, denar = 100):
        self.ime = ime
        self.denar = denar
        self.roka = Roka()
        self.poteza = Poteza()

    def stanje(self):
        return self.denar

    def stava(self, stavljen_znesek):
        self.denar -= stavljen_znesek

    # Black Jack je * 1.5, ostale zmage so *2
    def zmaga(self, dobitek, denar_v_igri):
        self.denar += dobitek * denar_v_igri
        print('Priigral si: ', dobitek * denar_v_igri)

    def push(self, denar_v_igri):
        self.denar += denar_v_igri

    def izpis_nova_karta(self):
        print('Igralec ima:  \n'
              '  v roki: %s \n'
              '  pike: %s \n'
              '  najboljša opcija = %s pik' %(self.roka.karte_v_roki,
                                              self.roka.prestejPikeKartVRoki(),
                                              self.roka.najboljsaOpcija()))

    #izpis 'hišnih' kart - dokler igralec hit-a, je karta skrita -> prikaz = 'n', ko se karta odkrije je prijaz ='d'
    def izpis_hisa(self, prikaz):
        if prikaz == 'n':
            print('Hiša ima: \n'
                  ' na mizi: %s' %(self.roka.karte_v_roki[0]))
        elif prikaz == 'd':
            print('Hiša ima: \n'
                  '  na mizi: %s \n'
                  '  pike: %s \n'
                  '  najboljša opcija = %s pik' %(self.roka.karte_v_roki,
                                              self.roka.prestejPikeKartVRoki(),
                                              self.roka.najboljsaOpcija()))


class Roka(object):
    def __init__(self):
        self.karte_v_roki = []
        self.stava = 0
        self.deck = Deck()

    def dodaj_karto(self):
        self.karte_v_roki.append(self.deck.dodeliKarto())

    def karte_v_roki(self):
        return self.karte_v_roki

    def prestejPikeKartVRoki(self):
        #možnih različnih rezultatov je število AS-ov + 1 (AS se šteje lahko kot 1 ali 11).
        #1. preštejem AS-e
        #2. preštejem pike brez AS-ov
        #3. naredim seznam z št.AS-ov + 1 elementov, vsak element ima začetno vrednost iz #2.
        #4. naredim seznam možnih rezultatov
        pike = 0
        n = self.karte_v_roki.count('As')

        for karta in self.karte_v_roki:
            if karta in ['B', 'J', 'K']:
                pike += 10
            elif karta == 'As':
                pass
            else:
                pike += karta

        #možnih različnih rezultatov je število AS-ov + 1 (AS se šteje lahko kot 1 ali 11).
        rezultat = [pike] * (n + 1)

        for i in range(len(rezultat)):
            rezultat[i] += n + ((i) * 10)

        return rezultat


    def najboljsaOpcija(self):
    #najboljša opcija je tista, ki je najbližje oz. enaka vsoti 21
        best = 21
        tocka = 0
        for p in self.prestejPikeKartVRoki():
            if p <= 21:
                temp = 21 - p
                if temp < best:
                    best = temp
                    tocka = p
        return tocka

    def BlackJack(self):
        return True if (len(self.karte_v_roki) == 2 and self.najboljsaOpcija() == 21) else False

class Poteza(object):

    def __init__(self):
        self.roka = Roka()

    def izberi_potezo(self):
        return input('Kakšna je tvoja poteza? (h = hit, s = stand):')


# MAIN
#oh! Tole bi bilo treba drugače. Narediti funkcije za posamezne akcije, potem pa v 'mainu' samo klicati akcije.

def main():
    paket = Deck()
    igra = 'd'

    Hisa = Oseba('Hiša', 0)
    igralec1 = Oseba('Maja', 200)

    while igra == 'd':

        while True:
            try:
                znesek_stava = int(input('Postavi stavo. Na razpolago imaš %s.' %(igralec1.stanje())))
            except:
                print('Nekaj ne štima. Si sigurno vnesel številko? Poskusi še enkrat.')
                continue
            else:
                if znesek_stava > igralec1.stanje():
                    print('Ni dovolj denarja za takšno stavo. Imaš %s. ' %(igralec1.vsota))
                    continue
                else:
                    print('Stava sprejeta.')
                    igralec1.stava(znesek_stava)
                    igralec1.stanje()
                    break

        igralec1.roka = Roka()
        Hisa.roka = Roka()


        #razdeli karte
        for i in range(0,4):
            #potegnem karto in jo dodelim igralcu ali Hisi
            if i % 2 == 1:
                igralec1.roka.dodaj_karto()
            else:
                Hisa.roka.dodaj_karto()

        #rokaIgralec1.karte_v_roki = ['As', 'K']
        #Hisa.roka.karte_v_roki = ['As', 6]

        #na vrsti so poteze
        #Najprej preverim, če ima kdo blackJack
        if igralec1.roka.BlackJack() == True:
            if Hisa.roka.BlackJack() == True:
                igralec1.izpis_nova_karta()
                Hisa.izpis_hisa('d')
                print('SKORAAJ!! Ampak je PUSH.')
                igralec1.push(znesek_stava)
            else:
                igralec1.izpis_nova_karta()
                Hisa.izpis_hisa('d')
                print('IJEEE!! Black Jack. Zmagal si')
                igralec1.zmaga(1.5, znesek_stava)
        else:
            igralec1.izpis_nova_karta()
            Hisa.izpis_hisa('n')

            #Za izbiro poteze bi bilo treba narediti še preverjanje pravilnosti izbrane poteze
            while igralec1.poteza.izberi_potezo() == 'h':
                igralec1.roka.dodaj_karto()
                igralec1.izpis_nova_karta()
                Hisa.izpis_hisa('n')

                if igralec1.roka.najboljsaOpcija() == 0:
                    print('Ojoj! Pa je šlo čez! Tvoje točke: %s => BUST! KONEC IGRE' %(igralec1.roka.prestejPikeKartVRoki()))
                    igra = 'konec'
                    break
                    #konec igre
                elif igralec1.roka.najboljsaOpcija() == 21:
                    print('Juhu 21! ... Kaj pa ima hiša? ')
                    break

        Hisa.izpis_hisa('d')

        while Hisa.roka.najboljsaOpcija() < 17 and igra != 'konec' and Hisa.roka.najboljsaOpcija() != 0 and igralec1.roka.BlackJack() == False:
            Hisa.roka.dodaj_karto()

            Hisa.izpis_hisa('d')
            print('igralec najboljsa opcija = ', igralec1.roka.najboljsaOpcija())
            print('hisa najboljsa opcija = ', Hisa.roka.najboljsaOpcija())

        if Hisa.roka.najboljsaOpcija() == 0 and igralec1.roka.najboljsaOpcija() <= 21:
            print('Hiša bust! Bravo, zmagal si!')
            igralec1.zmaga(2, znesek_stava)
        elif 0 < Hisa.roka.najboljsaOpcija() <= 21 and igralec1.roka.najboljsaOpcija() <= 21:
            if igralec1.roka.najboljsaOpcija() < Hisa.roka.najboljsaOpcija():
                print('Ojej! Hiša zmaga. Izgubil si!')
            elif igralec1.roka.najboljsaOpcija() == Hisa.roka.najboljsaOpcija():
                print('SKORAAJ si zmagal!! Ampak je PUSH. Hiša in ti imata enako število pik.')
                igralec1.push(znesek_stava)
            elif igralec1.roka.najboljsaOpcija() > Hisa.roka.najboljsaOpcija():
                print('BRAVO!! ZMAGA!!')
                igralec1.zmaga(2, znesek_stava)
            else:
                print('Kaj se je zgodilo?') #itak se nikoli ne zgodi

        igra = input('Želiš še eno igro?')


if __name__ == '__main__':
    main()
