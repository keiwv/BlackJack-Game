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

    def hit(self):
        # Valor aleatorio para la carta
        # 1 a 13 para As, 2-10, Jota, Reina, Rey
        value = random.choice(range(1, 14))
        # 0 a 3 para Corazones, Diamantes, Tréboles y Picas
        suit = random.choice(range(4))

        # Asignar valores a las cartas
        if value == 1:  # As
            value = 11  # Inicialmente, el As vale 11
        elif value > 10:  # Figuras (Jota, Reina, Rey)
            value = 10

        self.cards.append((value, suit))  # Añadir la carta como una tupla
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
        return sum(self.cards) == 21

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
