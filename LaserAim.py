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


class Mirror:

    def __init__(self, center):
        self.center = center
        self.angle = 0
        self.start = [center[0] + math.cos(self.angle) * 25, center[1] - math.sin(self.angle) * 25]
        self.end = [center[0] + math.cos(math.pi + self.angle) * 25, center[1] - math.sin(math.pi + self.angle) * 25]
        self.clicked = False

    def draw(self):
        pygame.draw.line(dis, silver, self.start, self.end, width=6)
        pygame.draw.circle(dis, black, self.center, 4)
        pygame.draw.circle(dis, red, self.start, 2)

    def movable(self, mouse_pos):
        return dist(mouse_pos, self.center) <= 5

    def update(self):
        self.start = [self.center[0] + math.cos(self.angle) * 25,
                      self.center[1] - math.sin(self.angle) * 25]
        self.end = [self.center[0] + math.cos(math.pi + self.angle) * 25,
                    self.center[1] - math.sin(math.pi + self.angle) * 25]

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

    laser_trail = create_laser()
    mirrors = [Mirror(point) for i, point in enumerate(laser_trail) if 0 < i < len(laser_trail) - 1]


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

        dis.fill(yellow)
        draw_laser(laser_trail)
        for mirror in mirrors:
            mirror.update()
            mirror.draw()
        pygame.display.update()

game()
