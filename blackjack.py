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


# 1 = Playing, 0 = Player or House lose, 3 = House wins with 21 or in the first play, 4 = Player-House wins, 5 = end turn, 6 = insurance, 7 = bet time, 8 = waiting, 9 = no money
GAME_STATE_HOUSE = 1
GAME_STATE_PLAYER1 = 7
GAME_STATE_PLAYER2 = 8
GAME_STATE_PLAYER3 = 8


# Money of the players
MONEYP1 = 1000
MONEYP2 = 1000
MONEYP3 = 1000

# Last bet of the players
LASTBETP1 = 0
LASTBETP2 = 0
LASTBETP3 = 0

# Pay of the players
PAYP1 = 0
PAYP2 = 0
PAYP3 = 0

# Insurance bet
INSURANCEBET = 0

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

# Reload button
CENTER_C = (200, 200)
RADIUS = 50

# ------------------------------ IMAGES ------------------------------

RELOAD_BUTTON = Actor("reload", pos=(1180, 118))
FICHA20 = Actor("ficha25.png", pos=(60, 200))
FICHA50 = Actor("ficha50.png", pos=(60, 280))
FICHA100 = Actor("ficha100.png", pos=(60, 360))
FICHA500 = Actor("ficha500.png", pos=(60, 440))

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
    if blackjack(PLAYER3):
        GAME_STATE_PLAYER3 = 4

# Main function to draw the game


def draw():
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, NAMECARD1, NAMECARD2, NAMECARD3, NAMECARDHOUSE, MONEYP1, MONEYP2, MONEYP3, PAYP1, PAYP2, PAYP3, LASTBETP1, LASTBETP2, LASTBETP3, INSURANCEBET

    screen.clear()
    screen.blit('blackjack_fondo', (0, 0))
    screen.blit(resized_image_surface1, PLAYER1_IMAGE_POS)
    screen.blit(resized_image_surface2, PLAYER2_IMAGE_POS)
    screen.blit(resized_image_surface3, PLAYER3_IMAGE_POS)
    RELOAD_BUTTON.draw()

    screen.draw.text(f'{MONEYP1}', (390, 689), fontsize=30,
                     color="yellow", shadow=(1, 1))
    screen.draw.text(f'{MONEYP2}', (710, 700), fontsize=30,
                     color="yellow", shadow=(1, 1))
    screen.draw.text(f'{MONEYP3}', (1035, 665), fontsize=30,
                     color="yellow", shadow=(1, 1))

    # Bet time
    if (GAME_STATE_PLAYER1 == 8 or GAME_STATE_PLAYER2 == 8 or GAME_STATE_PLAYER3 == 8) or (LASTBETP1 == 0 or LASTBETP2 == 0 or LASTBETP3 == 0):
        if GAME_STATE_PLAYER1 == 7 and MONEYP1 != 0:
            screen.draw.text("BET PLAYER 1", (CENTER_X - 100, CENTER_Y - 50), fontsize=50,
                             color="yellow", shadow=(1, 1))
            FICHA20.draw()
            FICHA50.draw()
            FICHA100.draw()
            FICHA500.draw()
        elif LASTBETP1 == 0:
            GAME_STATE_PLAYER1 = 1
            LASTBETP1 = 2
            GAME_STATE_PLAYER2 = 7

        if GAME_STATE_PLAYER2 == 7 and MONEYP2 != 0:
            screen.draw.text("BET PLAYER 2", (CENTER_X - 100, CENTER_Y - 50), fontsize=50,
                             color="yellow", shadow=(1, 1))
            FICHA20.draw()
            FICHA50.draw()
            FICHA100.draw()
            FICHA500.draw()
        elif LASTBETP2 == 0 and GAME_STATE_PLAYER2 != 8:
            GAME_STATE_PLAYER2 = 1
            LASTBETP2 = 2
            GAME_STATE_PLAYER3 = 7

        if GAME_STATE_PLAYER3 == 7 and MONEYP3 != 0:
            screen.draw.text("BET PLAYER 3", (CENTER_X - 100, CENTER_Y - 50), fontsize=50,
                             color="yellow", shadow=(1, 1))
            FICHA20.draw()
            FICHA50.draw()
            FICHA100.draw()
            FICHA500.draw()
        elif LASTBETP3 == 0 and GAME_STATE_PLAYER3 != 8:
            GAME_STATE_PLAYER3 = 1
            LASTBETP3 = 2
    else:  # Game time
        if GAME_STATE_HOUSE == 3:  # House wins with 21 or in the first play
            drawCardsDisplay()
            if (INSURANCEBET == 1):  # Insurance bet
                drawButtonInsuranceP1()
                drawButtonInsuranceP2()
                drawButtonInsuranceP3()
                if GAME_STATE_PLAYER1 == 6 and GAME_STATE_PLAYER2 == 6 and GAME_STATE_PLAYER3 == 6:
                    GAME_STATE_PLAYER1 = 1
                    GAME_STATE_PLAYER2 = 1
                    GAME_STATE_PLAYER3 = 1
                    INSURANCEBET = 0
            else:  # No insurance bet
                drawCardsHouse()
                screen.draw.text("BLACKJACK", (470, 100),
                                 fontsize=50, color="yellow", shadow=(1, 1))
                if GAME_STATE_PLAYER1 == 4:
                    screen.draw.text("PUSH", (295, 500),
                                     fontsize=50, color="yellow", shadow=(1, 1))
                    if PAYP1 == 0:
                        MONEYP1 += LASTBETP1
                    PAYP1 = 1
                else:
                    screen.draw.text("LOSE", (295, 500),
                                     fontsize=50, color="red", shadow=(1, 1))
                    poorPlayer()
                if GAME_STATE_PLAYER2 == 4:
                    screen.draw.text("PUSH", (620, 500),
                                     fontsize=50, color="yellow", shadow=(1, 1))
                    if PAYP2 == 0:
                        MONEYP2 += LASTBETP2
                    PAYP2 = 1
                else:
                    screen.draw.text("LOSE", (620, 500),
                                     fontsize=50, color="red", shadow=(1, 1))
                    poorPlayer()
                if GAME_STATE_PLAYER3 == 4:
                    screen.draw.text("PUSH", (945, 500),
                                     fontsize=50, color="yellow", shadow=(1, 1))
                    if PAYP3 == 0:
                        MONEYP3 += LASTBETP3
                    PAYP3 = 1
                else:
                    screen.draw.text("LOSE", (945, 500),
                                     fontsize=50, color="red", shadow=(1, 1))
                    poorPlayer()
        else:  # House doesn't win with 21 or in the first play
            drawCardsDisplay()
            if (INSURANCEBET == 1):
                drawButtonInsuranceP1()
                drawButtonInsuranceP2()
                drawButtonInsuranceP3()
                if GAME_STATE_PLAYER1 == 6 and GAME_STATE_PLAYER2 == 6 and GAME_STATE_PLAYER3 == 6:
                    GAME_STATE_PLAYER1 = 1
                    GAME_STATE_PLAYER2 = 1
                    GAME_STATE_PLAYER3 = 1
                    INSURANCEBET = 0
            else:  # Each player calls for cards
                if GAME_STATE_PLAYER1 != 9:
                    if GAME_STATE_PLAYER1 == 1:
                        drawButtonsP1()
                    if GAME_STATE_PLAYER1 == 0:
                        screen.draw.text("LOSE", (295, 500),
                                         fontsize=50, color="red", shadow=(1, 1))
                    if GAME_STATE_PLAYER1 == 5:
                        screen.draw.text("STAND", (295, 500), fontsize=50,
                                         color="blue", shadow=(1, 1))
                    if GAME_STATE_PLAYER1 == 4:
                        screen.draw.text("BLACKJACK", (295, 500),
                                         fontsize=50, color="yellow", shadow=(1, 1))

                if (GAME_STATE_PLAYER2 == 1 and GAME_STATE_PLAYER2 != 9) and (GAME_STATE_PLAYER1 == 5 or GAME_STATE_PLAYER1 == 0 or GAME_STATE_PLAYER1 == 4 or GAME_STATE_PLAYER1 == 9):  # When player 1 ends his turn
                    drawButtonsP2()
                if GAME_STATE_PLAYER2 == 0:
                    screen.draw.text("LOSE", (620, 500),
                                     fontsize=50, color="red", shadow=(1, 1))
                if GAME_STATE_PLAYER2 == 5:
                    screen.draw.text("STAND", (620, 500), fontsize=50,
                                     color="blue", shadow=(1, 1))
                if GAME_STATE_PLAYER2 == 4:
                    screen.draw.text("BLACKJACK", (620, 500),
                                     fontsize=50, color="yellow", shadow=(1, 1))

                if (GAME_STATE_PLAYER3 == 1 and GAME_STATE_PLAYER3 != 9) and (GAME_STATE_PLAYER2 == 5 or GAME_STATE_PLAYER2 == 0 or GAME_STATE_PLAYER2 == 4 or GAME_STATE_PLAYER2 == 9):
                    drawButtonsP3()
                if GAME_STATE_PLAYER3 == 0:
                    screen.draw.text("LOSE", (945, 500),
                                     fontsize=50, color="red", shadow=(1, 1))
                if GAME_STATE_PLAYER3 == 5:
                    screen.draw.text("STAND", (945, 500), fontsize=50,
                                     color="blue", shadow=(1, 1))
                if GAME_STATE_PLAYER3 == 4:
                    screen.draw.text("BLACKJACK", (945, 500),
                                     fontsize=50, color="yellow", shadow=(1, 1))

                if (GAME_STATE_HOUSE == 4 or GAME_STATE_HOUSE == 0) and (GAME_STATE_PLAYER3 == 0 or GAME_STATE_PLAYER3 == 5 or GAME_STATE_PLAYER3 == 4 or GAME_STATE_PLAYER3 == 9):  # The winners are decided
                    drawCardsHouse()
                    # Player 1 state
                    if ((sum(PLAYER1) > sum(HOUSE) and sum(PLAYER1) < 22) or sum(HOUSE) > 21):
                        screen.draw.text("WIN", (295, 400),
                                         fontsize=50, color="green", shadow=(1, 1))
                        if GAME_STATE_PLAYER1 == 4 and PAYP1 == 0:
                            MONEYP1 += math.floor(LASTBETP1 * 2.5)
                        elif PAYP1 == 0:
                            MONEYP1 += LASTBETP1 * 2
                        PAYP1 = 1
                    elif (sum(PLAYER1) == sum(HOUSE)):
                        screen.draw.text("PUSH", (295, 400),
                                         fontsize=50, color="yellow", shadow=(1, 1))
                        if PAYP1 == 0:
                            MONEYP1 += LASTBETP1
                        PAYP1 = 1
                    else:
                        screen.draw.text("LOSE", (295, 400),
                                         fontsize=50, color="red", shadow=(1, 1))
                        poorPlayer()
                    # Player 2 state
                    if (sum(PLAYER2) > sum(HOUSE) and sum(PLAYER2) < 22) or sum(HOUSE) > 21:
                        screen.draw.text("WIN", (620, 430),
                                         fontsize=50, color="green", shadow=(1, 1))
                        if GAME_STATE_PLAYER2 == 4 and PAYP2 == 0:
                            MONEYP2 += math.floor(LASTBETP2 * 2.5)
                        elif PAYP2 == 0:
                            MONEYP2 += LASTBETP2 * 2
                        PAYP2 = 1
                    elif (sum(PLAYER2) == sum(HOUSE)):
                        screen.draw.text("PUSH", (620, 430),
                                         fontsize=50, color="yellow", shadow=(1, 1))
                        if PAYP2 == 0:
                            MONEYP2 += LASTBETP2
                        PAYP2 = 1
                    else:
                        screen.draw.text("LOSE", (620, 430),
                                         fontsize=50, color="red", shadow=(1, 1))
                        poorPlayer()

                    # Player 3 state
                    if (sum(PLAYER3) > sum(HOUSE) and sum(PLAYER3) < 22) or sum(HOUSE) > 21:
                        screen.draw.text("WIN", (945, 400),
                                         fontsize=50, color="green", shadow=(1, 1))
                        if GAME_STATE_PLAYER3 == 4 and PAYP3 == 0:
                            MONEYP3 += math.floor(LASTBETP3 * 2.5)
                        elif PAYP3 == 0:
                            MONEYP3 += LASTBETP3 * 2
                        PAYP3 = 1
                    elif (sum(PLAYER3) == sum(HOUSE)):
                        screen.draw.text("PUSH", (945, 400),
                                         fontsize=50, color="yellow", shadow=(1, 1))
                        if PAYP3 == 0:
                            MONEYP3 += LASTBETP3
                        PAYP3 = 1
                    else:
                        screen.draw.text("LOSE", (945, 400),
                                         fontsize=50, color="red", shadow=(1, 1))
                        poorPlayer()
                RELOAD_BUTTON.draw()


# Draw buttons to take more cards, stand or double for any player
def drawButtonsP1():
    screen.draw.filled_rect(
        Rect((button_x, button_y), (button_width, button_height)), button_color_hit)
    screen.draw.text("HIT", (button_x + 23, button_y + 10),
                     fontsize=30, color="black")

    screen.draw.filled_rect(
        Rect((button_x - 110, button_y), (button_width, button_height)), button_color_stand)
    screen.draw.text("STAND", (button_x - 105, button_y + 10),
                     fontsize=30, color="black")

    screen.draw.filled_rect(Rect((button_x + 110, button_y),
                                 (button_width + 17, button_height)), (255, 255, 0))
    screen.draw.text("DOUBLE", (button_x + 115, button_y + 10),
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

    screen.draw.filled_rect(Rect((button_x + 415, button_y + 14),
                                 (button_width + 17, button_height)), (255, 255, 0))
    screen.draw.text("DOUBLE", (button_x + 420, button_y + 23),
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

    screen.draw.filled_rect(Rect((button_x + 715, button_y),
                                 (button_width + 17, button_height)), (255, 255, 0))
    screen.draw.text("DOUBLE", (button_x + 720, button_y + 10),
                     fontsize=30, color="black")


# Draw buttons to insurance or no insurance for any player
def drawButtonInsuranceP1():
    screen.draw.filled_rect(
        Rect((button_x - 75, button_y - 220), (button_width + 80, button_height)), button_color_hit)
    screen.draw.text("INSURANCE", (button_x - 55, button_y - 210),
                     fontsize=30, color="black")

    screen.draw.filled_rect(
        Rect((button_x - 75, button_y - 180), (button_width + 80, button_height)), button_color_stand)
    screen.draw.text("NO INSURANCE", (button_x - 73, button_y - 170),
                     fontsize=30, color="black")


def drawButtonInsuranceP2():
    screen.draw.filled_rect(
        Rect((button_x - 85 + 308, button_y - 206), (button_width + 80, button_height)), button_color_hit)
    screen.draw.text("INSURANCE", (button_x - 65 + 308, button_y - 196),
                     fontsize=30, color="black")

    screen.draw.filled_rect(
        Rect((button_x - 85 + 308, button_y - 166), (button_width + 80, button_height)), button_color_stand)
    screen.draw.text("NO INSURANCE", (button_x - 83 + 308, button_y - 156),
                     fontsize=30, color="black")


def drawButtonInsuranceP3():
    screen.draw.filled_rect(
        Rect((button_x - 75 + 615, button_y - 220), (button_width + 80, button_height)), button_color_hit)
    screen.draw.text("INSURANCE", (button_x - 55 + 615, button_y - 210),
                     fontsize=30, color="black")

    screen.draw.filled_rect(
        Rect((button_x - 75 + 615, button_y - 180), (button_width + 80, button_height)), button_color_stand)
    screen.draw.text("NO INSURANCE", (button_x - 73 + 615, button_y - 170),
                     fontsize=30, color="black")

# Function to know if the mouse is clicked


def on_mouse_down(pos):
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, MONEYP1, MONEYP2, MONEYP3, INSURANCEBET, LASTBETP1, LASTBETP2, LASTBETP3
    # Check if the click was within the button area
    if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:  # Hit button
        moreCards(PLAYER1)
    elif button_x - 110 <= pos[0] <= button_x - 110 + button_width and button_y <= pos[1] <= button_y + button_height:  # Stand button
        GAME_STATE_PLAYER1 = 5
        return GAME_STATE_PLAYER1
    elif button_x + 110 <= pos[0] <= button_x + 110 + button_width and button_y <= pos[1] <= button_y + button_height:  # Double button
        if LASTBETP1 != 0:
            GAME_STATE_PLAYER1 = 7
            bet(LASTBETP1)
            moreCards(PLAYER1)
            GAME_STATE_PLAYER1 = 5
            GAME_STATE_PLAYER2 = 1
            return GAME_STATE_PLAYER1
    if button_x + 308 <= pos[0] <= button_x + 308 + button_width and button_y + 14 <= pos[1] <= button_y + 14 + button_height:  # Hit button
        moreCards(PLAYER2)
    elif button_x + 205 <= pos[0] <= button_x + 205 + button_width and button_y + 14 <= pos[1] <= button_y + 14 + button_height:  # Stand button
        GAME_STATE_PLAYER2 = 5
        return GAME_STATE_PLAYER2
    elif button_x + 415 <= pos[0] <= button_x + 415 + button_width and button_y + 14 <= pos[1] <= button_y + 14 + button_height:  # Double button
        if LASTBETP2 != 0:
            GAME_STATE_PLAYER2 = 7
            bet(LASTBETP2)
            moreCards(PLAYER2)
            GAME_STATE_PLAYER2 = 5
            GAME_STATE_PLAYER3 = 1
            return GAME_STATE_PLAYER2
    if button_x + 615 <= pos[0] <= button_x + 615 + button_width and button_y <= pos[1] <= button_y + button_height:  # Hit button
        moreCards(PLAYER3)
    elif button_x + 514 <= pos[0] <= button_x + 514 + button_width and button_y <= pos[1] <= button_y + button_height:  # Stand button
        GAME_STATE_PLAYER3 = 5
        return GAME_STATE_PLAYER3
    elif button_x + 715 <= pos[0] <= button_x + 715 + button_width and button_y <= pos[1] <= button_y + button_height:  # Double button
        if LASTBETP3 != 0:
            GAME_STATE_PLAYER3 = 7
            bet(LASTBETP3)
            moreCards(PLAYER3)
            GAME_STATE_PLAYER3 = 5
            return GAME_STATE_PLAYER3

    # Check if the click was within the reload button area
    if RELOAD_BUTTON.collidepoint(pos):
        restart()

    # Check if the click was within the chip area
    if FICHA20.collidepoint(pos):
        if GAME_STATE_PLAYER1 == 7:
            if MONEYP1 >= 20:
                bet(20)
                return MONEYP1
        if GAME_STATE_PLAYER2 == 7:
            if MONEYP2 >= 20:
                bet(20)
                return MONEYP2
        if GAME_STATE_PLAYER3 == 7:
            if MONEYP3 >= 20:
                bet(20)
                return MONEYP3
    if FICHA50.collidepoint(pos):
        if GAME_STATE_PLAYER1 == 7:
            if MONEYP1 >= 50:
                bet(50)
                return MONEYP1
        if GAME_STATE_PLAYER2 == 7:
            if MONEYP2 >= 50:
                bet(50)
                return MONEYP2
        if GAME_STATE_PLAYER3 == 7:
            if MONEYP3 >= 50:
                bet(50)
                return MONEYP3
    if FICHA100.collidepoint(pos):
        if GAME_STATE_PLAYER1 == 7:
            if MONEYP1 >= 100:
                bet(100)
                return MONEYP1
        if GAME_STATE_PLAYER2 == 7:
            if MONEYP2 >= 100:
                bet(100)
                return MONEYP2
        if GAME_STATE_PLAYER3 == 7:
            if MONEYP3 >= 100:
                bet(100)
                return MONEYP3
    if FICHA500.collidepoint(pos):
        if GAME_STATE_PLAYER1 == 7:
            if MONEYP1 >= 500:
                bet(500)
                return MONEYP1
        if GAME_STATE_PLAYER2 == 7:
            if MONEYP2 >= 500:
                bet(500)
                return MONEYP2
        if GAME_STATE_PLAYER3 == 7:
            if MONEYP3 >= 500:
                bet(500)
                return MONEYP3

    # Insurance button for each player
    if button_x - 75 <= pos[0] <= button_x - 75 + button_width + 80:
        if button_y - 220 <= pos[1] <= button_y - 220 + button_height:
            handle_insurance(PLAYER1)
        elif button_y - 180 <= pos[1] <= button_y - 180 + button_height:
            handle_no_insurance(PLAYER1)

    if button_x - 75 + 308 <= pos[0] <= button_x - 75 + 308 + button_width + 80:
        if button_y - 206 <= pos[1] <= button_y - 206 + button_height:
            handle_insurance(PLAYER2)
        elif button_y - 166 <= pos[1] <= button_y - 166 + button_height:
            handle_no_insurance(PLAYER2)

    if button_x - 75 + 615 <= pos[0] <= button_x - 75 + 615 + button_width + 80:
        if button_y - 220 <= pos[1] <= button_y - 220 + button_height:
            handle_insurance(PLAYER3)
        elif button_y - 180 <= pos[1] <= button_y - 180 + button_height:
            handle_no_insurance(PLAYER3)

# Function to insurance or no insurance for each player


def handle_insurance(player):
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, GAME_STATE_HOUSE, MONEYP1, MONEYP2, MONEYP3, PLAYER1, PLAYER2, PLAYER3, HOUSE, LASTBETP1, LASTBETP2, LASTBETP3
    if player == PLAYER1:
        if GAME_STATE_HOUSE == 3:
            MONEYP1 += LASTBETP1
        else:
            INSURANCE = math.floor(LASTBETP1 / 2)
            MONEYP1 -= INSURANCE
        GAME_STATE_PLAYER1 = 6
    if player == PLAYER2:
        if GAME_STATE_HOUSE == 3:
            MONEYP2 += LASTBETP2
        else:
            INSURANCE = math.floor(LASTBETP2 / 2)
            MONEYP2 -= INSURANCE
        GAME_STATE_PLAYER2 = 6
    if player == PLAYER3:
        if GAME_STATE_HOUSE == 3:
            MONEYP3 += LASTBETP3
        else:
            INSURANCE = math.floor(LASTBETP3 / 2)
            MONEYP3 -= INSURANCE
        GAME_STATE_PLAYER3 = 6


def handle_no_insurance(player):
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, GAME_STATE_HOUSE, MONEYP1, MONEYP2, MONEYP3, PLAYER1, PLAYER2, PLAYER3, HOUSE, LASTBETP1, LASTBETP2, LASTBETP3
    if player == PLAYER1:
        if GAME_STATE_HOUSE == 3:
            MONEYP1 -= LASTBETP1
        GAME_STATE_PLAYER1 = 6
    if player == PLAYER2:
        if GAME_STATE_HOUSE == 3:
            MONEYP2 -= LASTBETP2
        GAME_STATE_PLAYER2 = 6
    if player == PLAYER3:
        if GAME_STATE_HOUSE == 3:
            MONEYP3 -= LASTBETP3
        GAME_STATE_PLAYER3 = 6

# Funtion to know if a player need to bet


def poorPlayer():
    global GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, MONEYP1, MONEYP2, MONEYP3
    if MONEYP1 == 0:
        GAME_STATE_PLAYER1 = 9
        return GAME_STATE_PLAYER1
    if MONEYP2 == 0:
        GAME_STATE_PLAYER2 = 9
        return GAME_STATE_PLAYER2
    if MONEYP3 == 0:
        GAME_STATE_PLAYER3 = 9
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
                if (player == PLAYER1):
                    GAME_STATE_PLAYER1 = 0
                elif (player == PLAYER2):
                    GAME_STATE_PLAYER2 = 0
                elif (player == PLAYER3):
                    GAME_STATE_PLAYER3 = 0

        if sum(player) == 21:
            if (player == PLAYER1):
                GAME_STATE_PLAYER1 = 4
            elif (player == PLAYER2):
                GAME_STATE_PLAYER2 = 4
            elif (player == PLAYER3):
                GAME_STATE_PLAYER3 = 4

        i = len(player) - 1
        if player[i] == 10:
            if (player == PLAYER1):
                NAMECARD1.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER2):
                NAMECARD2.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER3):
                NAMECARD3.append(random.choice(["Jota", "Reina", "Rey"]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        elif player[i] == 11 or player[i] == 1:
            if (player == PLAYER1):
                NAMECARD1.append(
                    "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER2):
                NAMECARD2.append(
                    "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER3):
                NAMECARD3.append(
                    "As_de_" + random.choice(["Corazones", "Diamantes", "Espadas", "Tréboles"]))
        else:
            if (player == PLAYER1):
                NAMECARD1.append(str(player[i]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER2):
                NAMECARD2.append(str(player[i]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))
            elif (player == PLAYER3):
                NAMECARD3.append(str(player[i]) + "_de_" + random.choice(
                    ["Corazones", "Diamantes", "Espadas", "Tréboles"]))

# Funtions to pass the turn of each player


def passTurnP1():
    return GAME_STATE_PLAYER1 == 5


def passTurnP2():
    return GAME_STATE_PLAYER2 == 5


def passTurnP3():
    return GAME_STATE_PLAYER3 == 5

# Funtion to know if a player has blackjack


def blackjack(player):
    return sum(player) == 21

# Funtion to bet for each player


def bet(amount):
    global MONEYP1, MONEYP2, MONEYP3, GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, LASTBETP1, LASTBETP2, LASTBETP3
    if GAME_STATE_PLAYER1 == 7:
        MONEYP1 -= amount
        GAME_STATE_PLAYER1 = 1
        GAME_STATE_PLAYER2 = 7
        LASTBETP1 += amount
        return MONEYP1, GAME_STATE_PLAYER1, LASTBETP1
    elif GAME_STATE_PLAYER2 == 7:
        MONEYP2 -= amount
        GAME_STATE_PLAYER2 = 1
        GAME_STATE_PLAYER3 = 7
        LASTBETP2 += amount
        return MONEYP2, GAME_STATE_PLAYER2, LASTBETP2
    elif GAME_STATE_PLAYER3 == 7:
        MONEYP3 -= amount
        GAME_STATE_PLAYER3 = 1
        LASTBETP3 += amount
        return MONEYP3, GAME_STATE_PLAYER3, LASTBETP3


# Game logic
def logic():
    global GAME_STATE_HOUSE, GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, PLAYER1, PLAYER2, PLAYER3, HOUSE, INSURANCEBET
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
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
        if sum(HOUSE) < 17:
            firstPlay = 1
            HOUSE.append((random.choice(numbers)))
            # This is to change the value of the card 11 to 1. Only if the player or house has two 11 cards
            if HOUSE.count(11) == 2:
                HOUSE.remove(11)
                HOUSE.append(1)
        if sum(HOUSE) > 21 and HOUSE.count(11) == 1:
            HOUSE.remove(11)
            HOUSE.append(1)
        if sum(HOUSE) > 21 and HOUSE.count(11) == 0:
            GAME_STATE_HOUSE = 0
        if sum(HOUSE) > 16 and sum(HOUSE) < 22:
            GAME_STATE_HOUSE = 4
        if firstPlay == 0 and sum(HOUSE) == 21:
            GAME_STATE_HOUSE = 3
            firstPlay = 1
        if HOUSE[0] == 11 or HOUSE[0] == 1:
            INSURANCEBET = 1

    drawCards()

# ------------------------------ LOAD CARD IMAGES AND DRAW IT ------------------------------

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

# Function to load the images


def loadImages():
    images = {}
    for filename in os.listdir("images/cards"):
        path = os.path.join("images/cards", filename)
        if os.path.isfile(path):
            images[os.path.splitext(filename)[0]] = pygame.image.load(path)
    return images


IMAGES = loadImages()

# Funtion to draw the cards


def drawCardsDisplay():
    global PLAYER1, PLAYER2, PLAYER3, HOUSE, NAMECARD1, NAMECARD2, NAMECARD3, NAMECARDHOUSE, BARAJA

    # Draw PLAYER1 cards
    for i, card_name in enumerate(NAMECARD1):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER1_IMAGE_POS[0] +
                        i * 20, PLAYER1_IMAGE_POS[1] - (i + 3.5) * (50))
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Draw PLAYER2 cards
    for i, card_name in enumerate(NAMECARD2):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER2_IMAGE_POS[0] +
                        i * 20, PLAYER2_IMAGE_POS[1] - (i + 3.5) * (50))
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Draw PLAYER3 cards
    for i, card_name in enumerate(NAMECARD3):
        card_image = IMAGES.get(card_name)
        if card_image:
            card_image = resizeCards(card_image)
            card_pos = (PLAYER3_IMAGE_POS[0] +
                        i * 20, PLAYER3_IMAGE_POS[1] - (i + 3.5) * (50))
            screen.blit(card_image, card_pos)
        else:
            print(f"Imagen no encontrada: {card_name}")

    # Draw only 1 card
    for i in range(1):
        card_image = IMAGES.get(NAMECARDHOUSE[0])
        baraja = IMAGES.get('baraja')
        if (card_image):
            card_image = resizeCards(card_image)
            baraja = resizeCards(baraja)
            card_pos = (470 + 1 * 80, 135)
            screen.blit(card_image, card_pos)
            screen.blit(baraja, (470 + 2 * 80, 135))

# Function to draw the cards of the house


def drawCardsHouse():
    global HOUSE, NAMECARDHOUSE
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

# Funtion to restart the game


def restart():
    global PLAYER1, PLAYER2, PLAYER3, HOUSE, NAMECARD1, NAMECARD2, NAMECARD3, NAMECARDHOUSE, GAME_STATE_HOUSE, GAME_STATE_PLAYER1, GAME_STATE_PLAYER2, GAME_STATE_PLAYER3, LASTBETP1, LASTBETP2, LASTBETP3, MONEYP1, MONEYP2, MONEYP3
    global PAYP1, PAYP2, PAYP3, INSURANCEBET
    PLAYER1 = []
    PLAYER2 = []
    PLAYER3 = []
    HOUSE = []

    NAMECARD1 = []
    NAMECARD2 = []
    NAMECARD3 = []
    NAMECARDHOUSE = []

    GAME_STATE_HOUSE = 1
    GAME_STATE_PLAYER1 = 7
    GAME_STATE_PLAYER2 = 8
    GAME_STATE_PLAYER3 = 8

    LASTBETP1 = 0
    LASTBETP2 = 0
    LASTBETP3 = 0

    PAYP1 = 0
    PAYP2 = 0
    PAYP3 = 0

    INSURANCEBET = 0

    logic()


# Run the game
logic()
pgzrun.go()
