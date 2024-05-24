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


# 1 = Playing, 0 = House wins, 3 = House wins with 21 or in the first play, 4 = Player-House wins, 5 = end turn, 6 = insurance
GAME_STATE_HOUSE = 1
GAME_STATE_PLAYER1 = 1
GAME_STATE_PLAYER2 = 1
GAME_STATE_PLAYER3 = 1


# ------------------------------ BUTTONS ------------------------------

# Define the position and size of the button
button_x = 350
button_y = 605
button_width = 80
button_height = 35
button_color_hit = (0, 179, 252)  # Blue
button_color_stand = (255, 31, 44)  # Red

# Cards size
CARD_WIDTH = 75
CARD_HEIGHT = 125

# ------------------------------ IMAGES ------------------------------

# Position of the players image
PLAYER1_IMAGE_POS = (280, 635)
PLAYER2_IMAGE_POS = (602, 652)
PLAYER3_IMAGE_POS = (927, 635)

# Load PNG images with transparency
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


# Convert the resized image to a Pygame Zero Surface
resized_image_surface1 = pygame.Surface(
    (new_width, new_height), pygame.SRCALPHA)
resized_image_surface1.blit(resized_image1, (0, 0))

resized_image_surface2 = pygame.Surface(
    (new_width, new_height), pygame.SRCALPHA)
resized_image_surface2.blit(resized_image2, (0, 0))

resized_image_surface3 = pygame.Surface(
    (new_width, new_height), pygame.SRCALPHA)
resized_image_surface3.blit(resized_image3, (0, 0))

# ------------------------------ FUNCTIONS ------------------------------


def update():
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3

    if lose(PLAYER1):
        GAME_STATE_PLAYER1 = 0
    if lose(PLAYER2):
        GAME_STATE_PLAYER2 = 0
    if lose(PLAYER3):
        GAME_STATE_PLAYER3 = 0
    if passTurnP1():
        GAME_STATE_PLAYER1 = 5
    if passTurnP2():
        GAME_STATE_PLAYER2 = 5
    if blackjack(PLAYER1):
        GAME_STATE_PLAYER1 = 4
    if blackjack(PLAYER2):
        GAME_STATE_PLAYER2 = 4


def draw():
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3
    
    screen.clear()
    screen.blit('blackjack_fondo', (0, 0))
    screen.blit(resized_image_surface1, PLAYER1_IMAGE_POS)
    screen.blit(resized_image_surface2, PLAYER2_IMAGE_POS)
    screen.blit(resized_image_surface3, PLAYER3_IMAGE_POS)
    drawCardsDisplay()

    if GAME_STATE_HOUSE == 3:
        screen.draw.text("BLACKJACK", (470, 100),
                         fontsize=50, color="yellow", shadow=(1, 1))



    if GAME_STATE_PLAYER1 == 1:
        drawButtonsP1()
    if GAME_STATE_PLAYER1 == 0:
        screen.draw.text("LOSE", (295, 500),
                         fontsize=50, color="red", shadow=(1, 1))
    if GAME_STATE_PLAYER1 == 5:
        screen.draw.text("STAND", (295, 500), fontsize=50,
                         color="red", shadow=(1, 1))
    if GAME_STATE_PLAYER1 == 4:
        screen.draw.text("BLACKJACK", (295, 500),
                         fontsize=50, color="yellow", shadow=(1, 1))
        
    if GAME_STATE_PLAYER2 == 1 and (GAME_STATE_PLAYER1 == 5 or GAME_STATE_PLAYER1 == 0 or GAME_STATE_PLAYER1 == 4):
        drawButtonsP2()
    if GAME_STATE_PLAYER2 == 0:
        screen.draw.text("LOSE", (620, 500),
                         fontsize=50, color="red", shadow=(1, 1))
    if GAME_STATE_PLAYER2 == 5:
        screen.draw.text("STAND", (620, 500), fontsize=50,
                         color="red", shadow=(1, 1))
    if GAME_STATE_PLAYER2 == 4:
        screen.draw.text("BLACKJACK", (620, 500),
                         fontsize=50, color="yellow", shadow=(1, 1))
    
    if GAME_STATE_PLAYER3 == 1 and (GAME_STATE_PLAYER2 == 5 or GAME_STATE_PLAYER2 == 0 or GAME_STATE_PLAYER2 == 4):
        drawButtonsP3()
    if GAME_STATE_PLAYER3 == 0:
        screen.draw.text("LOSE", (945, 500),
                         fontsize=50, color="red", shadow=(1, 1))
    if GAME_STATE_PLAYER3 == 5:
        screen.draw.text("STAND", (945, 500), fontsize=50,
                         color="red", shadow=(1, 1))
    if GAME_STATE_PLAYER3 == 4:
        screen.draw.text("BLACKJACK", (945, 500),
                         fontsize=50, color="yellow", shadow=(1, 1))

    #! TODAVIA NO ME DICE QUIEN GANA
    if GAME_STATE_HOUSE == 4:
        #Player 1 state
        if( sum(PLAYER1) > sum(HOUSE) and sum(PLAYER1) < 22):
            screen.draw.text("WIN", (470, 100),
                            fontsize=50, color="green", shadow=(1, 1))
        elif(sum(PLAYER1) == sum(HOUSE)):
            screen.draw.text("PUSH", (470, 100),
                            fontsize=50, color="yellow", shadow=(1, 1))
        else:
            screen.draw.text("LOSE", (470, 100),
                            fontsize=50, color="red", shadow=(1, 1))
        # Player 2 state
        if( sum(PLAYER2) > sum(HOUSE) and sum(PLAYER2) < 22):
            screen.draw.text("WIN", (470, 100),
                            fontsize=50, color="green", shadow=(1, 1))
        elif(sum(PLAYER2) == sum(HOUSE)):
            screen.draw.text("PUSH", (470, 100),
                            fontsize=50, color="yellow", shadow=(1, 1))
        else:
            screen.draw.text("LOSE", (470, 100),
                            fontsize=50, color="red", shadow=(1, 1))

        # Player 3 state
        if( sum(PLAYER3) > sum(HOUSE) and sum(PLAYER3) < 22):
            screen.draw.text("WIN", (470, 100),
                            fontsize=50, color="green", shadow=(1, 1))
        elif(sum(PLAYER3) == sum(HOUSE)):
            screen.draw.text("PUSH", (470, 100),
                            fontsize=50, color="yellow", shadow=(1, 1))
        else:
            screen.draw.text("LOSE", (470, 100),
                            fontsize=50, color="red", shadow=(1, 1))      



def drawButtonsP1():
    screen.draw.filled_rect(
        Rect((button_x, button_y), (button_width, button_height)), button_color_hit)
    screen.draw.text("HIT", (button_x + 23, button_y + 10),
                     fontsize=30, color="black")

    screen.draw.filled_rect(
        Rect((button_x - 110, button_y), (button_width, button_height)), button_color_stand)
    screen.draw.text("STAND", (button_x - 105, button_y + 10),
                     fontsize=30, color="black")
    
def drawButtonsP2():
    screen.draw.filled_rect(
        Rect((button_x + 308, button_y + 14), (button_width, button_height)), button_color_hit)
    screen.draw.text("HIT", (button_x + 330, button_y + 23),
                     fontsize=30, color="black")

    screen.draw.filled_rect(
        Rect((button_x + 205, button_y + 14), (button_width, button_height)), button_color_stand)
    screen.draw.text("STAND", (button_x + 212, button_y + 23),
                     fontsize=30, color="black")

def drawButtonsP3():
    screen.draw.filled_rect(
        Rect((button_x + 615, button_y), (button_width, button_height)), button_color_hit)
    screen.draw.text("HIT", (button_x + 640, button_y + 10),
                     fontsize=30, color="black")

    screen.draw.filled_rect(
        Rect((button_x + 514, button_y), (button_width, button_height)), button_color_stand)
    screen.draw.text("STAND", (button_x + 520, button_y + 10),
                     fontsize=30, color="black")


# Function to know if the mouse is clicked
def on_mouse_down(pos):
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3
    # Check if the click was within the button area
    if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
        moreCards(PLAYER1)
    elif button_x - 110 <= pos[0] <= button_x - 110 + button_width and button_y <= pos[1] <= button_y + button_height:
        GAME_STATE_PLAYER1 = 5
        return GAME_STATE_PLAYER1
    if button_x + 308 <= pos[0] <= button_x + 308 + button_width and button_y + 14 <= pos[1] <= button_y + 14 + button_height:
        moreCards(PLAYER2)
    elif button_x + 205 <= pos[0] <= button_x + 205 + button_width and button_y + 14 <= pos[1] <= button_y + 14 + button_height:
        GAME_STATE_PLAYER2 = 5
        return GAME_STATE_PLAYER2
    if button_x + 615 <= pos[0] <= button_x + 615 + button_width and button_y <= pos[1] <= button_y + button_height:
        moreCards(PLAYER3)
    elif button_x + 514 <= pos[0] <= button_x + 514 + button_width and button_y <= pos[1] <= button_y + button_height:
        GAME_STATE_PLAYER3 = 5
        return GAME_STATE_PLAYER3

# Function to check if a player loses


def lose(player):
    return sum(player) > 21

# Function to take one more card


def moreCards(player):
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, PLAYER1, PLAYER2, PLAYER3
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    if sum(player) < 21:
        player.append((random.choice(numbers)))
        if player.count(11) == 2:
            player.remove(11)
            player.append(1)
            if sum(player) > 21:
                player.remove(11)
                player.append(1)
        if sum(player) > 21:
            if player.count(11) == 1:
                player.remove(11)
                player.append(1)
            else:
                if(player == PLAYER1):
                    GAME_STATE_PLAYER1 = 0
                elif (player == PLAYER2):
                    GAME_STATE_PLAYER2 = 0
                elif (player == PLAYER3):
                    GAME_STATE_PLAYER3 = 0
        
        if sum(player) == 21:
            if(player == PLAYER1):
                    GAME_STATE_PLAYER1 = 4
            elif (player == PLAYER2):
                    GAME_STATE_PLAYER2 = 4
            elif (player == PLAYER3):
                    GAME_STATE_PLAYER3 = 4

        i = len(player) - 1
        if player[i] == 10: 
            if(player == PLAYER1):
                NAMECARD1.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER2):
                NAMECARD2.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER3):
                NAMECARD3.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        elif player[i] == 11 or player[i] == 1:
            if(player == PLAYER1):
                NAMECARD1.append(
                "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER2):
                NAMECARD2.append(
                "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER3):
                NAMECARD3.append(
                "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        else:
            if(player == PLAYER1):
                NAMECARD1.append(str(player[i]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER2):
                NAMECARD2.append(str(player[i]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER3):
                NAMECARD3.append(str(player[i]) + "_de_" + random.choice(
                ["Corazones", "Diamantes", "Espadas", "Tréboles"]))


def passTurnP1():
    return GAME_STATE_PLAYER1 == 5

def passTurnP2():
    return GAME_STATE_PLAYER2 == 5

def passTurnP3():
    return GAME_STATE_PLAYER3 == 5

def blackjack(player):
    return sum(player) == 21

# Game logic


def logic():
    global GAME_STATE_HOUSE, GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, PLAYER1, PLAYER2, PLAYER3, HOUSE
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    firstPlay = 0  # This is to control the first play of the house

    # Assign cards to players and house
    for i in range(2):
        PLAYER1.append((random.choice(numbers)))
        PLAYER2.append((random.choice(numbers)))
        PLAYER3.append((random.choice(numbers)))
        HOUSE.append((random.choice(numbers)))

        # This is to change the value of the card 11 to 1. Only if the player or house has two 11 cards
        if HOUSE.count(11) == 2:
            HOUSE.remove(11)
            HOUSE.append(1)
        if PLAYER1.count(11) == 2:
            PLAYER1.remove(11)
            PLAYER1.append(1)
        if PLAYER2.count(11) == 2:
            PLAYER2.remove(11)
            PLAYER2.append(1)
        if PLAYER3.count(11) == 2:
            PLAYER3.remove(11)
            PLAYER3.append(1)

    while GAME_STATE_HOUSE == 1:
        # This is to control the cards taken by the house
        if firstPlay == 0 and sum(HOUSE) == 21:
            GAME_STATE_HOUSE = 3
        if sum(HOUSE) < 17:
            HOUSE.append((random.choice(numbers)))
            # This is to change the value of the card 11 to 1. Only if the player or house has two 11 cards
            if HOUSE.count(11) == 2:
                HOUSE.remove(11)
                HOUSE.append(1)
        if sum(HOUSE) > 21 and HOUSE.count(11) < 2:
            GAME_STATE_HOUSE = 0
        if sum(HOUSE) > 16 and sum(HOUSE) < 22:
            GAME_STATE_HOUSE = 4

    drawCards()

    #! This is for debugging
    print("Cards player 1 ", PLAYER1)
    print("Cards player 2 ", PLAYER2)
    print("Cards player 3 ", PLAYER3)
    print("Cards house ", HOUSE)

# Function to draw the cards with the images and random figures


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

# Function to load the images


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

    # Draw PLAYER1 cards
    for i, card_name in enumerate(NAMECARD1):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER1_IMAGE_POS[0] +
                        i * 80, PLAYER1_IMAGE_POS[1] - 185)
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Draw PLAYER2 cards
    for i, card_name in enumerate(NAMECARD2):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER2_IMAGE_POS[0] - 30 +
                        i * 80, PLAYER2_IMAGE_POS[1] - 170)
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Draw PLAYER3 cards
    for i, card_name in enumerate(NAMECARD3):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER3_IMAGE_POS[0] - 50 +
                        i * 80, PLAYER3_IMAGE_POS[1] - 185)
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Draw HOUSE cards
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
