import pygame
import Pong
import BrickBreak
import PixelSentry

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Arcade by YS")
dis.set_colorkey((255, 255, 255))

pygame.font.init()


def empty_rect(coords, length, height, thickness):
    """
    Creates a rectangular frame
    :param coords: positions for the rectangle
    :param length:
    :param height:
    :param thickness: of the frame
    :return: None
    """
    pygame.draw.rect(dis, (0, 0, 0), [coords[0], coords[1], length, height])
    pygame.draw.rect(dis, (255, 255, 255),
                     [coords[0] + thickness, coords[1] + thickness, length - 2 * thickness, height - 2 * thickness])


def button(coords, length, height, thickness, msg):
    """
    Set a frame and add the fitting text
    :param coords: x and y of the top left corner
    :param length:
    :param height:
    :param thickness: of the frame
    :param msg: to be presented on the button
    :return: None
    """
    empty_rect(coords, length, height, thickness)
    dis.blit(get_entry_text(msg, 30), (coords[0] + 10, coords[1] + 10))


def get_entry_text(msg, fontsize):
    """
    Forms a rendered version of a message
    :param msg:
    :param fontsize:
    :return: None
    """
    textfont = pygame.font.SysFont('Comic Sans MS', fontsize)
    return textfont.render(msg, False, (0, 0, 0))


def mainscreen():
    quit = False

    while not quit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # activate buttons
                if 100 <= x <= 500:
                    if 100 <= y <= 175:
                        PixelSentry.game()
                    if 200 <= y <= 275:
                        BrickBreak.game()
                    if 300 <= y <= 375:
                        Pong.game()
                    if 250 <= x <= 350 and 400 <= y <= 475:
                        quit = True

        dis.fill((255, 255, 255))

        dis.blit(get_entry_text("Welcome to the Arcade!", 50), (17, 5))

        # create buttons
        button([100, 100], 400, 75, 5, "Click here for PixelSentry")
        button([100, 200], 400, 75, 5, "Click here for BrickBreak")
        button([100, 300], 400, 75, 5, "Click here for Pong")
        button([250, 400], 100, 75, 3, "Quit")

        pygame.display.update()


mainscreen()
