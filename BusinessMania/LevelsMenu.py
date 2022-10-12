import pygame
import time
import lib
from Levels import Lvl1, Lvl2, Lvl3, Lvl4, Lvl5, Lvl6

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("BusinessMania by YoavSpiegel")
pygame.font.init()

black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (235, 235, 235)
mid_gray = (120, 120, 120)
dark_gray = (50, 50, 50)
green = (0, 200, 0)


def open(levels):

    back = False
    lib.fade_out(dis)
    start_time = time.time()

    level_boxes = [[5 + (i % 10) * 60, 150 + (i // 10) * 100, 50, 50] for i, level in enumerate(levels)]

    level_code = {1: Lvl1, 2: Lvl2, 3: Lvl3, 4: Lvl4, 5: Lvl5, 6: Lvl6}

    while not back:
        playable = [levels[:i].count(True) > i - 3 if i >= 3 else True for i, level in enumerate(levels)]

        delta_start = time.time() - start_time
        fade_color = 235 * delta_start
        bg_color = (0, 0, 0)
        if delta_start < 1:
            bg_color = (fade_color, fade_color, fade_color)
        else:
            bg_color = light_gray
        dis.fill(bg_color)

        dis.blit(lib.get_entry_text("Levels:", 50), [225, 20])

        for i, level in enumerate(levels):
            pygame.draw.rect(dis, green if level else mid_gray, level_boxes[i])

            if i < 9:
                dis.blit(lib.get_entry_text(str(i + 1), 30), [20 + (i % 10) * 60, 155 + (i // 10) * 100])
            else:
                dis.blit(lib.get_entry_text(str(i + 1), 30), [12 + (i % 10) * 60, 155 + (i // 10) * 100])

            if not playable[i]:
                pygame.draw.line(dis, black, [level_boxes[i][0], level_boxes[i][1]],
                                 [level_boxes[i][0] + level_boxes[i][2], level_boxes[i][1] + level_boxes[i][3]])

        pygame.draw.rect(dis, black, [170, 470, 260, 50], width=4)
        dis.blit(lib.get_entry_text("Back to main menu", 25), [190, 475])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                back = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if lib.mouse_in_box([170, 470, 260, 50]):
                    back = True
                for i, level in enumerate(levels):
                    if playable[i] and lib.mouse_in_box(level_boxes[i]):
                        levels[i] = level_code[i+1].run_level(levels[i])

        pygame.display.update()

    lib.fade_out(dis)

    return levels


if __name__ == "__main__":
    open([False for _ in range(30)])
