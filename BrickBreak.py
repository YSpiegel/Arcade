import pygame
import math
import random

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("BrickBreak by YS")
dis.set_colorkey((0, 255, 0))

pygame.font.init()

white = (255, 255, 255)
black = (0, 0, 0)


def get_entry_text(msg, fontsize):
    """
    Forms a rendered version of a message
    :param msg:
    :param fontsize:
    :return: None
    """
    textfont = pygame.font.SysFont('Comic Sans MS', fontsize)
    return textfont.render(msg, False, black)


def create_bricks():
    bricks = []
    for y in range(3):  # create first three rows
        brickrow = []
        for x in range(8):  # create eight possible bricks in each row
            if random.randrange(1, 11) > 2:  # 80% chance for each brick
                brickrow.append([75 * x + 15, 100 + 50 * y])  # brick location formula
            else:
                brickrow.append([-100, -100])  # brick not existent
        bricks.append(brickrow)
    return bricks


def end_of_round():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return True
                if event.key == pygame.K_r:
                    return False

        dis.blit(get_entry_text("Click q to quit or r for another round", 30), [10, 500])

        pygame.display.update()


def draw_target(center, size):
    x = center[0]
    y = center[1]
    pygame.draw.circle(dis, black, center, 8 * size, width=4 * size)
    pygame.draw.circle(dis, black, center, 16 * size, width=4 * size)
    pygame.draw.line(dis, black, [x-(20*size), y], [x-(5*size), y], width=size)
    pygame.draw.line(dis, black, [x+(5*size), y], [x+(20*size), y], width=size)
    pygame.draw.line(dis, black, [x, y-(20*size)], [x, y-(5*size)], width=size)
    pygame.draw.line(dis, black, [x, y+(5*size)], [x, y+(20*size)], width=size)


def shift_location(loc, size, angle, radius):
    return [loc[0] + math.cos(angle) * radius * size, loc[1] + math.sin(angle) * radius * size]


def draw_arrow(bottom, size, angle):
    head1 = shift_location(bottom, size, angle, 3 * size)
    head2 = shift_location(bottom, size, angle, 2 * size)
    side_a = shift_location(bottom, size, angle - math.pi / (size * 2.5), 2 * size)
    side_b = shift_location(bottom, size, angle + math.pi / (size * 2.5), 2 * size)
    pygame.draw.line(dis, white, bottom, head2, width=size)
    pygame.draw.polygon(dis, white, [head1, side_a, side_b])

def game():
    game_over = False

    # ball properties
    modspeedx = 0.5
    modspeedy = 0.5
    ballx = 300
    bally = 450
    slope = math.pi * 1.5
    released = False

    score = 0

    bricks = create_bricks()

    addrow = False
    addrowflag = False

    mode = -1  # ball control modes: 0 - target, 1 - release trail, 2 - arrow
    arrow_angle = math.pi * 1.5
    arrow_angle_mod = math.pi / 1024

    def bricks_falling():

        bricks_fell = False
        acceleration = 0
        while not bricks_fell:
            for brick in bricks[-1]:
                pygame.draw.rect(dis, (0, 255, 0), [brick[0], brick[1], 50, 20])
                if brick[0] != -100:
                    brick[1] += 0.01 + 0.5 * acceleration
                    if brick[1] > 600:
                        bricks_fell = True
                pygame.draw.rect(dis, white, [brick[0], brick[1], 50, 20])  # draw brick

            for x in range(15):  # draw release line
                pygame.draw.rect(dis, white, [80 * x, 450, 40, 2])

            acceleration += 0.01
            pygame.display.update()

    while not game_over:

        # mode selection screen:
        while mode == -1 and not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    if 200 <= y <= 320:
                        if 60 <= x <= 180:
                            mode = 0
                        elif 240 <= x <= 360:
                            mode = 1
                        elif 420 <= x <= 580:
                            mode = 2


            dis.fill((0, 255, 0))
            dis.blit(get_entry_text("Choose gamemode", 50), [90, 50])

            # draw target button
            pygame.draw.rect(dis, black, [60, 200, 120, 120], width=10)
            draw_target([120, 260], 2)

            # draw release trail button
            pygame.draw.rect(dis, black, [240, 200, 120, 120], width=10)
            for i in range(8):
                pygame.draw.circle(dis, white, [265 + 10 * i, 295 - 10 * i], 4)

            # draw arrow button
            pygame.draw.rect(dis, black, [420, 200, 120, 120], width=10)
            draw_arrow([480, 295], 5, math.pi * 1.5)

            pygame.display.update()

        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    (mode == 1 and my > 450 or mode == 0 and my < 450):  # clicking releases the ball
                released = True
                if bally == 450:  # every two turns add a row
                    if addrowflag:
                        addrow = True
                    addrowflag = not addrowflag
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and mode == 2:
                    released = True
                    if bally == 450:  # every two turns add a row
                        if addrowflag:
                            addrow = True
                        addrowflag = not addrowflag

        dis.fill((0, 255, 0))
        for x in range(15):  # draw release line
            pygame.draw.rect(dis, white, [80 * x, 450, 40, 2])

        dis.blit(get_entry_text(f"Score: {score}", 30), [250, 10])

        pygame.draw.circle(dis, white, [ballx, bally], 10)  # draw ball
        county = my
        countx = mx

        end_round = False

        # draw bricks and check for bricks being destroyed
        for row in bricks:
            row_exists = 8
            for brick in row:
                if (brick[0] <= ballx <= brick[0] + 50 and  # ball in contact with brick's upper/lower part
                        (brick[1] - 10 <= bally <= brick[1] or brick[1] + 20 <= bally <= brick[1] + 30)):
                    modspeedy *= -1
                    brick[0] = -100
                    brick[1] = -100
                    score += 1
                if brick[1] <= bally <= brick[1] + 20 and \
                        (brick[0] - 10 <= ballx <= brick[0] or brick[0] + 50 <= ballx <= brick[0] + 60):
                    # ball in contact with brick's left/right part
                    modspeedx *= -1
                    brick[0] = -100
                    brick[1] = -100
                    score += 1
                if (brick[1] - 10 <= bally <= brick[1] or brick[1] + 20 <= bally <= brick[1] + 30) and \
                        (brick[0] - 10 <= ballx <= brick[0] or brick[0] + 50 <= ballx <= brick[0] + 60):
                    # ball in contact with brick's edge part
                    if abs(slope) > 1:  # change direction by slope
                        modspeedy *= -1
                    else:
                        modspeedx *= -1
                    brick[0] = -100
                    brick[1] = -100
                    score += 1
                pygame.draw.rect(dis, white, [brick[0], brick[1], 50, 20])  # draw brick

                # count non-existing bricks
                if brick[0] == brick[1] == -100:
                    row_exists -= 1

                # end of round scenario
                if brick[1] == 450:
                    end_round = True

            # remove row if doesn't exist
            if not row_exists:
                bricks.remove(row)

        # bounce off bounds
        if ballx <= 0 or ballx >= 600:
            modspeedx *= -1
        if bally <= 0:
            modspeedy *= -1

        if released:  # set moving ball's position
            if slope > 0:  # change x-axis speed according to slope
                ballx += modspeedx * math.cos(math.atan(slope)) * -2
            ballx += modspeedx * math.cos(math.atan(slope))
            bally -= modspeedy * math.sin(abs(math.atan(slope)))
        else:
            if mode == 0 or mode == 1:
                # set the slope
                if ballx - mx == 0:
                    slope = math.inf
                else:
                    slope = (bally - my) / (ballx - mx)

                # create release trail
                if mode == 1:
                    while county > bally:
                        pygame.draw.circle(dis, white, [countx, county], 2)
                        if slope != math.inf:
                            countx -= slope / abs(slope) * math.cos(math.atan(slope)) * 20
                            county -= slope / abs(slope) * math.sin(math.atan(slope)) * 20
                        else:
                            county -= 10

                # create target tracker
                if mode == 0 and my < 450:
                    draw_target(pygame.mouse.get_pos(), 1)

            # mode 2 - arrow
            else:
                arrow_angle += arrow_angle_mod
                if arrow_angle >= math.pi * 31 / 16 or arrow_angle <= math.pi + math.pi / 16:
                    arrow_angle_mod *= - 1
                slope = math.tan(arrow_angle)
                draw_arrow([ballx, bally], 4, arrow_angle)





        if bally == 450:  # ball on the release line
            released = False
            modspeedx = 0.5
            modspeedy = 0.5

            if addrow:
                # advance each row downwards
                for row in bricks:
                    for brick in row:
                        if brick[1] != -100:
                            brick[1] += 50

                newrow = []

                # add another row on top
                for x in range(8):
                    if random.randrange(1, 10) > 2:
                        newrow.append([75 * x + 15, 100])
                    else:
                        newrow.append([-100, -100])
                bricks.insert(0, newrow)

                addrow = False

        if end_round:
            bricks_falling()
            game_over = end_of_round()

            bricks = create_bricks()
            score = 0
            addrow = False
            addrowflag = False

            # reset ball properties
            modspeedx = 0.5
            modspeedy = 0.5
            ballx = 300
            bally = 450
            slope = 0
            released = False

            mode = -1  # ball control modes: 0 - target, 1 - release trail, 2 - arrow
            arrow_angle = math.pi * 1.5
            arrow_angle_mod = math.pi / 1024

        pygame.display.update()


if __name__ == '__main__':
    game()
