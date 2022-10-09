import pygame
import time
import random


def fade_out(dis):
    fade_start = time.time()
    fade_c = 235
    bg_c = (fade_c, fade_c, fade_c)
    while time.time() - fade_start < 0.5:
        dis.fill(bg_c)
        fade_c = 235 * (1 - 2 * (time.time() - fade_start))
        bg_c = (fade_c, fade_c, fade_c)
        pygame.display.update()


def get_entry_text(msg, fontsize):
    """
    Forms a rendered version of a message
    :param msg:
    :param fontsize:
    :return: None
    """
    textfont = pygame.font.SysFont('Comic Sans MS', fontsize)
    return textfont.render(msg, False, (0, 0, 0))