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
        card = random.choice(range(1, 12))
        self.cards.append(card)
        self.adjustForAces()

    def adjustForAces(self):
        while sum(self.cards) > 21 and 11 in self.cards:
            self.cards[self.cards.index(11)] = 1

    def hasBlackjack(self):
        return sum(self.cards) == 21

    def isBusted(self):
        return sum(self.cards) > 21
