import pygame
import math
import random

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("LaserAim by YS")
dis.set_colorkey((255, 255, 0))
yellow = (255, 255, 0)
red = (255, 0, 0)
silver = (169, 169, 169)
black = (0, 0, 0)
pygame.font.init()


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


def disposition(point, angle, radius):
    return [point[0] + math.cos(angle) * radius, point[1] - math.sin(angle) * radius]


class Mirror:

    def __init__(self, center):
        self.center = center
        self.angle = 0
        self.start = disposition(center, self.angle, 25)
        self.end = disposition(center, math.pi + self.angle, 25)
        self.clicked = False

    def draw(self):
        pygame.draw.line(dis, silver, self.start, self.end, width=6)
        pygame.draw.circle(dis, black, self.center, 4)

    def movable(self, mouse_pos):
        return dist(mouse_pos, self.center) <= 8

    def update(self):
        self.start = disposition(self.center, self.angle, 25)
        self.end = disposition(self.center, math.pi + self.angle, 25)

    def in_contact(self, point):
        return abs(dist(point, self.start) + dist(point, self.end) - dist(self.start, self.end)) <= 1

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def angle(A, B, C):
    """
    Find the angle BAC
    :param A: head point coords
    :param B: side point coords
    :param C: side point coords
    :return: BAC
    """
    a = dist(B, C)
    b = dist(A, C)
    c = dist(A, B)

    return math.acos((b**2 + c**2 - a**2) / (2*b*c))


def valid_point(point, points):
    for i in range(len(points)):
        if dist(points[i], point) <= 50:
            return False
        if (len(points) > 1 and i < len(points) - 1 and angle(point, points[i], points[i+1]) > math.pi * 6 / 8) or \
                (1 < i < len(points) and angle(points[i-1], points[i], point) > math.pi * 6 / 8):
            return False
    return True

def create_laser():
    points = [[600, random.randint(50, 500)]]

    for _ in range(5):
        point = [random.randint(50, 550), random.randint(50, 550)]
        while not valid_point(point, points):
            point = [random.randint(50, 550), random.randint(50, 550)]
        points.append(point)

    points.append([0, random.randint(50, 500)])

    return points


def draw_laser(laser_trail):
    for i in range(len(laser_trail) - 1):
        pygame.draw.line(dis, red, laser_trail[i], laser_trail[i+1], width=4)


def game():
    game_over = False

    target_laser_trail = create_laser()
    mirrors = [Mirror(point) for i, point in enumerate(target_laser_trail) if 0 < i < len(target_laser_trail) - 1]


    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for mirror in mirrors:
                    if mirror.clicked:
                        mirror.clicked = False
                    if mirror.movable(pygame.mouse.get_pos()):
                        mirror.clicked = True

        for mirror in mirrors:
            if mirror.clicked:
                mirror.angle = get_angle(mirror.center, pygame.mouse.get_pos()) - math.pi / 2

        current_laser = [target_laser_trail[0], target_laser_trail[0]]
        laser_angle = get_angle(target_laser_trail[0], target_laser_trail[1])
        while current_laser[-1][0] > 0:

            # draw_laser(current_laser)
            # for mirror in mirrors:
            #     mirror.update()
            #     mirror.draw()
            # pygame.display.update()

            if not 0 <= current_laser[-1][1] <= 600:
                laser_angle = math.pi - laser_angle
                current_laser.append(current_laser[-1])
            for mirror in mirrors:
                if mirror.in_contact(current_laser[-1]):
                    laser_angle = mirror.angle - laser_angle
                    current_laser.append(current_laser[-1])

            current_laser[-1] = disposition(current_laser[-1], laser_angle, 1)

        dis.fill(yellow)
        draw_laser(current_laser)

        for mirror in mirrors:
            mirror.update()
            mirror.draw()
            dis.blit(get_entry_text(str(mirror.angle)[:4], 20), mirror.center)
        pygame.display.update()

game()
