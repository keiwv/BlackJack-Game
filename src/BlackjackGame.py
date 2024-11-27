from Player import Player
import os
import pygame
from pygame import Rect
import random

# Constants
WIDTH, HEIGHT = 1286, 772
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_COLOR_START = (0, 200, 0)
BUTTON_COLOR_HIT = (0, 0, 200)
BUTTON_COLOR_STAND = (200, 0, 0)
CARD_WIDTH, CARD_HEIGHT = 75, 125
PLAYER1_IMAGE_POS = (300, 600)


# Chip positions and values
CHIP_POSITIONS = [(60, 200), (60, 280), (60, 360), (60, 440)]
CHIP_VALUES = [25, 50, 100, 500]


class BlackjackGame:
    def __init__(self):
        self.player = Player("Player 1", (602, 652))
        self.house = Player("House", (CENTER_X, 100))
        self.images = self.loadImages()
        self.phase = "betting"  # Game phases: betting, playing, houseTurn, results
        self.startButtonPos = (CENTER_X - 75, CENTER_Y +
                               50)  # Button to start game
        self.hitButtonPos = (300, 700)  # Hit button
        self.standButtonPos = (400, 700)  # Stand button
        self.reloadButtonPos = (WIDTH - 100, HEIGHT - 100)  # Reload button

    def loadImages(self):
        images = {}
        for filename in os.listdir("./assets/images/cards"):
            path = os.path.join("./assets/images/cards", filename)
            if os.path.isfile(path):
                # Guarda el nombre sin extensión como clave
                key = os.path.splitext(filename)[0]
                images[key] = pygame.image.load(path)

        # Agregar imágenes de fichas
        images["chip25"] = pygame.image.load("ficha25.png")
        images["chip50"] = pygame.image.load("ficha50.png")
        images["chip100"] = pygame.image.load("ficha100.png")
        images["chip500"] = pygame.image.load("ficha500.png")

        # Cargar la imagen del botón de recarga
        images["reload"] = pygame.image.load("./assets/images/reload.png")
        return images

    def resetGame(self):
        self.player.reset()
        self.house.reset()
        self.phase = "betting"
        print("Game reset. Ready for a new round.")  # Depuración


    def dealInitialCards(self):
        if not self.player.cards and not self.house.cards:  # Solo asignar si no hay cartas
            for _ in range(2):
                self.player.hit()
                self.house.hit()
            print(f"Initial cards dealt: Player {self.player.cards}, House {self.house.cards}")  # Depuración
        else:
            print("Cards already dealt, not regenerating.")  # Depuración




    def houseLogic(self):
        if self.phase != "houseTurn":
            print("House logic skipped: Not the house turn.")  # Depuración
            return

        print(f"House starts with cards: {self.house.cards}")  # Depuración

        # Solo permitir que el dealer tome cartas si las actuales son válidas
        while self.house.getCardValuesSum() < 17:
            self.house.hit()
            print(f"House hits: Current cards {self.house.cards}, Sum: {self.house.getCardValuesSum()}")  # Depuración

            if len(self.house.cards) > 5:  # Evitar demasiadas cartas
                print("House stops hitting due to too many cards.")
                break

        self.phase = "results"
        print(f"House logic ends with cards: {self.house.cards}")  # Depuración





    def draw(self, screen):
        screen.clear()
        screen.blit("blackjack_fondo", (0, 0))

        self.drawPlayerCards(screen, self.player)
        self.drawHouseCards(screen)

        if self.phase == "betting":
            self.drawBettingPhase(screen)
        elif self.phase == "playing":
            self.drawPlayerActions(screen, self.player)
        elif self.phase == "houseTurn":
            self.drawHouseCards(screen)
        elif self.phase == "results":
            self.drawResults(screen)

        # Draw reload button
        reload_image = self.images.get("reload")
        if reload_image:
            screen.blit(reload_image, self.reloadButtonPos)


    def drawPlayerCards(self, screen, player, position=(602, 652)):
        if not player.cards:
            print(f"No cards to draw for {player.name}")  # Depuración
            return

        # Usa la posición predeterminada si no se proporciona una
        position = position or player.position
        print(f"Drawing cards for {player.name}: {player.cards} at position {position}")  # Depuración

        for i, card in enumerate(player.cards):
            card_name = self.getCardName(card)
            card_image = self.images.get(card_name)
            if card_image:
                card_image = self.resizeCards(card_image)
                # Ajusta las coordenadas de cada carta
                card_pos = (
                    position[0] + i * 50,
                    position[1] - (i + 3.5) * 45
                )
                screen.blit(card_image, card_pos)
            else:
                print(f"Image not found for card: {card_name}")


    def drawHouseCards(self, screen):
        if not self.house.cards:  # Depuración
            print("No cards to draw for the house")
            return

        for i, card in enumerate(self.house.cards):
            card_name = self.getCardName(card)
            card_image = self.images.get(card_name)
            if card_image:
                card_image = self.resizeCards(card_image)
                card_pos = (470 + i * 80, 135)
                screen.blit(card_image, card_pos)
            else:
                print(f"Image not found for card: {card_name}")

    def drawBettingPhase(self, screen):
        self.drawPlayerInfo(screen, self.player)
        screen.draw.text("Place your bets!", (CENTER_X - 100,
                         CENTER_Y - 50), fontsize=40, color="yellow")
        for i, chip_pos in enumerate(CHIP_POSITIONS):
            chip_image = self.images.get(f"chip{CHIP_VALUES[i]}")
            if chip_image:
                screen.blit(chip_image, chip_pos)
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
        playerSum = self.player.getCardValuesSum()  # Obtener la suma del jugador
        houseSum = self.house.getCardValuesSum()    # Obtener la suma de la casa

        if self.player.isBusted():
            result = "You Lose!"
        elif self.house.isBusted() or playerSum > houseSum:
            result = "You Win!"
        elif playerSum == houseSum:
            result = "It's a Tie!"
        else:
            result = "You Lose!"

        # Mostrar el resultado en pantalla
        screen.draw.text(result, (CENTER_X - 50, CENTER_Y - 50),
                         fontsize=40, color="yellow")

    def drawPlayerInfo(self, screen, player, position = (602, 652), spacing_horizontal = 50):
        """
        Dibuja el texto con el nombre del jugador y su dinero.
        """
        player_name_pos = (position[0], position[1] + 20)  # Texto justo debajo de las cartas
        money_pos = (position[0], position[1] + 50)       # Dinero debajo del nombre

        # Dibuja el nombre del jugador
        screen.draw.text(f"{player.name}", 
                        player_name_pos, 
                        fontsize=30, 
                        color="white")

        # Dibuja el dinero del jugador
        screen.draw.text(f"Money: ${player.money}", 
                        money_pos, 
                        fontsize=25, 
                        color="yellow")



    def getCardName(self, card):
        valores = {1: "As", 11: "Jota", 12: "Reina", 13: "Rey"}
        figuras = ["Corazones", "Diamantes", "Tréboles", "Espadas"]

        valor, figura_id = card
        figura = figuras[figura_id]

        if valor == 11:  # As
            return f"As_de_{figura}"
        elif valor == 10:  # Cartas figuradas: J, Q, K
            # Selecciona el nombre correcto basado en el índice (J: 11, Q: 12, K: 13)
            if card[0] == 10 and figura_id < 3:  # J, Q o K basadas en asignación previa
                nombre_figura = ["Jota", "Reina", "Rey"][figura_id]
                return f"{nombre_figura}_de_{figura}"
            return f"10_de_{figura}"
        else:
            return f"{valor}_de_{figura}"



    def resizeCards(self, card_image):
        return pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
