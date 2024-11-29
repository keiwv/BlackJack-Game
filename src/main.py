import pgzrun
import pygame
import BlackjackGame

# Constantes
WIDTH, HEIGHT = 1286, 772
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50

# Valores y posiciones de las fichas
CHIP_POSITIONS = [(60, 200), (60, 280), (60, 360), (60, 440)]
CHIP_VALUES = [25, 50, 100, 500]

# Inicializar el juego
game = BlackjackGame.BlackjackGame()
game.resetGame()

def on_mouse_down(pos):
    if game.phase == "betting":
        # Validar clic en las fichas
        for i, chip_pos in enumerate(CHIP_POSITIONS):
            x, y = chip_pos
            chip_width = 75  
            chip_height = 75  

            # Verificar si el clic esta dentro de los limites de la ficha actual
            if x <= pos[0] <= x + chip_width and y <= pos[1] <= y + chip_height:
                bet_amount = CHIP_VALUES[i]
                game.player.placeBet(bet_amount)
                return


    # Validar clic en boton de inicio
    if game.startButtonPos[0] <= pos[0] <= game.startButtonPos[0] + BUTTON_WIDTH and \
       game.startButtonPos[1] <= pos[1] <= game.startButtonPos[1] + BUTTON_HEIGHT:
        game.phase = "playing"
        game.dealInitialCards()
        return

    # Validar clic en boton de reinicio
    if game.reloadButtonPos[0] <= pos[0] <= game.reloadButtonPos[0] + 75 and \
       game.reloadButtonPos[1] <= pos[1] <= game.reloadButtonPos[1] + 75:
        game.resetGame()

    # Validar clic en botones de juego
    elif game.phase == "playing":
        # Restringir a botones válidos
        if game.hitButtonPos[0] <= pos[0] <= game.hitButtonPos[0] + BUTTON_WIDTH and \
        game.hitButtonPos[1] <= pos[1] <= game.hitButtonPos[1] + BUTTON_HEIGHT:
            if not game.player.isBusted():
                game.player.hit()
                if game.player.isBusted():
                    game.phase = "results"
            return
        elif game.standButtonPos[0] <= pos[0] <= game.standButtonPos[0] + BUTTON_WIDTH and \
            game.standButtonPos[1] <= pos[1] <= game.standButtonPos[1] + BUTTON_HEIGHT:
            game.phase = "houseTurn"
            game.houseLogic()
            return

        


    if game.reloadButtonPos[0] <= pos[0] <= game.reloadButtonPos[0] + 75 and \
       game.reloadButtonPos[1] <= pos[1] <= game.reloadButtonPos[1] + 75:
        game.resetGame()


def draw():
    game.draw(screen)


pgzrun.go()

