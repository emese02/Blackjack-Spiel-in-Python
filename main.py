import random
import datetime

class Deck:
    def __init__(self, liste_von_karten = []):
        self.liste_von_karten = liste_von_karten

    def naechste_karte(self):
        karte = self.liste_von_karten[-1]
        self.liste_von_karten.pop()
        return karte

    def mischen(self):
        random.shuffle(self.liste_von_karten)

    def initialisieren(self):
        file = open("karten.txt","r")

        for i in range(4):
            line = file.readline()
            bild, rang1, rang2, anzug = line.rstrip().split(',')
            bild = chr(int(bild))
            rang1 = int(rang1)
            rang2 = int(rang2)
            karte = AceCard(bild, rang1, rang2, anzug)
            self.liste_von_karten.append(karte)

        for i in range(12):
            line = file.readline()
            bild, rang1, rang2, anzug = line.rstrip().split(',')
            bild = chr(int(bild))
            rang1 = int(rang1)
            rang2 = int(rang2)
            karte = FaceCard(bild, rang1, rang2, anzug)
            self.liste_von_karten.append(karte)

        line = file.readline()
        while line != '':
            bild, rang1, rang2, anzug = line.rstrip().split(',')
            bild = chr(int(bild))
            rang1 = int(rang1)
            rang2 = int(rang2)
            karte = Karte(bild, rang1, rang2, anzug)
            self.liste_von_karten.append(karte)
            line = file.readline()
        file.close()
        self.mischen()

    def karten_anzeigen(self):
        for karte in self.liste_von_karten:
            print(karte, "  ", type(karte))

class Karte:
    def __init__(self, bild, rang1, rang2, anzug): #rang1 bedeutet harten Wert, rang2 bedeutet weichen wert
        self.bild = bild
        self.rang1 = rang1
        self.rang2 = rang2
        self.anzug = anzug

    def __repr__(self):
        return f'Bild: {self.bild}, Anzug: {self.anzug}, Wert: {self.rang1}'

class FaceCard(Karte):
    def __init__(self, bild, rang1, rang2, anzug):
        super().__init__(bild, rang1, rang2, anzug)
        self.rang1 = self.rang2 = 10

class AceCard(FaceCard):
    def __init__(self, bild, rang1, rang2, anzug):
        super().__init__(bild, rang1, rang2, anzug)
        self.rang1 = 11
        self.rang2 = 1

    def __repr__(self):
        return super().__repr__() + f' oder {self.rang2}'

class Scores:
    def anhaengen(self, spieler):
        file = open("spielen.txt", "r")
        gespielte_runde = len(file.readlines()) + 1
        file.close()
        file = open("spielen.txt","a")
        file.write(f'{datetime.date.today()}, {gespielte_runde}. Rund, Geldbetrag: {spieler.geldbetrag}, Name: {spieler.name}\n')
        file.close()

    def anhaengen_final_score(self, spieler):
        file = open("final_score.txt", "r")
        gespielte_partitur = len(file.readlines()) + 1
        file.close()
        file = open("final_score.txt", "a")
        file.write(
            f'{datetime.date.today()}, {gespielte_partitur}. Partitur, Geldbetrag: {spieler.geldbetrag}, Name: {spieler.name}\n')
        file.close()

    def auslesen(self, betrag):
        file = open("final_score.txt", "r")
        scores = []
        for line in file:
            wert = line.split(':')[1].strip()
            wert = int(wert.split(',')[0])
            scores.append(wert)
        scores.sort(reverse = True)
        print("Highscore-Tafel: ")
        for nr, score in enumerate(scores):
            if score == betrag:
                print(f'* {nr + 1}. {score} *')
            else:
                print(f'{nr + 1}. {score}')
        file.close()

class Nutzer:
    def __init__(self, name, geldbetrag=100):
        self.name = name
        self.geldbetrag = geldbetrag

    def __repr__(self):
        return f'Name: {self.name}, Geldbetrag: {self.geldbetrag}€'

class Dealer:
    def __init__(self, deck):
        self.deck = deck

    def naechste_karte_bekommen(self):
        return self.deck.naechste_karte()

    def neues_deck_erhalten(self, neues_deck):
        self.deck = neues_deck

class Spiel:
    def __init__(self, dealer, spieler):
        self.dealer = dealer
        self.spieler = spieler

def test_mischen():
    liste = [Karte('127141','5','5','five_of_spades'),Karte('127143','7','7','seven_of_spades'),Karte('127173','5','5','five_of_diamonds'),Karte('127189','5','5','five_of_clubs')]
    deck1 = Deck(liste)
    deck1.mischen()
    veraendert = False
    for nr, karte in enumerate(deck1.liste_von_karten):
        if karte != liste[nr]:
            veraendert = True
    return veraendert

def test_naechste_karte_bekommen():
    liste = [Karte('127141', '5', '5', 'five_of_spades'), Karte('127143', '7', '7', 'seven_of_spades'),
             Karte('127173', '5', '5', 'five_of_diamonds'), Karte('127189', '5', '5', 'five_of_clubs')]
    deck1 = Deck(liste)
    dealer = Dealer(deck1)
    initial_len = len(deck1.liste_von_karten)
    dealer.naechste_karte_bekommen()
    set_von_karten = set (deck1.liste_von_karten)
    assert len(deck1.liste_von_karten) == initial_len - 1 and len(deck1.liste_von_karten) == len(set_von_karten)

def test_weiche_harte_werte():
    karte1 = Karte('127173', '5', '5', 'five_of_diamonds')
    karte2 = AceCard ('127169','11','1','ace_of_diamonds')
    karte3 = FaceCard ('127147','10','10','jack_of_spades')
    assert karte1.rang1 == karte1.rang2 and karte2.rang1 == 11 and karte2.rang2 == 1 and karte3.rang1 == karte3.rang2 == 10

def main():
    deck_fuer_spieler = Deck()
    deck_fuer_spieler.initialisieren()
    deck_fuer_dealer = Deck()
    deck_fuer_dealer.initialisieren()
    dealer = Dealer(deck_fuer_spieler)
    test_mischen()
    test_weiche_harte_werte()
    name = input("Name: ")
    spieler = Nutzer(name)
    spiel = Spiel(dealer, spieler)
    rund = 1
    while rund != 6:
        if spieler.geldbetrag == 0:
            print("Dein Geldbetrag ist kaputt.")
            Scores.anhaengen_final_score(Scores, spieler)
            break
        print("Rund nr. ", rund)
        value = int(input(f'Achtung! Du hast nur {spieler.geldbetrag}€. Wie viel Geld möchtest du abgeben?: '))
        if value > spieler.geldbetrag:
            raise ValueError("Dein Geldbetrag ist nicht genug für ein neues Rund.")
        karte = dealer.naechste_karte_bekommen()
        test_naechste_karte_bekommen()
        print(karte)
        if isinstance(karte, AceCard):
            kartenwert = input(f'Welches Wert möchtest du verwenden: weichen oder harten Wert: w oder h? ({karte.rang2}/{karte.rang1}): ')
            if kartenwert.lower() == 'w':
                summe = karte.rang2
            elif kartenwert.lower() == 'h':
                summe = karte.rang1
        else:
            summe = karte.rang1
        option = None
        rund += 1
        while option != 'nein':
            option = input("Möchtest du eine neue Karte bekommen? (Antworte mit ja oder nein): ")
            if option == 'ja':
                karte = dealer.naechste_karte_bekommen()
                print(karte)
                if isinstance(karte,AceCard):
                    kartenwert = input(f'Welches Wert möchtest du verwenden: weichen oder harten Wert: w oder h? ({karte.rang2}/{karte.rang1}): ')
                    if kartenwert.lower() == 'w':
                        summe += karte.rang2
                    elif kartenwert.lower() == 'h':
                        summe += karte.rang1
                    else:
                        raise ValueError("Dieses Wert gibt es nicht.")
                else:
                    summe += karte.rang1
            if summe == 21:
                spieler.geldbetrag += value
                print(f'Du bist der Gewinner! Du hast {spieler.geldbetrag}€.')
                Scores.anhaengen(Scores, spieler)
                break
            if summe > 21:
                spieler.geldbetrag -= value
                print(f'Game over, 21 ist überschritten. Du hast {spieler.geldbetrag}€.')
                Scores.anhaengen(Scores, spieler)
                break

        if summe >= 21:
            continue

        print("Dealer: ")
        dealer.deck = deck_fuer_dealer
        dealer.deck.mischen()
        karte = dealer.naechste_karte_bekommen()
        print(karte)
        summe_dealer = karte.rang1
        if isinstance(karte, AceCard):
            print(f'{karte.rang1} gewählt')
        while summe_dealer < summe and summe_dealer < 21:
            karte = dealer.naechste_karte_bekommen()
            print(karte)
            if isinstance(karte, AceCard):
                if 11 + summe_dealer <= 21:
                    summe_dealer += karte.rang1
                    print(f'{karte.rang1} gewählt')
                else:
                    summe_dealer += karte.rang2
                    print(f'{karte.rang2} gewählt')
            else:
                summe_dealer += karte.rang1

        if summe_dealer == summe:
            print(f'Das Geldbetrag ist unverändert: {spieler.geldbetrag}€.')
        elif summe > summe_dealer and summe < 21 or summe_dealer > 21:
            spieler.geldbetrag += value
            print(f'Du bist der Gewinner! Du hast {spieler.geldbetrag}€.')
        else:
            spieler.geldbetrag -= value
            print(f'Du hast {value}€ verloren. Du hast {spieler.geldbetrag}€.')
        Scores.anhaengen(Scores, spieler)
        dealer.deck = deck_fuer_spieler
        dealer.deck.mischen()

    if spieler.geldbetrag != 0:
        Scores.anhaengen_final_score(Scores, spieler)
    Scores.auslesen(Scores, spieler.geldbetrag)
main()