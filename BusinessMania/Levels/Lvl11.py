import pygame
import time
import random
import classes
import functions

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("BusinessMania by YS")
dis.set_colorkey((255, 255, 255))
black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (235, 235, 235)
mid_gray = (120, 120, 120)
dark_gray = (50, 50, 50)
pygame.font.init()

obs_list = [[0, 580, 600, 20], [0, 0, 600, 20], [0, 0, 20, 600], [580, 0, 20, 600], [295, 300, 10, 300],

            [220, 540, 10, 40], [180, 540, 40, 10], [180, 500, 10, 40], [140, 500, 40, 10], [140, 460, 10, 40],
            [100, 460, 40, 10], [100, 420, 10, 40], [60, 420, 40, 10], [60, 380, 10, 40], [20, 380, 40, 10],

            [380, 540, 10, 40], [390, 540, 40, 10], [420, 500, 10, 40], [430, 500, 40, 10], [460, 460, 10, 40],
            [470, 460, 40, 10], [500, 420, 10, 40], [500, 420, 50, 10], [540, 380, 10, 40], [540, 380, 50, 10],

            [80, 240, 10, 40], [90, 240, 40, 10], [120, 200, 10, 40], [130, 200, 40, 10], [160, 160, 10, 40],
            [170, 160, 40, 10], [200, 120, 10, 40], [210, 120, 180, 10], [510, 240, 10, 40], [470, 240, 50, 10],
            [470, 200, 10, 40], [430, 200, 40, 10], [430, 160, 10, 40], [390, 160, 40, 10], [390, 120, 10, 40]
            ]

paperwork = classes.paperwork([325, 540], dis)

trampoline_list = [[25, 370, 30, 10]]

trampolines = [classes.trampoline(rect, dis) for rect in trampoline_list]

obs_list += [[rect[0] - 10, rect[1] + rect[3], rect[2] + 20, 10] for rect in trampoline_list]

obstacles = [classes.obstacle(rect, dis) for rect in obs_list]


def run_level(passed_before):
    player = classes.player(dis, [275, 500])

    game_over = False

    while not game_over:

        dis.fill(light_gray)

        y_delta_time = player.y_dt() * 4

        player.falling = True
        player.can_move_right = True
        player.can_move_left = True

        for obs in obstacles:

            if functions.in_vertically(player.hitbox(), obs.hitbox):
                if functions.vertical_collusion(player.hitbox(), obs.hitbox) == obs.hitbox:
                    if player.jumping:
                        player.change_y_movement(10)
                elif functions.vertical_collusion(player.hitbox(), obs.hitbox) == player.hitbox():
                    if not player.jumping or (player.jumping and player.current_speed() == 0):
                        player.change_y_movement(0)
                        player.falling = False
                        player.jumping = False
            else:
                if functions.horizontal_collusion(player.hitbox(), obs.hitbox) == obs.hitbox:
                    player.can_move_left = False
                    if player.xv < 0:
                        player.xt = time.time()
                        player.x0 = player.pos[0]
                if functions.horizontal_collusion(player.hitbox(), obs.hitbox) == player.hitbox():
                    player.can_move_right = False
                    if player.xv > 0:
                        player.xt = time.time()
                        player.x0 = player.pos[0]

        for tramp in trampolines:

            if functions.in_vertically(player.hitbox(), tramp.hitbox):
                if functions.vertical_collusion(player.hitbox(), tramp.hitbox) == tramp.hitbox:
                    if player.jumping:
                        player.change_y_movement(10)
                elif functions.vertical_collusion(player.hitbox(), tramp.hitbox) == player.hitbox():
                    if not player.jumping or (player.jumping and player.current_speed() == 0):
                        if tramp.static:
                            tramp.impact()
                        player.change_y_movement(-200)
                        player.falling = False
                        player.jumping = True
            else:
                if functions.horizontal_collusion(player.hitbox(), tramp.hitbox) == tramp.hitbox:
                    player.can_move_left = False
                    if player.xv < 0:
                        player.xt = time.time()
                        player.x0 = player.pos[0]
                if functions.horizontal_collusion(player.hitbox(), tramp.hitbox) == player.hitbox():
                    player.can_move_right = False
                    if player.xv > 0:
                        player.xt = time.time()
                        player.x0 = player.pos[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if functions.mouse_in_box([510, 30, 60, 30]):
                    return run_level(passed_before)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not player.falling:
                    player.jumping = True
                    player.change_y_movement(-100)
                if event.key == pygame.K_d:
                    player.change_x_movement(100)
                if event.key == pygame.K_a:
                    player.change_x_movement(-100)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    player.change_x_movement(0)
                if event.key == pygame.K_a:
                    player.change_x_movement(0)

        if player.jumping and player.current_speed() > 0:
            player.jumping = False
            player.falling = True

        if player.falling or player.jumping:
            player.pos[1] = player.y0 + player.yv0 * y_delta_time + 0.5 * player.ya * (y_delta_time ** 2)

        if 0 <= player.pos[0] <= 600:
            if (player.xv > 0 and player.can_move_right) or (player.xv < 0 and player.can_move_left):
                player.pos[0] = player.x0 + player.xv * player.x_dt()

        if functions.horizontal_collusion(player.hitbox(), paperwork.hitbox) != 0 and \
            functions.vertical_collusion(player.hitbox(), paperwork.hitbox) != 0:
            return True

        player.draw()
        for obs in obstacles:
            obs.draw()
        for tramp in trampolines:
            tramp.update()
        paperwork.draw()

        pygame.draw.rect(dis, black, [510, 30, 60, 30], width=3)
        dis.blit(functions.get_entry_text("Restart", 14), [515, 35])

        pygame.display.update()
    return passed_before


if __name__ == "__main__":
    run_level(False)