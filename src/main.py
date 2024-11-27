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
        # Validar clic en las fichas
        for i, chip_pos in enumerate(CHIP_POSITIONS):
            x, y = chip_pos
            chip_width = 75  # Ajusta si las fichas tienen un ancho específico
            chip_height = 75  # Ajusta si las fichas tienen un alto específico

            # Depuración: muestra las coordenadas de las áreas activas
            print(f"Checking chip {i+1}: Area=({x}, {y}, {x+chip_width}, {y+chip_height})")

            # Verificar si el clic está dentro de los límites de la ficha actual
            if x <= pos[0] <= x + chip_width and y <= pos[1] <= y + chip_height:
                bet_amount = CHIP_VALUES[i]
                game.player.placeBet(bet_amount)
                print(f"Chip {i+1} selected: Bet {bet_amount}, Player money: {game.player.money}")  # Depuración detallada
                return

        # Si el clic no está en ninguna ficha
        print(f"Click outside of chips at {pos}. No bet placed.")  # Depuración para clics inválidos

    # Validar clic en otros botones
    if game.startButtonPos[0] <= pos[0] <= game.startButtonPos[0] + BUTTON_WIDTH and \
       game.startButtonPos[1] <= pos[1] <= game.startButtonPos[1] + BUTTON_HEIGHT:
        game.phase = "playing"
        game.dealInitialCards()
        print("Game started!")  # Depuración
        return

    if game.reloadButtonPos[0] <= pos[0] <= game.reloadButtonPos[0] + 75 and \
       game.reloadButtonPos[1] <= pos[1] <= game.reloadButtonPos[1] + 75:
        print("Game reset!")  # Depuración
        game.resetGame()

    elif game.phase == "playing":
        # Restringir a botones válidos
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
            print("Player stands!")  # Depuración
            game.phase = "houseTurn"
            game.houseLogic()
            return

        # Ignorar clics fuera de botones válidos
        print("Click ignored: Not on a valid button during 'playing'")


    if game.reloadButtonPos[0] <= pos[0] <= game.reloadButtonPos[0] + 75 and \
       game.reloadButtonPos[1] <= pos[1] <= game.reloadButtonPos[1] + 75:
        print("Game reset!")  # Depuración
        game.resetGame()





def draw():
    game.draw(screen)


pgzrun.go()

#! Ahora falta implementar el pago de las apuestas
