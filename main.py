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

# 1 = Playing, 0 = House wins, 3 = House wins with 21 or in the first play
GAME_STATE_HOUSE = 1
GAME_STATE_PLAYER1 = 1
GAME_STATE_PLAYER2 = 1
GAME_STATE_PLAYER3 = 1


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
    screen.clear()
    screen.blit('blackjack_fondo', (0, 0))
    screen.blit(resized_image_surface, PLAYER1_IMAGE_POS)


# Logic of the game
def logic():
    global GAME_STATE_HOUSE, GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, PLAYER1, PLAYER2, PLAYER3, HOUSE, FCPLAYER1, FCPLAYER2, FCPLAYER3, FCHOUSE, SCPLAYER1, SCPLAYER2, SCPLAYER3, SCHOUSE
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    firstPlay = 0  # This is to control the first play of the house

    # Asign cards to players and house
    for i in range(2):
        PLAYER1.append((random.choice(numbers)))
        PLAYER2.append((random.choice(numbers)))
        PLAYER3.append((random.choice(numbers)))
        HOUSE.append((random.choice(numbers)))

        # This is to change the value of the card 11 to 1. Only if the player or house has two 11 cards
        if (HOUSE.count(11) == 2):
            HOUSE.remove(11)
            HOUSE.append(1)
        if (PLAYER1.count(11) == 2):
            PLAYER1.remove(11)
            PLAYER1.append(1)
        if (PLAYER2.count(11) == 2):
            PLAYER2.remove(11)
            PLAYER2.append(1)
        if (PLAYER3.count(11) == 2):
            PLAYER3.remove(11)
            PLAYER3.append(1)

        if i == 0:
            # Variables to take the cards of the images folder
            FCPLAYER1 = PLAYER1[i]
            FCPLAYER2 = PLAYER2[i]
            FCPLAYER3 = PLAYER3[i]
            FCHOUSE = HOUSE[i]
        else:
            SCPLAYER1 = PLAYER1[i]
            SCPLAYER2 = PLAYER2[i]
            SCPLAYER3 = PLAYER3[i]
            SCHOUSE = HOUSE[i]

    while (GAME_STATE_HOUSE == 1):
        # This is to control the cards taken by the house
        if (firstPlay == 0 and sum(HOUSE) == 21):
            GAME_STATE_HOUSE = 3
        if (sum(HOUSE) < 17):
            HOUSE.append((random.choice(numbers)))
            # This is to change the value of the card 11 to 1. Only if the player or house has two 11 cards
            if (HOUSE.count(11) == 2):
                HOUSE.remove(11)
                HOUSE.append(1)
        if (sum(HOUSE) > 21 and HOUSE.count(11) < 2):
            GAME_STATE_HOUSE = 0
        if (sum(HOUSE) > 16 and sum(HOUSE) < 22):
            GAME_STATE_HOUSE = 0

    #! Esto es para hacer debug
    print("Cards player 1 ", PLAYER1)
    print("Cards player 2 ", PLAYER2)
    print("Cards player 3 ", PLAYER3)
    print("Cards house ", HOUSE)


# Run the game
pgzrun.go()
