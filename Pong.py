import pygame
import random
import math
import time

dis = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pong by YS")
dis.set_colorkey((0, 0, 255))
black = (0, 0, 0)

pygame.font.init()

class Ball:
    def __init__(self):
        self.ballx = 300
        self.bally = 300
        self.ball_angle = random.random()
        self.modspeed = 0.3
        self.balltrail = [[self.ballx, self.bally]]

        self.boundstimer = 0
        self.rackettimer = 0

    def change_modspeed(self):
        self.modspeed *= - 1

    def mod_vectors(self):
        self.ballxmod = self.modspeed * math.cos(self.ball_angle)
        self.ballymod = self.modspeed * math.sin(self.ball_angle)
        self.ballx += self.ballxmod
        self.bally -= self.ballymod

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

    racket1 = 260  # right racket
    racket2 = 260  # left racket
    racket1mod = 0
    racket2mod = 0

    balls = []

    points = 0


    waiting = True
    wait_time = time.time()

    while not game_over:

        # mode selection screen
        while len(balls) == 0 and not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    if 200 <= y <= 320:
                        if 60 <= x <= 180:
                            balls = [Ball()]
                        elif 240 <= x <= 360:
                            balls = [Ball(), Ball()]
                        elif 420 <= x <= 580:
                            balls = [Ball(), Ball(), Ball()]

            dis.fill((0, 0, 255))
            dis.blit(get_entry_text("Choose gamemode", 50), [90, 50])

            # draw one ball button
            pygame.draw.rect(dis, black, [60, 200, 120, 120], width=10)
            pygame.draw.circle(dis, white, [120, 260], 16)

            # draw two balls trail button
            pygame.draw.rect(dis, black, [240, 200, 120, 120], width=10)
            pygame.draw.circle(dis, white, [280, 260], 16)
            pygame.draw.circle(dis, white, [320, 260], 16)

            # draw three balls button
            pygame.draw.rect(dis, black, [420, 200, 120, 120], width=10)
            pygame.draw.circle(dis, white, [480, 240], 16)
            pygame.draw.circle(dis, white, [455, 280], 16)
            pygame.draw.circle(dis, white, [505, 280], 16)

            pygame.display.update()

            wait_time = time.time()

        if waiting:
            wait_delta = time.time() - wait_time
            if wait_delta > 3:
                waiting = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            dis.fill((0, 0, 255))

            for ball in balls:
                for i in range(1, 200):  # draw a trail
                    if i < len(ball.balltrail):
                        pygame.draw.circle(dis, (225, 225, 225), ball.balltrail[i], 10 - 0.05 * i)

                pygame.draw.circle(dis, white, [ball.ballx, ball.bally], 10)  # draw the ball

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

            # handle balls
            for i, ball in enumerate(balls):
                # contact with racket 2 or 1
                if ball.rackettimer >= 200 and ((30 <= ball.ballx <= 50 and racket2 <= ball.bally <= racket2 + 80) or
                                           (
                                                   550 <= ball.ballx <= 570 and racket1 <= ball.bally <= racket1 + 80)):
                    ball.ball_angle = modifyangle(ball.ball_angle)
                    ball.change_modspeed()  # change ball movement direction
                    points += 1
                    ball.rackettimer = 0
                ball.rackettimer += 1  # time since hit a racket

                if ball.boundstimer >= 150 and (ball.bally >= 600 or ball.bally <= 0):  # contact with edges
                    ball.ball_angle = math.pi - ball.ball_angle
                    ball.change_modspeed()
                    ball.boundstimer = 0
                ball.boundstimer += 1  # time since hit a border

                if ball.balltrail[-1][0] < -10 or ball.balltrail[-1][0] > 610:
                    game_over = end_of_round()
                    balls = [Ball() for ball in balls]

                    points = 0
                    racket1 = 260  # right racket
                    racket2 = 260  # left racket

                    waiting = True
                    wait_time = time.time()

                    break

                wait_delta = time.time() - wait_time
                if wait_delta > i + 3:
                    ball.mod_vectors()
                # ball.ballxmod = ball.modspeed * math.cos(ball.ball_angle)  # modifying ball's vectors
                # ball.ballymod = ball.modspeed * math.sin(ball.ball_angle)
                # ball.ballx += ball.ballxmod
                # ball.bally -= ball.ballymod

                ball.balltrail = [[ball.ballx, ball.bally]] + ball.balltrail  # update trail
                if len(ball.balltrail) > 150:
                    ball.balltrail.remove(ball.balltrail[-1])

            dis.fill((0, 0, 255))
            textfont = pygame.font.SysFont('Comic Sans MS', 30)
            score = textfont.render("Score: " + str(points), False, (0, 0, 0))
            dis.blit(score, (245, 50))

            # draw rackets
            pygame.draw.rect(dis, white, [550, racket1, 20, 80])
            pygame.draw.rect(dis, white, [30, racket2, 20, 80])

            # draw balls
            for ball in balls:
                for i in range(1, 150):  # draw a trail
                    if i < len(ball.balltrail):
                        pygame.draw.circle(dis, (225, 225, 225), ball.balltrail[i], 10 - 0.05 * i)

                pygame.draw.circle(dis, white, [ball.ballx, ball.bally], 10)  # draw the ball


            pygame.display.update()


if __name__ == '__main__':
    game()
