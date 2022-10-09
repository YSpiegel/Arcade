import pygame
import time
import func

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
    func.fade_out(dis)
    start_time = time.time()

    level_boxes = [[5 + (i % 10) * 60, 150 + (i // 10) * 100, 50, 50] for i, level in enumerate(levels)]

    while not back:

        delta_start = time.time() - start_time
        fade_color = 235 * delta_start
        bg_color = (0, 0, 0)
        if delta_start < 1:
            bg_color = (fade_color, fade_color, fade_color)
        else:
            bg_color = light_gray
        dis.fill(bg_color)

        dis.blit(func.get_entry_text("Levels:", 50), [225, 20])

        for i, level in enumerate(levels):
            pygame.draw.rect(dis, green if level else mid_gray, level_boxes[i])

            if i < 9:
                dis.blit(func.get_entry_text(str(i + 1), 30), [20 + (i % 10) * 60, 155 + (i // 10) * 100])
            else:
                dis.blit(func.get_entry_text(str(i + 1), 30), [12 + (i % 10) * 60, 155 + (i // 10) * 100])

        pygame.draw.rect(dis, black, [170, 470, 260, 50], width=4)
        dis.blit(func.get_entry_text("Back to main menu", 25), [190, 475])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                back = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if func.mouse_in_box([170, 470, 260, 50]):
                    back = True
                for i, level in enumerate(levels):
                    if func.mouse_in_box(level_boxes[i]):
                        levels[i] = True

        pygame.display.update()

    func.fade_out(dis)

    return levels


if __name__ == "__main__":
    open([False for _ in range(30)])
