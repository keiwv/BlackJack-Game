from Player import Player
import os
import pygame
from pygame import Rect

# Constants
WIDTH, HEIGHT = 1286, 772
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_COLOR_START = (0, 200, 0)
BUTTON_COLOR_HIT = (0, 0, 200)
BUTTON_COLOR_STAND = (200, 0, 0)
CARD_WIDTH, CARD_HEIGHT = 75, 125

# Chip positions and values
CHIP_POSITIONS = [(60, 200), (60, 280), (60, 360), (60, 440)]
CHIP_VALUES = [25, 50, 100, 500]


class BlackjackGame:
    def __init__(self):
        self.player = Player("Player", (300, 600))
        self.house = Player("House", (CENTER_X, 100))
        self.images = self.loadImages()
        self.phase = "betting"  # Game phases: betting, playing, houseTurn, results
        self.startButtonPos = (CENTER_X - 75, CENTER_Y +
                               50)  # Button to start game
        self.hitButtonPos = (300, 700)  # Hit button
        self.standButtonPos = (400, 700)  # Stand button

    def loadImages(self):
        images = {}
        for filename in os.listdir("./assets/images/cards"):
            path = os.path.join("./assets/images/cards", filename)
            if os.path.isfile(path):
                images[os.path.splitext(filename)[0]] = pygame.image.load(path)

        # Add chip images
        images["chip25"] = pygame.image.load("ficha25.png")
        images["chip50"] = pygame.image.load("ficha50.png")
        images["chip100"] = pygame.image.load("ficha100.png")
        images["chip500"] = pygame.image.load("ficha500.png")
        return images

    def resetGame(self):
        self.player.reset()
        self.house.reset()
        self.phase = "betting"

    def dealInitialCards(self):
        for _ in range(2):
            self.player.hit()
            self.house.hit()

    def houseLogic(self):
        while sum(self.house.cards) < 17:
            self.house.hit()
        self.phase = "results"

    def draw(self, screen):
        screen.clear()
        screen.blit("blackjack_fondo", (0, 0))

        self.drawPlayerCards(screen, self.player)
        self.drawHouseCards(screen)

        if self.phase == "betting":
            self.drawBettingPhase(screen)
        elif self.phase == "playing":
            self.drawPlayerActions(screen, self.player)
        elif self.phase == "results":
            self.drawResults(screen)

    def drawPlayerCards(self, screen, player):
        for i, card in enumerate(player.cards):
            card_image = self.images.get(f"{card}")
            if card_image:
                card_pos = (player.position[0] + i * 20, player.position[1])
                screen.blit(card_image, card_pos)

    def drawHouseCards(self, screen):
        for i, card in enumerate(self.house.cards):
            card_image = self.images.get(f"{card}")
            if card_image:
                card_pos = (
                    self.house.position[0] + i * 20, self.house.position[1])
                screen.blit(card_image, card_pos)

    def drawBettingPhase(self, screen):
        screen.draw.text("Place your bets!", (CENTER_X - 100,
                         CENTER_Y - 50), fontsize=40, color="yellow")
        for i, chip_pos in enumerate(CHIP_POSITIONS):
            chip_image = self.images.get(f"chip{CHIP_VALUES[i]}")
            if chip_image:
                screen.blit(chip_image, chip_pos)
        screen.draw.text(f"{self.player.name}: ${self.player.money}",
                         (200, HEIGHT - 150), fontsize=30, color="white")
        screen.draw.filled_rect(
            Rect(self.startButtonPos, (BUTTON_WIDTH,
                 BUTTON_HEIGHT)), BUTTON_COLOR_START
        )
        screen.draw.text(
            "Start", (self.startButtonPos[0] + 30, self.startButtonPos[1] + 10), fontsize=30, color="black")

    def drawPlayerActions(self, screen, player):
        screen.draw.filled_rect(
            Rect(self.hitButtonPos, (BUTTON_WIDTH, BUTTON_HEIGHT)), BUTTON_COLOR_HIT
        )
        screen.draw.text(
            "Hit", (self.hitButtonPos[0] + 30, self.hitButtonPos[1] + 10), fontsize=30, color="black")
        screen.draw.filled_rect(
            Rect(self.standButtonPos, (BUTTON_WIDTH,
                 BUTTON_HEIGHT)), BUTTON_COLOR_STAND
        )
        screen.draw.text(
            "Stand", (self.standButtonPos[0] + 25, self.standButtonPos[1] + 10), fontsize=30, color="black")

    def drawResults(self, screen):
        playerSum = sum(self.player.cards)
        houseSum = sum(self.house.cards)
        if self.player.isBusted():
            result = "You Lose!"
        elif self.house.isBusted() or playerSum > houseSum:
            result = "You Win!"
        elif playerSum == houseSum:
            result = "It's a Tie!"
        else:
            result = "You Lose!"
        screen.draw.text(result, (CENTER_X - 50, CENTER_Y - 50),
                         fontsize=40, color="yellow")
