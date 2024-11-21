import pgzrun
import pygame
import BlackjackGame

# Constants
WIDTH, HEIGHT = 1286, 772
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BUTTON_COLOR_START = (0, 200, 0)
CARD_WIDTH, CARD_HEIGHT = 75, 125

# Chip positions and values
CHIP_POSITIONS = [(60, 200), (60, 280), (60, 360), (60, 440)]
CHIP_VALUES = [25, 50, 100, 500]

# Initialize the game
game = BlackjackGame.BlackjackGame()
game.resetGame()


def on_mouse_down(pos):
    if game.phase == "betting":
        for i, chip_pos in enumerate(CHIP_POSITIONS):
            x, y = chip_pos
            if x <= pos[0] <= x + CARD_WIDTH and y <= pos[1] <= y + CARD_HEIGHT:
                game.player.placeBet(CHIP_VALUES[i])
                break
        if game.startButtonPos[0] <= pos[0] <= game.startButtonPos[0] + BUTTON_WIDTH and \
           game.startButtonPos[1] <= pos[1] <= game.startButtonPos[1] + BUTTON_HEIGHT:
            game.phase = "playing"
            game.dealInitialCards()
    elif game.phase == "playing":
        # Check if "Hit" button is clicked
        if game.hitButtonPos[0] <= pos[0] <= game.hitButtonPos[0] + BUTTON_WIDTH and \
           game.hitButtonPos[1] <= pos[1] <= game.hitButtonPos[1] + BUTTON_HEIGHT:
            game.player.hit()
            if game.player.isBusted():
                game.phase = "results"
        # Check if "Stand" button is clicked
        elif game.standButtonPos[0] <= pos[0] <= game.standButtonPos[0] + BUTTON_WIDTH and \
                game.standButtonPos[1] <= pos[1] <= game.standButtonPos[1] + BUTTON_HEIGHT:
            game.phase = "houseTurn"
            game.houseLogic()


def draw():
    game.draw(screen)


pgzrun.go()
