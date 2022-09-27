import pygame
import random
import math
import time
import numpy

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("PixelSentry by YS")
dis.set_colorkey((255, 0, 0))

pygame.font.init()
black = (0, 0, 0)


def get_entry_text(msg, fontsize):
    """
    Forms a rendered version of a message
    :param msg:
    :param fontsize:
    :return: None
    """
    textfont = pygame.font.SysFont('Comic Sans MS', fontsize)
    return textfont.render(msg, False, (0, 0, 0))


def get_angle(pos1, pos2):
    """
    Calculate the angle between two positions
    :param pos1: first input position
    :param pos2: second input position
    :return: angle between pos1 and pos2
    """
    x1, y1, x2, y2 = pos1[0], pos1[1], pos2[0], pos2[1]
    if x2 != x1:
        angle = math.atan(- (y2 - y1) / (x2 - x1))
    else:
        if pos2[1] > pos1[1]:
            return 3 * math.pi / 2
        else:
            return math.pi / 2

    if pos2[0] > pos1[0]:
        return angle
    else:
        return math.pi + angle


def end_of_round():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return True
                if event.key == pygame.K_r:
                    return False

        dis.blit(get_entry_text("Click q to quit or r for another round", 30), [10, 500])

        pygame.display.update()


def pixels_in_sight(pixels):
    for pixel in pixels:
        angle = pixel[0]
        radius = pixel[1]
        if -10 <= 300 + radius * math.cos(angle) <= 610 and -10 <= 300 - radius * math.sin(angle) <= 610:
            return True
    return False


def game():
    game_over = False

    # sentry properties
    sentry_angle = math.pi / 2

    # pixels properties
    pixels = []
    total_pixels = 0
    last_attack = time.time()

    # shots properties
    shots = []

    score = 0

    def pixel_scatter():
        while pixels_in_sight(pixels):
            dis.fill((255, 0, 0))

            dis.blit(get_entry_text(f"Score: {score}", 30), [250, 10])

            # create sentry
            pygame.draw.circle(dis, black, [300, 300], 10)
            for x in range(8):
                pygame.draw.circle(dis, black,
                                   [300 + (10 + 2 * x) * math.cos(sentry_angle),
                                    300 - (10 + 2 * x) * math.sin(sentry_angle)], 2)
            for pixel in pixels:
                angle = pixel[0]
                radius = pixel[1]
                pygame.draw.rect(dis, black, [300 + radius * math.cos(angle), 300 - radius * math.sin(angle), 10, 10])
                pixel[1] += 0.5

            pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(shots) == 0 or shots[-1][1] > 12:
                    shots.append([sentry_angle, 16])

        # set sentry angle to mouse position
        if len(shots) == 0 or shots[-1][1] > 12:
            sentry_angle = get_angle([300, 300], pygame.mouse.get_pos())

        # shoot a pixel if time has passed
        if time.time() - last_attack > 0.1 + 1 / (0.03 * total_pixels + 0.5) + random.random():
            pixels.append([random.choice(numpy.arange(math.pi * 5 / 8, math.pi * 2 + math.pi * 3 / 8, math.pi / 32)),
                           300])
            last_attack = time.time()
            total_pixels += 1

        dis.fill((255, 0, 0))

        end_round = False

        # create pixels
        for pixel in pixels:
            angle = pixel[0]
            radius = pixel[1]
            topx = 300 + radius * math.cos(angle)
            topy = 300 - radius * math.sin(angle)
            bottomx = 310 + radius * math.cos(angle)
            bottomy = 310 - radius * math.sin(angle)
            pygame.draw.rect(dis, black, [300 + radius * math.cos(angle), 300 - radius * math.sin(angle), 10, 10])
            pixel[1] -= 0.05 + 0.002 * total_pixels / 10
            for shot in shots:
                if topx <= 300 + shot[1] * math.cos(shot[0]) <= bottomx \
                        and topy <= 300 - shot[1] * math.sin(shot[0]) <= bottomy and pixel in pixels:
                        pixels.remove(pixel)
                        shots.remove(shot)
                        score += 1

            if radius <= 4:
                end_round = True

        dis.blit(get_entry_text(f"Score: {score}", 30), [250, 10])

        # create sentry
        pygame.draw.circle(dis, black, [300, 300], 10)
        for x in range(8):
            pygame.draw.circle(dis, black,
                               [300 + (10 + 2 * x) * math.cos(sentry_angle),
                                300 - (10 + 2 * x) * math.sin(sentry_angle)], 2)

        if end_round:
            pixel_scatter()
            game_over = end_of_round()

            # sentry properties
            sentry_angle = math.pi / 2

            # pixels properties
            pixels = []
            last_attack = time.time()

            # shots properties
            shots = []

            score = 0

        # create shots
        for shot in shots:
            angle = shot[0]
            radius = shot[1]
            for x in range(1, 8):
                pygame.draw.circle(dis, black,
                                   [300 + (radius + 2 * x) * math.cos(angle), 300 - (radius + 2 * x) * math.sin(angle)],
                                   1)
            shot[1] += 0.2
            if shot[1] > 300:
                shots.remove(shot)

        pygame.display.update()


if __name__ == '__main__':
    game()
