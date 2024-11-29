import random


class Player:
    def __init__(self, name, pos):
        self.name = name
        self.cards = []
        self.money = 1000
        self.lastBet = 0
        self.position = pos

    def reset(self):
        self.cards.clear()
        self.lastBet = 0

    def placeBet(self, amount):
        if self.money >= amount:
            self.money -= amount
            self.lastBet += amount
        else:
            print("Insufficient funds for this bet.")  


    def hit(self):
        value = random.choice(range(1, 14))  # Valores de 1 a 13
        suit = random.choice(range(4))      # Figuras: 0, 1, 2, 3

        # Asignar valor numerico correcto
        if value == 1:  # As
            card = (11, suit)  # Representa el As inicialmente como 11
        elif value > 10:  # J, Q, K
            card = (10, suit)  # Representa las figuras con valor 10
        else:
            card = (value, suit)

        self.cards.append(card)
        self.adjustForAces()


    def adjustForAces(self):
        # Extrae solo los valores de las cartas
        valores = [card[0] for card in self.cards]

        # Ajusta el valor de los Ases (11 -> 1) si el total supera 21
        while sum(valores) > 21 and 11 in valores:
            valores[valores.index(11)] = 1

        # Actualiza los valores en las cartas originales
        for i, card in enumerate(self.cards):
            if card[0] == 11 and sum(valores) <= 21:
                break
            if card[0] == 11 and valores.count(11) < sum(1 for v in valores if v == 11):
                self.cards[i] = (1, card[1])  # Cambia el valor del As


    def hasBlackjack(self):
        return self.getCardValuesSum() == 21 and len(self.cards) == 2


    def isBusted(self):
        return self.getCardValuesSum() > 21

    def getCardValuesSum(self):
        return sum(card[0] for card in self.cards)

    def adjustForAces(self):
        # Extrae los valores actuales de las cartas
        valores = [card[0] for card in self.cards]

        # Ajustar los As de 11 a 1 si el total supera 21
        while sum(valores) > 21 and 11 in valores:
            valores[valores.index(11)] = 1

        # Actualizar los valores en las cartas originales
        for i, card in enumerate(self.cards):
            if card[0] == 11 and sum(valores) <= 21:
                break
            if card[0] == 11 and valores.count(11) < sum(1 for v in valores if v == 11):
                self.cards[i] = (1, card[1])  # Cambia el valor del As a 1
