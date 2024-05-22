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

# Players money
MONEYP1 = 1000
MONEYP2 = 1000
MONEYP3 = 1000

#Position of the players image
PLAYER1_IMAGE_POS = (270, 600)

# Game state
GAME_STATE = True # True = Playing, False = House wins

#! Load the images

# Cargar la imagen PNG con transparencia
PLAYER1_IMAGE = pygame.image.load("images/perfil1.png") # Load image

# Resize the image
new_width = 200
new_height = 150
resized_image = pygame.transform.scale(PLAYER1_IMAGE, (new_width, new_height))

# Convertir la imagen redimensionada a un Surface de Pygame Zero
resized_image_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
resized_image_surface.blit(resized_image, (0, 0))

def draw():
    logic()
    screen.clear()
    screen.blit('blackjack_fondo', (0, 0))
    screen.blit(resized_image_surface, PLAYER1_IMAGE_POS)


# Logic of the game
def logic():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Asign cards to players and house
    for i in range(2):
        PLAYER1.append((random.choice(numbers)))
        PLAYER2.append((random.choice(numbers)))
        PLAYER3.append((random.choice(numbers)))
        HOUSE.append((random.choice(numbers)))

    # while(GAME_STATE == True):
        if(sum(HOUSE) == 21):
            GAME_STATE = False
            print("House wins")

        if(sum(HOUSE) <= 16):
            HOUSE.append((random.choice(numbers)))

        

        print("Cards player 1 ", PLAYER1)
        print("Cards player 2 ", PLAYER2)
        print("Cards player 3 ", PLAYER3)
        print("Cards house ", HOUSE)


# Run the game
pgzrun.go()