import pygame
import time
import random
black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (235, 235, 235)
light_blue = (200, 200, 255)


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


def mouse_in_box(box):
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    return box[0] <= mouse_x <= box[0] + box[2] and box[1] <= mouse_y <= box[1] + box[3]

