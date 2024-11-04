class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.cards = []
        self.nameCards = []
        # 1 = Playing, 0 = Player or House lose, 3 = House wins with 21 or in the first play, 4 = Player-House wins, 5 = end turn, 6 = insurance, 7 = bet time, 8 = waiting, 9 = no money
        self.gameStatePlayer = 8
        self.money = 1000
        self.bet = 0
        self.insurance = 0
