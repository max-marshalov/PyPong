import os
import pygame
import sys
import time
import math
import random

pygame.init()

FPS = 60

#scr_size = (width, height) = (600, 400)

clock = pygame.time.Clock()


class Scene:
    def __init__(self, image):
        self.size = (600, 400)
        self.img = pygame.image.load(image)
        self.scale = pygame.transform.scale(self.img, (self.size[0], self.size[1]))

        self.screen = pygame.display.set_mode(self.size)
        self.fps = 60

    def draw_background(self):
        self.screen.blit(self.scale, (0, 0))


class Game(Scene):
    def __init__(self):
        super().__init__(image="data/Board.png")

    def displaytext(self, text, fontsize, x, y, color):
        font = pygame.font.SysFont('sawasdee', fontsize, True)
        text = font.render(text, 1, color)
        textpos = text.get_rect(centerx=x, centery=y)
        game.screen.blit(text, textpos)

    def aimove(self, ai, ball):
        if ball.movement[0] > 0:

            if ball.rect.bottom > ai.rect.bottom + ai.rect.height / 5:
                ai.movement[1] = 8
            elif ball.rect.top < ai.rect.top - ai.rect.height / 5:
                ai.movement[1] = -8
            else:
                ai.movement[1] = 0
        else:
            ai.movement[1] = 0


    def main(self):
        gameOver = False
        paddle = Paddle(game.size[0] / 10, game.size[1] / 2, game.size[0] / 60, game.size[1] / 8, (255, 255, 255))
        ai = Paddle(game.size[0] - game.size[0] / 10, game.size[1] / 2, game.size[0] / 60, game.size[1] / 8,
                    (255, 255, 255))
        ball = Ball(game.size[0] / 2, game.size[1] / 2, 12, (255, 255, 255), [5, 5])

        while not gameOver:

            if paddle.points > ai.points and paddle.points == 11:
                win.main()

                gameOver = True

            if paddle.points < ai.points and ai.points == 11:

                lose.main()

                gameOver = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        paddle.movement[1] = -8
                    elif event.key == pygame.K_s:
                        paddle.movement[1] = 8
                if event.type == pygame.KEYUP:
                    paddle.movement[1] = 0

            game.aimove(ai, ball)

            game.draw_background()

            paddle.draw()
            ai.draw()
            ball.draw()

            game.displaytext(str(paddle.points), 20, game.size[0] / 8, 25, (255, 255, 255))
            game.displaytext(str(ai.points), 20, game.size[0] - game.size[0] / 8, 25, (255, 255, 255))

            if pygame.sprite.collide_mask(paddle, ball):
                ball.movement[0] = -1 * ball.movement[0]
                ball.movement[1] = ball.movement[1] - int(0.1 * random.randrange(5, 10) * paddle.movement[1])
                if ball.movement[1] > ball.maxspeed:
                    ball.movement[1] = ball.maxspeed
                if ball.movement[1] < -1 * ball.maxspeed:
                    ball.movement[1] = -1 * ball.maxspeed

            if pygame.sprite.collide_mask(ai, ball):
                ball.movement[0] = -1 * ball.movement[0]
                ball.movement[1] = ball.movement[1] - int(0.1 * random.randrange(5, 10) * ai.movement[1])
                if ball.movement[1] > ball.maxspeed:
                    ball.movement[1] = ball.maxspeed
                if ball.movement[1] < -1 * ball.maxspeed:
                    ball.movement[1] = -1 * ball.maxspeed

            if ball.score == 1:
                ai.points += 1
                ball.score = 0
            elif ball.score == -1:
                paddle.points += 1
                ball.score = 0

            paddle.update()
            ball.update()
            ai.update()

            pygame.display.update()

            clock.tick(FPS)

        pygame.quit()
        quit()



class Menu(Scene):
    def __init__(self):
        super().__init__(image="data/Menu.png")


    def main(self):
        scene = True
        while scene:
            menu.draw_background()
            exit_button = Button(250, 230, 100, 50, "data/Exit.png")
            start_button = Button(250, 150, 100, 50, "data/Start.png")
            #start_button = Button()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scene = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if exit_button.check_collision():
                        scene = False
                    if start_button.check_collision():
                        game.main()
                        scene = False

            pygame.display.flip()


class Lose(Scene):
    def __init__(self):
        super().__init__(image="data/GameOver.png")


    def main(self):
        scene = True
        while scene:
            lose.draw_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scene = False
                if event.type == pygame.KEYUP:
                    menu.main()
                    scene = False
            pygame.display.flip()



class Win(Scene):
    def __init__(self):
        super().__init__(image="data/Win.png")


    def main(self):
        scene = True
        while scene:
            win.draw_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scene = False
                if event.type == pygame.KEYUP:
                    menu.main()
                    scene = False
            pygame.display.flip()





















class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, sizex, sizey, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.image = pygame.Surface((sizex, sizey), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.rect(self.image, self.color, (0, 0, sizex, sizey))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.points = 0
        self.movement = [0, 0]

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > game.size[1]:
            self.rect.bottom = game.size[1]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > game.size[0]:
            self.rect.right = game.size[0]

    def update(self):
        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        # pygame.draw.rect(self.image,self.color,(0,0,self.sizex,self.sizey))
        game.screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, size, color, movement=[0, 0]):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.movement = movement
        self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.color, (int(self.rect.width / 2), int(self.rect.height / 2)), int(size / 2))
        self.rect.centerx = x
        self.rect.centery = y
        self.maxspeed = 10
        self.score = 0
        self.movement = movement

    def checkbounds(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > game.size[1]:
            self.rect.bottom = game.size[1]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > game.size[0]:
            self.rect.right = game.size[0]

    def update(self):
        if self.rect.top == 0 or self.rect.bottom == game.size[1]:
            self.movement[1] = -1 * self.movement[1]
        if self.rect.left == 0:
            self.rect.centerx = game.size[0] / 2
            self.rect.centery = game.size[1] / 2
            self.movement = [random.randrange(-1, 2, 2) * 4, random.randrange(-1, 2, 2) * 4]
            self.score = 1

        if self.rect.right == game.size[0]:
            self.rect.centerx = game.size[0] / 2
            self.rect.centery = game.size[1] / 2
            self.movement = [random.randrange(-1, 2, 2) * 4, random.randrange(-1, 2, 2) * 4]
            self.score = -1

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def draw(self):
        pygame.draw.circle(self.image, self.color, (int(self.rect.width / 2), int(self.rect.height / 2)),
                           int(self.size / 2))
        game.screen.blit(self.image, self.rect)



class Button:
    def __init__(self, pos_x, pos_y, width, height, image):
        self.width = width
        self.height = height
        self.x = pos_x
        self.y = pos_y
        self.img = pygame.image.load(image)
        self.scale = pygame.transform.scale(self.img, (self.width, self.height))

        pygame.draw.rect(menu.screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

        menu.screen.blit(self.scale, (self.x, self.y))

    def check_collision(self):
        if pygame.mouse.get_pos() >= (self.x, self.y) and pygame.mouse.get_pos() <= (
                (self.x + self.width), (self.y + self.height)):

            return True

        else:

            return False


game = Game()
menu = Menu()
lose = Lose()
win = Win()



menu.main()
