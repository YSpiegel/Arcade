import pygame
import math
import random

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("BrickBreak by YS")
dis.set_colorkey((0, 255, 0))

pygame.font.init()


def game():
    game_over = False




    while not game_over:

