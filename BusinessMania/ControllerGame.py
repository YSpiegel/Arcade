import pygame
import time
import random

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("ControllerGame by YS")
dis.set_colorkey((255, 255, 255))
black = (0, 0, 0)
white = (255, 255, 255)
pygame.font.init()

game_over = False


def get_entry_text(msg, fontsize):
    """
    Forms a rendered version of a message
    :param msg:
    :param fontsize:
    :return: None
    """
    textfont = pygame.font.SysFont('Comic Sans MS', fontsize)
    return textfont.render(msg, False, (0, 0, 0))


class player:
    def __init__(self):
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
        pygame.draw.circle(dis, black, self.pos, 5)
        pygame.draw.rect(dis, black, [self.pos[0] - 3, self.pos[1] + 5, 6, 15])

    def current_speed(self):
        return self.yv0 + self.y_dt() * self.ya * 4


class obstacle:
    def __init__(self, pos, length, height):
        self.pos = pos
        self.hitbox = [[pos[0], pos[0] + length], [pos[1], pos[1] + height]]
        self.length = length
        self.height = height

    def draw(self):
        pygame.draw.rect(dis, black, [self.pos[0], self.pos[1], self.length, self.height])


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

    if hitbox1[1][0] <= hitbox2[1][0] <= hitbox1[1][1] or hitbox2[1][0] <= hitbox1[1][0] <= hitbox2[1][1]:
        if hitbox1[0][0] <= hitbox2[0][0] <= hitbox1[0][1]:
            return hitbox1
        if hitbox2[0][0] <= hitbox1[0][0] <= hitbox2[0][1]:
            return hitbox2
    return 0


player = player()
#
obstacles = [obstacle([0, 580], 600, 20), obstacle([0, 0], 600, 20),
             obstacle([0, 0], 20, 600), obstacle([580, 0], 20, 600)]

for _ in range(15):
    obstacles.append(obstacle([random.randint(0, 400), random.randint(0, 400)],
                              random.randint(50, 100), random.randint(50, 100)))

program_start = time.time()

while not game_over:

    dis.fill(white)

    y_delta_time = player.y_dt() * 4

    player.falling = True
    player.can_move_right = True
    player.can_move_left = True

    for obs in obstacles:

        if in_vertically(player.hitbox(), obs.hitbox):
            if vertical_collusion(player.hitbox(), obs.hitbox) == obs.hitbox:
                if player.jumping:
                    player.change_y_movement(10)
                    # dis.blit(get_entry_text(f"player under", 30), [20, 50])
            elif vertical_collusion(player.hitbox(), obs.hitbox) == player.hitbox():
                # dis.blit(get_entry_text(f"player on top", 30), [20, 50])
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
        # dis.blit(get_entry_text(" in " if in_vertically(player.hitbox(), obs.hitbox) else "not in", 30),
        #          [obs.pos[0], obs.pos[1] - 40])
        # dis.blit(get_entry_text(" col " if horizontal_collusion(player.hitbox(), obs.hitbox) else "not col", 30),
        #          [obs.pos[0], obs.pos[1] - 40])

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

    player.draw()
    for obs in obstacles:
        obs.draw()
    # dis.blit(get_entry_text(f"y = {player.pos[1]}", 30), [20, 20])
    # dis.blit(get_entry_text(f"v0 = {player.yv0}, a = {player.ya}, dt = {y_delta_time}", 30), [20, 50])
    # dis.blit(get_entry_text(f"{player.x0}", 30), [20, 20])
    # dis.blit(get_entry_text(f"v = {int(player.current_speed())}, coords = {int(player.pos[0]), int(player.pos[1])}",
    # 30)
    #          , [20, 20])
    # pygame.draw.rect(dis, black, [player.hitbox()[0][0], player.hitbox()[1][0],
    #                               player.hitbox()[0][1] - player.hitbox()[0][0],
    #                               player.hitbox()[1][1] - player.hitbox()[1][0]], width=1)
    # dis.blit(get_entry_text(f"falling = {player.falling}, jumping = {player.jumping}", 30), [20, 80])
    pygame.display.update()
