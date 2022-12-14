import pygame
import time
import random
import lib
import LevelsMenu

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("BusinessMania by YoavSpiegel")
pygame.font.init()
black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (235, 235, 235)
mid_gray = (120, 120, 120)
dark_gray = (50, 50, 50)


game_over = False
start_time = time.time()


def draw_building():
    pygame.draw.polygon(dis, black, [[100, 450], [200, 400], [200, 200], [100, 250]])
    pygame.draw.polygon(dis, dark_gray if bg_color[0] > dark_gray[0] else bg_color,
                        [[100, 450], [50, 400], [50, 200], [100, 250]])
    pygame.draw.polygon(dis, mid_gray if bg_color[0] > mid_gray[0] else bg_color,
                        [[50, 200], [100, 250], [200, 200], [150, 150]])
    pygame.draw.polygon(dis, bg_color, [[150, 425], [150, 400], [170, 390], [170, 415]])
    for x in range(3):
        for y in range(260, 400, 30):
            pygame.draw.polygon(dis, bg_color, [[112 + 35 * x, y - 17 * x], [112 + 35 * x, y + 15 - 17 * x],
                                                [122 + 35 * x, y - 17 * x + 10], [122 + 35 * x, y - 5 - 17 * x]])


def credits():
    lib.fade_out(dis)

    texts = [lib.get_entry_text("All rights reserved", 30), lib.get_entry_text("Levels: Yoav Spiegel", 30),
             lib.get_entry_text("Screens: Yoav Spiegel", 30), lib.get_entry_text("Creative: Yoav Spiegel", 30),
             lib.get_entry_text("Design: Yoav Spiegel", 30), lib.get_entry_text("Coding: Yoav Spiegel", 30),
             lib.get_entry_text("Director: Yoav Spiegel", 30)]


    # fade in
    fade_start = time.time()
    fade_c = 235
    bg_c = (fade_c, fade_c, fade_c)
    while time.time() - fade_start < 0.5:
        dis.fill(bg_c)
        draw_building()
        fade_c = 235 * 2 * (time.time() - fade_start)
        bg_c = (fade_c, fade_c, fade_c)
        pygame.display.update()

    cred_start = time.time()
    cred_pos = -775
    while cred_pos < 600:
        dis.fill(bg_c)

        draw_building()

        for i, text in enumerate(texts):
            dis.blit(text, [250, cred_pos + 120 * i])

        delta_cred = time.time() - cred_start
        cred_pos += delta_cred / 40

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cred_pos = 600

    lib.fade_out(dis)


class character:
    def __init__(self, pos):
        self.pos = pos
        self.speed_mod = 100
        self.t0 = time.time()
        self.x0 = pos[0]

    def draw(self):
        pygame.draw.circle(dis, black, self.pos, 5)
        pygame.draw.rect(dis, black, [self.pos[0] - 3, self.pos[1] + 5, 6, 15])
        pygame.draw.polygon(dis, white, [[self.pos[0] - 3, self.pos[1] + 6], [self.pos[0] + 3, self.pos[1] + 6],
                                         [self.pos[0], self.pos[1] + 10]])
        pygame.draw.rect(dis, black, [self.pos[0] - 5, self.pos[1] - 5, 10, 2])
        pygame.draw.circle(dis, black, [self.pos[0], self.pos[1] - 5], 3)


characters = [character([300 + 290 * (random.randrange(1, 4, 2) - 2), y + 5 * (random.randrange(1, 4, 2) - 2)])
              for y in range(480, 580, 5)]
char_update = time.time()

levels = [False for _ in range(30)]

while not game_over:
    delta_start = time.time() - start_time
    fade_color = 235 * delta_start
    bg_color = (0, 0, 0)
    if delta_start < 1:
        bg_color = (fade_color, fade_color, fade_color)
    else:
        bg_color = light_gray
    dis.fill(bg_color)

    dis.blit(lib.get_entry_text("BusinessMania!", 60), [20, 20])
    dis.blit(lib.get_entry_text("By Yoav Spiegel", 20), [440, 65])

    # draw building
    draw_building()

    # draw characters

    delta_char = time.time() - char_update
    for char in characters:
        if delta_char > 0.5:
            if random.random() > 0.5:
                char.speed_mod *= -1
            char_update = time.time()
            char.x0 = char.pos[0]
            char.t0 = char_update
        char.pos[0] = char.x0 + delta_char * char.speed_mod
        char.draw()
        if char.pos[0] < -100 or char.pos[0] > 700:
            characters.remove(char)

    # draw buttons

    pygame.draw.rect(dis, black, [300, 150, 200, 50], width=4)
    dis.blit(lib.get_entry_text("Play", 35), [370, 150])
    pygame.draw.rect(dis, black, [300, 250, 200, 50], width=4)
    dis.blit(lib.get_entry_text("Credits", 35), [340, 250])
    pygame.draw.rect(dis, black, [300, 350, 200, 50], width=4)
    dis.blit(lib.get_entry_text("Quit", 35), [360, 350])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if lib.mouse_in_box([300, 150, 200, 50]):
                levels = LevelsMenu.open(levels)
            if lib.mouse_in_box([300, 250, 200, 50]):
                credits()
            if lib.mouse_in_box([300, 350, 200, 50]):
                game_over = True
                lib.fade_out(dis)

    pygame.display.update()
