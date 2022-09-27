import pygame
import math
import random

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("BrickBreak by YS")
dis.set_colorkey((0, 255, 0))

pygame.font.init()

white = (255, 255, 255)


def get_entry_text(msg, fontsize):
    """
    Forms a rendered version of a message
    :param msg:
    :param fontsize:
    :return: None
    """
    textfont = pygame.font.SysFont('Comic Sans MS', fontsize)
    return textfont.render(msg, False, (0, 0, 0))


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


def game():
    game_over = False

    # ball properties
    modspeedx = 0.5
    modspeedy = 0.5
    ballx = 300
    bally = 450
    slope = 0
    released = False

    score = 0

    bricks = create_bricks()

    addrow = False
    addrowflag = False

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:  # clicking releases the ball
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
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]
        county = mousey
        countx = mousex

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
            # set the slope
            if ballx - mousex == 0:
                slope = math.inf
            else:
                slope = (bally - mousey) / (ballx - mousex)

            # create release trail
            while county > bally:
                pygame.draw.circle(dis, white, [countx, county], 2)
                if slope != math.inf:
                    countx -= slope / abs(slope) * math.cos(math.atan(slope)) * 20
                    county -= slope / abs(slope) * math.sin(math.atan(slope)) * 20
                else:
                    county -= 10

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

        pygame.display.update()


if __name__ == '__main__':
    game()
