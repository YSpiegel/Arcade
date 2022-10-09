import pygame
import time
import random
black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (235, 235, 235)
light_blue = (200, 200, 255)


class player():
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

