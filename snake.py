import random

import pygame
from pygame.locals import  *
import time

SIZE = 50
BACKGROUND = (255, 255, 255)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("F:/game/app.jpeg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 15) * SIZE
        self.y = random.randint(0, 11) * SIZE


class Snake:

    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("F:/game/small.jpeg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increment(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(BACKGROUND)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'right':
            self.x[0] += SIZE

        if self.direction == 'up':
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((800, 600))
        self.surface.fill(BACKGROUND)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()
        # collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increment()
            self.apple.move()
            sound = pygame.mixer.Sound("F:/game/ding-noise-sound-effect.mp3")
            pygame.mixer.Sound.play(sound)

        #collision with snake
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                over = pygame.mixer.Sound("F:/game/boing-sound-effect.mp3")
                pygame.mixer.Sound.play(over)
                raise "Game Over"


    def show_gameover(self):
        self.surface.fill(BACKGROUND)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Your Score is {self.snake.length}", True, (8, 8, 8))
        self.surface.blit(line1, (150, 150))
        line2 = font.render("Press enter to Play again", True, (8, 8, 8))
        self.surface.blit(line2, (150, 190))
        line3 = font.render("Press esc to exit", True, (8, 8, 8))
        self.surface.blit(line3, (150, 230))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (8, 8, 8))
        self.surface.blit(score, (600, 10))


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_gameover()
                pause = True
                self.reset()
            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()

