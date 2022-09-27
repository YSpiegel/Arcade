import pygame
import random
import math
import time

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pong by YS")
dis.set_colorkey((0, 0, 255))

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


def modifyangle(ball_angle):
    """
    Change the angle according to its current value
    :param ball_angle:
    :return: Modified ball_angle
    """
    if ball_angle > 0.5:
        ball_angle -= random.random() / 2
    else:
        ball_angle += random.random() / 2
    return ball_angle


def end_of_round():
    while True:
        dis.blit(get_entry_text("Click q to quit or r for another round", 28), [62, 500])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return True
                elif event.key == pygame.K_r:  # reset parameters for a new match
                    return False

        pygame.display.update()


def game():
    game_over = False

    white = (255, 255, 255)

    racket1 = 300  # right racket
    racket2 = 300  # left racket
    racket1mod = 0
    racket2mod = 0

    ballx = 300
    bally = 300
    ball_angle = random.random()
    modspeed = 0.4
    balltrail = [[ballx, bally]]

    points = 0

    boundstimer = 0
    rackettimer = 0

    waiting = True
    wait_time = time.time()

    while not game_over:

        if waiting:
            wait_delta = time.time() - wait_time
            if wait_delta > 3:
                waiting = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            dis.fill((0, 0, 255))

            for i in range(1, 200):  # draw a trail
                if i < len(balltrail):
                    pygame.draw.circle(dis, (225, 225, 225), balltrail[i], 10 - 0.05 * i)

            pygame.draw.circle(dis, white, [ballx, bally], 10)  # draw the ball

            # draw rackets
            pygame.draw.rect(dis, white, [550, racket1, 20, 80])
            pygame.draw.rect(dis, white, [30, racket2, 20, 80])

            if 0 < wait_delta < 1:
                dis.blit(get_entry_text("3", 30), [295, 10])
            if 1 < wait_delta < 2:
                dis.blit(get_entry_text("2", 30), [295, 10])
            if 2 < wait_delta < 3:
                dis.blit(get_entry_text("1", 30), [295, 10])

            pygame.display.update()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.KEYDOWN:  # key of either racket is pressed on frame
                    # right racket movement modifier
                    if event.key == pygame.K_UP and racket1 > 0:
                        racket1mod = -1
                    elif event.key == pygame.K_DOWN and racket1 < 520:
                        racket1mod = 1
                    # left racket movement modifier
                    if event.key == pygame.K_w and racket2 > 0:
                        racket2mod = -1
                    elif event.key == pygame.K_s and racket2 < 520:
                        racket2mod = 1

                elif event.type == pygame.KEYUP:  # release of control over the rackets
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:  # right racket is not controlled
                        racket1mod = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:  # left racket is not controlled
                        racket2mod = 0

            if (racket1 == 0 or racket1 == 520) and \
                    not 0 < racket1 + racket1mod < 520:  # making sure racket is inbound
                racket1mod = 0
            else:  # in bounds
                racket1 += racket1mod

            if (racket2 == 0 or racket2 == 520) and \
                    not 0 < racket2 + racket2mod < 520:  # making sure racket is inbound
                racket2mod = 0
            else:  # in bounds
                racket2 += racket2mod

            if (rackettimer > 2500) and abs(modspeed) == 0.4:  # accelerate if takes long
                modspeed *= 4
            if (ballx <= 150 or ballx >= 450) and abs(modspeed) == 1.6:  # decelerate if getting close to a racket
                modspeed /= 4

            # contact with racket 2 or 1
            if rackettimer >= 200 and ((30 <= ballx <= 50 and racket2 <= bally <= racket2 + 80) or
                                       (
                                               550 <= ballx <= 570 and racket1 <= bally <= racket1 + 80)):
                ball_angle = modifyangle(ball_angle)
                modspeed = -modspeed  # change ball movement direction
                points += 1
                rackettimer = 0
            rackettimer += 1  # time since hit a racket

            if boundstimer >= 150 and (bally >= 600 or bally <= 0):  # contact with edges
                ball_angle = math.pi - ball_angle
                modspeed = -modspeed
                boundstimer = 0
            boundstimer += 1  # time since hit a border

            if balltrail[-1][0] < -10 or balltrail[-1][0] > 610:
                game_over = end_of_round()
                racket1 = 300  # right racket
                racket2 = 300  # left racket
                racket1mod = 0
                racket2mod = 0

                ballx = 300
                bally = 300
                ball_angle = random.random()
                modspeed = 0.4

                points = 0

                balltrail = [[ballx, bally]]

                waiting = True
                wait_time = time.time()

            ballxmod = modspeed * math.cos(ball_angle)  # modifying ball's vectors
            ballymod = modspeed * math.sin(ball_angle)
            ballx += ballxmod
            bally -= ballymod

            balltrail = [[ballx, bally]] + balltrail  # update trail
            if len(balltrail) > 150:
                balltrail.remove(balltrail[-1])

            dis.fill((0, 0, 255))

            # draw rackets
            pygame.draw.rect(dis, white, [550, racket1, 20, 80])
            pygame.draw.rect(dis, white, [30, racket2, 20, 80])

            for i in range(1, 150):  # draw a trail
                if i < len(balltrail):
                    pygame.draw.circle(dis, (225, 225, 225), balltrail[i], 10 - 0.05 * i)

            pygame.draw.circle(dis, white, [ballx, bally], 10)  # draw the ball

            textfont = pygame.font.SysFont('Comic Sans MS', 30)
            score = textfont.render("Score: " + str(points), False, (0, 0, 0))
            dis.blit(score, (245, 50))

            pygame.display.update()


if __name__ == '__main__':
    game()
