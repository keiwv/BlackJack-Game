import cImages, cTable, cPlayer
import pygame
import pgzrun

images = cImages.Images()

def draw():
    screen.clear()
    screen.blit(images.background.image, (0, 0)) 

pgzrun.go()
