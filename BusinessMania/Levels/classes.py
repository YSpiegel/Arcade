import pygame
import time
import random
black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (235, 235, 235)
light_blue = (200, 200, 255)


class player:
    def __init__(self, dis):
        self.pos = [300, 200]
        self.xt = time.time()
        self.xv = 0
        self.x0 = self.pos[0]
        self.yt = time.time()
        self.yv0 = 0
        self.ya = 100
        self.y0 = self.pos[1]

        self.falling = True
        self.jumping = False
        self.can_move_right = True
        self.can_move_left = True

        self.dis = dis

    def change_x_movement(self, xv_mod):
        self.xv = xv_mod
        self.xt = time.time()
        self.x0 = self.pos[0]

    def change_y_movement(self, yv0_mod):
        self.yv0 = yv0_mod
        self.ya = 100
        self.yt = time.time()
        self.y0 = self.pos[1]

    def hitbox(self):
        return [[self.pos[0] - 5, self.pos[0] + 5], [self.pos[1] - 5, self.pos[1] + 20]]

    def x_dt(self):
        return time.time() - self.xt

    def y_dt(self):
        return time.time() - self.yt

    def draw(self):
        pygame.draw.circle(self.dis, black, self.pos, 5)
        pygame.draw.rect(self.dis, black, [self.pos[0] - 3, self.pos[1] + 5, 6, 15])
        pygame.draw.polygon(self.dis, white, [[self.pos[0] - 3, self.pos[1] + 6], [self.pos[0] + 3, self.pos[1] + 6],
                                         [self.pos[0], self.pos[1] + 10]])
        pygame.draw.rect(self.dis, black, [self.pos[0] - 5, self.pos[1] - 5, 10, 2])
        pygame.draw.circle(self.dis,black, [self.pos[0], self.pos[1] - 5], 3)

    def current_speed(self):
        return self.yv0 + self.y_dt() * self.ya * 4


class obstacle:

    def __init__(self, rect, dis):
        self.rect = rect
        self.hitbox = [[rect[0], rect[0] + rect[2]], [rect[1], rect[1] + rect[3]]]
        self.dis = dis

    def draw(self):
        pygame.draw.rect(self.dis, black, self.rect)


class paperwork:

    def __init__(self, pos, dis):
        self.rect = [pos[0], pos[1], 20, 30]
        self.hitbox = [[self.rect[0], self.rect[0] + self.rect[2]], [self.rect[1], self.rect[1] + self.rect[3]]]
        self.dis = dis

    def draw(self):
        pygame.draw.rect(self.dis, light_blue, self.rect, width=2)
        for x in range(6):
            pygame.draw.line(self.dis, light_blue, [self.rect[0] + 5, self.rect[1] + 4 * x],
                             [self.rect[0] + self.rect[2] - 5, self.rect[1] + 4 * x])