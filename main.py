import pgzrun
import pygame
import random
import math

# Window size (background image size DON'T CHANGE)
WIDTH = 1286
HEIGHT = 772

# Players and house cards list
PLAYER1 = []
PLAYER2 = []
PLAYER3 = []
HOUSE = []

# First cards
FCPLAYER1 = 0
FCPLAYER2 = 0
FCPLAYER3 = 0
FCHOUSE = 0

# Second cards
SCPLAYER1 = 0
SCPLAYER2 = 0
SCPLAYER3 = 0
SCHOUSE = 0

# Game state
GAME_STATE = 1  # 1 = Playing, 0 = House wins


#! Load the images
# Position of the players image
PLAYER1_IMAGE_POS = (270, 600)

# Cargar la imagen PNG con transparencia
PLAYER1_IMAGE = pygame.image.load("images/perfil1.png")  # Load image

# Resize the image
new_width = 200
new_height = 150
resized_image = pygame.transform.scale(PLAYER1_IMAGE, (new_width, new_height))

# Convertir la imagen redimensionada a un Surface de Pygame Zero
resized_image_surface = pygame.Surface(
    (new_width, new_height), pygame.SRCALPHA)
resized_image_surface.blit(resized_image, (0, 0))


def draw():
    logic()
    print("First card player 1 ", FCPLAYER1)
    print("First card player 2 ", FCPLAYER2)
    screen.clear()
    screen.blit('blackjack_fondo', (0, 0))
    screen.blit(resized_image_surface, PLAYER1_IMAGE_POS)


# Logic of the game
def logic():
    global GAME_STATE, PLAYER1, PLAYER2, PLAYER3, HOUSE, FCPLAYER1, FCPLAYER2, FCPLAYER3, FCHOUSE, SCPLAYER1, SCPLAYER2, SCPLAYER3, SCHOUSE
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Asign cards to players and house
    for i in range(2):
        PLAYER1.append((random.choice(numbers)))
        PLAYER2.append((random.choice(numbers)))
        PLAYER3.append((random.choice(numbers)))
        HOUSE.append((random.choice(numbers)))
        if i == 0:
            FCPLAYER1 = PLAYER1[i]
            FCPLAYER2 = PLAYER2[i]
            FCPLAYER3 = PLAYER3[i]
            FCHOUSE = HOUSE[i]
        else:
            SCPLAYER1 = PLAYER1[i]
            SCPLAYER2 = PLAYER2[i]
            SCPLAYER3 = PLAYER3[i]
            SCHOUSE = HOUSE[i]

    print("Cards player 1 ", PLAYER1)
    print("Cards player 2 ", PLAYER2)
    print("Cards player 3 ", PLAYER3)
    print("Cards house ", HOUSE)


# Run the game
pgzrun.go()
