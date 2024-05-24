import pgzrun
import pygame
import random
import math
import os

# Window size (background image size DON'T CHANGE)
WIDTH = 1286
HEIGHT = 772
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)


# ------------------------------ VARIABLES ------------------------------

# Players and house cards list
PLAYER1 = []
PLAYER2 = []
PLAYER3 = []
HOUSE = []

# Variables to take the cards of the images folder
NAMECARD1 = []
NAMECARD2 = []
NAMECARD3 = []
NAMECARDHOUSE = []


# 1 = Playing, 0 = House wins, 3 = House wins with 21 or in the first play, 4 = Player wins
GAME_STATE_HOUSE = 1
GAME_STATE_PLAYER1 = 1
GAME_STATE_PLAYER2 = 1
GAME_STATE_PLAYER3 = 1


# ------------------------------ BUTTONS ------------------------------

# Definir la posición y el tamaño del botón
button_x = 350
button_y = 605
button_width = 80
button_height = 35
button_color_hit = (0, 179, 252)  # Verde
button_color_stand = (255, 31, 44)  # Rojo

# Cards size
CARD_WIDTH = 75
CARD_HEIGHT = 125

# ------------------------------ IMAGES ------------------------------

# Position of the players image
PLAYER1_IMAGE_POS = (280, 635)
PLAYER2_IMAGE_POS = (602, 652)
PLAYER3_IMAGE_POS = (927, 635)

# Cargar la imagen PNG con transparencia
PLAYER1_IMAGE = pygame.image.load("images/player 1 .png")  # Load image
PLAYER2_IMAGE = pygame.image.load("images/player 2.png")  # Load image
PLAYER3_IMAGE = pygame.image.load("images/player 3.png")  # Load image

# Resize the image
new_width = 300
new_height = 200
resized_image1 = pygame.transform.scale(PLAYER1_IMAGE, (new_width, new_height))
resized_image2 = pygame.transform.scale(
    PLAYER2_IMAGE, (new_width + 15, new_height))
resized_image3 = pygame.transform.scale(PLAYER3_IMAGE, (new_width, new_height))


# Convertir la imagen redimensionada a un Surface de Pygame Zero
resized_image_surface1 = pygame.Surface(
    (new_width, new_height), pygame.SRCALPHA)
resized_image_surface1.blit(resized_image1, (0, 0))

resized_image_surface2 = pygame.Surface(
    (new_width, new_height), pygame.SRCALPHA)
resized_image_surface2.blit(resized_image2, (0, 0))

resized_image_surface3 = pygame.Surface(
    (new_width, new_height), pygame.SRCALPHA)
resized_image_surface3.blit(resized_image3, (0, 0))

# ------------------------------ FUNTIONS ------------------------------


def update():
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3

    if (lose(PLAYER1) == True):
        GAME_STATE_PLAYER1 = 0
    if (lose(PLAYER2) == True):
        GAME_STATE_PLAYER2 = 0
    if (lose(PLAYER3) == True):
        GAME_STATE_PLAYER3 = 0


def draw():
    print("Cartas de player1 ", PLAYER1)
    screen.clear()
    screen.blit('blackjack_fondo', (0, 0))
    screen.blit(resized_image_surface1, PLAYER1_IMAGE_POS)
    screen.blit(resized_image_surface2, PLAYER2_IMAGE_POS)
    screen.blit(resized_image_surface3, PLAYER3_IMAGE_POS)

    screen.draw.filled_rect(
        Rect((button_x, button_y), (button_width, button_height)), button_color_hit)
    screen.draw.text("HIT", (button_x + 23, button_y + 10),
                     fontsize=30, color="black")

    screen.draw.filled_rect(
        Rect((button_x - 110, button_y), (button_width, button_height)), button_color_stand)
    screen.draw.text("STAND", (button_x - 105, button_y + 10),
                     fontsize=30, color="black")

    if (GAME_STATE_PLAYER1 == 0):
        screen.draw.text("Player 1 lose", (265, 500),
                         fontsize=50, color="red", shadow=(1, 1))

    drawCardsDisplay()


def on_mouse_down(pos):
    # Verificar si el clic fue dentro del área del botón
    if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
        moreCards(PLAYER1)
    elif button_x - 110 <= pos[0] <= button_x - 110 + button_width and button_y <= pos[1] <= button_y + button_height:
        passTurn(PLAYER1)

# Funtion to know if a player lose


def lose(player):
    if (sum(player) > 21):
        return True
    else:
        return False

# Function to take one more cards


def moreCards(player):
    print("More cards")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    if (sum(player) < 21):
        player.append((random.choice(numbers)))
        if (player.count(11) == 2):
            player.remove(11)
            player.append(1)
            if (sum(player) > 21):
                player.remove(11)
                player.append(1)
        if (sum(player) > 21):
            if (player.count(11) == 1):
                player.remove(11)
                player.append(1)
            else:
                GAME_STATE_PLAYER1 = 0
        if (sum(player) == 21):
            GAME_STATE_PLAYER1 = 4  # ! CORREGIR ESTO, NO SIEMPRE ES PLAYER 1

        i = len(player) - 1
        if player[i] == 10:  # ! CORREGIR ESTO, NO SIEMPRE ES NAMECARD1
            NAMECARD1.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        elif (player[i] == 11 or player[i] == 1):
            NAMECARD1.append(
                "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        else:
            NAMECARD1.append(str(player[i]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))


def passTurn(player):
    print("Pass turn")
    screen.draw.text("STAND", (265, 500))

# Logic of the game


def logic():
    global GAME_STATE_HOUSE, GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, PLAYER1, PLAYER2, PLAYER3, HOUSE
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

    drawCards()

    #! Esto es para hacer debug
    print("Cards player 1 ", PLAYER1)
    print("Cards player 2 ", PLAYER2)
    print("Cards player 3 ", PLAYER3)
    print("Cards house ", HOUSE)

# Funtion to draw the cards with the images and random figures


def drawCards():
    global NAMECARD1, NAMECARD2, NAMECARD3, NAMECARDHOUSE

    # Name of player 1 cards
    for i in range(len(PLAYER1)):
        if PLAYER1[i] == 10:
            NAMECARD1.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        elif PLAYER1[i] == 11 or PLAYER1[i] == 1:
            NAMECARD1.append(
                "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        else:
            NAMECARD1.append(str(PLAYER1[i]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
    print("Cartas de player 1 nombre real", NAMECARD1)

    # Name of player 2 cards
    for i in range(len(PLAYER2)):
        if PLAYER2[i] == 10:
            NAMECARD2.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        elif PLAYER2[i] == 11 or PLAYER2[i] == 1:
            NAMECARD2.append(
                "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        else:
            NAMECARD2.append(str(PLAYER2[i]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))

    # Name of player 3 cards
    for i in range(len(PLAYER3)):
        if PLAYER3[i] == 10:
            NAMECARD3.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        elif PLAYER3[i] == 11 or PLAYER3[i] == 1:
            NAMECARD3.append(
                "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        else:
            NAMECARD3.append(str(PLAYER3[i]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))

    # Name of house cards
    for i in range(len(HOUSE)):
        if HOUSE[i] == 10:
            NAMECARDHOUSE.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        elif HOUSE[i] == 11 or HOUSE[i] == 1:
            NAMECARDHOUSE.append(
                "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        else:
            NAMECARDHOUSE.append(str(HOUSE[i]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))


# ------------------------------ LOAD CARD IMAGES AND DRAW IT ------------------------------

# Funtion to load the images


def loadImages():
    images = {}
    for filename in os.listdir("images/cards"):
        path = os.path.join("images/cards", filename)
        if os.path.isfile(path):
            images[os.path.splitext(filename)[0]] = pygame.image.load(path)
    return images


IMAGES = loadImages()


def drawCardsDisplay():
    global PLAYER1, PLAYER2, PLAYER3, HOUSE, NAMECARD1, NAMECARD2, NAMECARD3, NAMECARDHOUSE

    # Dibujar las cartas de PLAYER1
    for i, card_name in enumerate(NAMECARD1):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER1_IMAGE_POS[0] +
                        i * 80, PLAYER1_IMAGE_POS[1] - 185)
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Dibujar las cartas de PLAYER2
    for i, card_name in enumerate(NAMECARD2):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER2_IMAGE_POS[0] - 30 +
                        i * 80, PLAYER2_IMAGE_POS[1] - 170)
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Dibujar las cartas de PLAYER3
    for i, card_name in enumerate(NAMECARD3):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER3_IMAGE_POS[0] - 50 +
                        i * 80, PLAYER3_IMAGE_POS[1] - 185)
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Dibujar las cartas de HOUSE
    for i, card_name in enumerate(NAMECARDHOUSE):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (470 + i * 80, 135)
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")


# Function to resize the cards
def resizeCards(image):
    resized_card = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
    return resized_card


def restart():
    logic()


# Run the game
logic()
pgzrun.go()
