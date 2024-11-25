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
    print(f"Mouse clicked at {pos} during phase: {game.phase}")  # Depuración

    if game.phase == "betting":
        for i, chip_pos in enumerate(CHIP_POSITIONS):
            x, y = chip_pos
            if x <= pos[0] <= x + CARD_WIDTH and y <= pos[1] <= y + CARD_HEIGHT:
                game.player.placeBet(CHIP_VALUES[i])
                print(f"Bet placed: {CHIP_VALUES[i]}")  # Depuración
                return
        if game.startButtonPos[0] <= pos[0] <= game.startButtonPos[0] + BUTTON_WIDTH and \
           game.startButtonPos[1] <= pos[1] <= game.startButtonPos[1] + BUTTON_HEIGHT:
            game.phase = "playing"
            game.dealInitialCards()
            print("Game started!")  # Depuración
            return

    elif game.phase == "playing":
        if game.hitButtonPos[0] <= pos[0] <= game.hitButtonPos[0] + BUTTON_WIDTH and \
        game.hitButtonPos[1] <= pos[1] <= game.hitButtonPos[1] + BUTTON_HEIGHT:
            if not game.player.isBusted():
                game.player.hit()
                print(f"Player hits! Current cards: {game.player.cards}")  # Depuración
                if game.player.isBusted():
                    print("Player busted!")  # Depuración
                    game.phase = "results"
            return

        elif game.standButtonPos[0] <= pos[0] <= game.standButtonPos[0] + BUTTON_WIDTH and \
            game.standButtonPos[1] <= pos[1] <= game.standButtonPos[1] + BUTTON_HEIGHT:
            if game.phase == "playing":
                print("Player stands!")  # Depuración
                game.phase = "houseTurn"
                game.houseLogic()  # Aquí solo se agrega lógica, no reinicia cartas
            return



    if game.reloadButtonPos[0] <= pos[0] <= game.reloadButtonPos[0] + 75 and \
       game.reloadButtonPos[1] <= pos[1] <= game.reloadButtonPos[1] + 75:
        print("Game reset!")  # Depuración
        game.resetGame()




def draw():
    game.draw(screen)


pgzrun.go()

#! Cuando presiono stand o hit me cambia las cartas
