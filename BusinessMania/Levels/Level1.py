import pygame
import time
import random
import classes

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("ControllerGame by YS")
dis.set_colorkey((255, 255, 255))
black = (0, 0, 0)
white = (255, 255, 255)
light_gray = (235, 235, 235)
light_blue = (200, 200, 255)
pygame.font.init()

game_over = False


def in_vertically(hitbox1, hitbox2):
    return hitbox2[0][0] - 5 <= hitbox1[0][0] < hitbox1[0][1] <= hitbox2[0][1] + 5


def vertical_collusion(hitbox1, hitbox2):
    """
    Checks for a collusion
    :param hitbox1:
    :param hitbox2:
    :return: The higher hitbox or none if there's no collusion
    """

    if hitbox1[0][0] <= hitbox2[0][0] <= hitbox1[0][1] or hitbox2[0][0] <= hitbox1[0][0] <= hitbox2[0][1]:
        if hitbox1[1][0] <= hitbox2[1][0] <= hitbox1[1][1]:
            return hitbox1
        if hitbox2[1][0] <= hitbox1[1][0] <= hitbox2[1][1]:
            return hitbox2
    return 0


def horizontal_collusion(hitbox1, hitbox2):
    """
        Checks for a collusion
        :param hitbox1:
        :param hitbox2:
        :return: The left hitbox or none if there's no collusion
        """

    if hitbox1[1][0] <= hitbox2[1][0] + 1 <= hitbox1[1][1] or hitbox2[1][0] <= hitbox1[1][0] + 1 <= hitbox2[1][1]:
        if hitbox1[0][0] <= hitbox2[0][0] <= hitbox1[0][1]:
            return hitbox1
        if hitbox2[0][0] <= hitbox1[0][0] <= hitbox2[0][1]:
            return hitbox2
    return 0


player = classes.player(dis)

obstacles = [classes.obstacle([0, 580, 600, 20], dis), classes.obstacle([0, 0, 600, 20], dis),
             classes.obstacle([0, 0, 20, 600], dis), classes.obstacle([580, 0, 20, 600], dis),

             classes.obstacle([280, 320, 40, 10], dis), classes.obstacle([310, 220, 10, 100], dis),
             classes.obstacle([280, 280, 10, 40], dis), classes.obstacle([220, 280, 60, 10], dis),
             classes.obstacle([170, 220, 10, 200], dis), classes.obstacle([170, 420, 100, 10], dis),
             classes.obstacle([270, 380, 10, 50], dis), classes.obstacle([280, 380, 50, 10], dis),
             classes.obstacle([170, 220, 120, 10], dis), classes.obstacle([330, 380, 10, 50], dis),
             classes.obstacle([330, 420, 50, 10], dis), classes.obstacle([380, 420, 10, 50], dis),
             classes.obstacle([380, 460, 50, 10], dis), classes.obstacle([430, 460, 10, 50], dis),
             classes.obstacle([430, 500, 50, 10], dis), classes.obstacle([480, 500, 10, 50], dis),
             classes.obstacle([480, 540, 50, 10], dis), classes.obstacle([530, 540, 10, 50], dis)]

program_start = time.time()

paperwork = classes.paperwork([550, 550], dis)

while not game_over:

    dis.fill(light_gray)

    y_delta_time = player.y_dt() * 4

    player.falling = True
    player.can_move_right = True
    player.can_move_left = True

    for obs in obstacles:

        if in_vertically(player.hitbox(), obs.hitbox):
            if vertical_collusion(player.hitbox(), obs.hitbox) == obs.hitbox:
                if player.jumping:
                    player.change_y_movement(10)
            elif vertical_collusion(player.hitbox(), obs.hitbox) == player.hitbox():
                if not player.jumping or (player.jumping and player.current_speed() == 0):
                    player.change_y_movement(0)
                    player.falling = False
                    player.jumping = False
        else:
            if horizontal_collusion(player.hitbox(), obs.hitbox) == obs.hitbox:
                player.can_move_left = False
                if player.xv < 0:
                    player.xt = time.time()
                    player.x0 = player.pos[0]
            if horizontal_collusion(player.hitbox(), obs.hitbox) == player.hitbox():
                player.can_move_right = False
                if player.xv > 0:
                    player.xt = time.time()
                    player.x0 = player.pos[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
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

    if horizontal_collusion(player.hitbox(), paperwork.hitbox) != 0 and \
        vertical_collusion(player.hitbox(), paperwork.hitbox) != 0:
        game_over = True

    player.draw()
    for obs in obstacles:
        obs.draw()
    paperwork.draw()

    pygame.display.update()
