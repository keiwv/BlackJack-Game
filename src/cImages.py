import pygame
import pgzrun
import os

class Images:
    def __init__(self):
        reloadButton = Actor("./images/reload.png", pos=(1180,118))
        chip25 = Actor("./images/chips/ficha25.png", pos=(60,200))
        chip50 = Actor("./images/chips/ficha50.png", pos=(60, 280))
        chip100 = Actor("./images/chips/ficha100.png", pos=(60, 360))
        chip500 = Actor("./images/chips/ficha500.png", pos=(60, 440))
        background = Actor("./images/background/blackjack_fondo.png")
