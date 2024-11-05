import pygame
from pgzero.actor import Actor
import os

class Images:
    def __init__(self):
        self.reloadButton = Actor("./images/reload.png", pos=(1180,118))
        self.chip25 = Actor("./images/chips/ficha25.png", pos=(60,200))
        self.chip50 = Actor("./images/chips/ficha50.png", pos=(60, 280))
        self.chip100 = Actor("./images/chips/ficha100.png", pos=(60, 360))
        self.chip500 = Actor("./images/chips/ficha500.png", pos=(60, 440))
        self.background = Actor("./images/background/blackjack_fondo.png")
