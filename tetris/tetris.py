import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
color_glass = BLACK

WIDTH = 10
HEIGHT = 20

EMPTY = 0

FULL = 1

CELL_SIZE = 30

size = [WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE]
screen = pygame.display.set_mode(size)

O = [[[1, 1],
      [1, 1]]]

I = [[[1, 1, 1, 1]],
     [[1],
      [1],
      [1],
      [1]]]

J = [[[1, 0, 0],
      [1, 1, 1]],
     [[0, 1],
      [0, 1],
      [1, 1]],
     [[1, 1, 1],
      [0, 0, 1]],
     [[1, 1],
      [1, 0],
      [1, 0]]]

L = [[[0, 0, 1],
      [1, 1, 1]],
     [[1, 1],
      [0, 1],
      [0, 1]],
     [[1, 1, 1],
      [1, 0, 0]],
     [[1, 0],
      [1, 0],
      [1, 1]]]

T = [[[0, 1, 0],
      [1, 1, 1]],
     [[0, 1],
      [1, 1],
      [0, 1]],
     [[1, 1, 1],
      [0, 1, 0]],
     [[1, 0],
      [1, 1],
      [1, 0]]]

S = [[[0, 1, 1],
      [1, 1, 0]],
     [[1, 0],
      [1, 1],
      [0, 1]]]

Z = [[[1, 1, 0],
      [0, 1, 1]],
     [[0, 1],
      [1, 1],
      [1, 0]]]

FORMS = [O, I, J, L, T, S, Z]


class Field:
    def __init__(self, width, height, color=BLACK):
        self.width = width
        self.height = height
        self.glass = []
        self.color = color
        for i in range(height):
            string = [FULL] + [EMPTY] * self.width + [FULL]
            self.glass.append(string)
        string = [FULL] * (self.width + 2)
        self.glass.append(string)
        self.draw(screen)

    def draw(self, screen):
        screen.fill(self.color)
        for y in range(self.height):
            for x in range(1, self.width + 1):
                if self.glass[y][x] != EMPTY:
                    pygame.draw.rect(screen, self.glass[y][x],
                                     [(x - 1) * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE])

    def delete_rows(self):
        for y in range(self.height):
            if EMPTY not in self.glass[y]:
                self.glass = [[FULL] + [EMPTY] * self.width + [FULL]] + self.glass[:y] + self.glass[y + 1:]

    def glass_is_full(self):
        return self.glass[0][1:-1] != [EMPTY] * self.width


class Figure:
    def __init__(self, field, screen, forms, turn):
        self.x = field.width // 2 - 1
        self.y = 0
        self.forms = forms
        self.turn = turn
        self.form = forms[turn]
        R = random.randint(50, 255)
        G = random.randint(50, 255)
        B = random.randint(50, 255)
        self.color = (R, G, B)
        self.draw(screen, self.color)

    def draw(self, screen, color=WHITE):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    pygame.draw.rect(screen, color,
                                     [(self.x + x - 1) * CELL_SIZE, (self.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE])

    def move_down(self, screen):
        self.draw(screen, color_glass)
        self.y += 1
        self.draw(screen, self.color)

    def move_right(self, screen):
        self.draw(screen, color_glass)
        self.x += 1
        self.draw(screen, self.color)

    def move_left(self, screen):
        self.draw(screen, color_glass)
        self.x += -1
        self.draw(screen, self.color)

    def can_move_right(self, field):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    if field.glass[self.y + y][self.x + x + 1] != EMPTY:
                        return False
        return True

    def can_move_left(self, field):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    if field.glass[self.y + y][self.x - 1] != EMPTY:
                        return False
        return True

    def can_move_down(self, field):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    if field.glass[self.y + y + 1][self.x + x] != EMPTY:
                        return False
        return True

    def rotate(self, screen):
        self.draw(screen, color_glass)
        if self.turn < len(self.forms) - 1:
            self.turn += 1
        else:
            self.turn = 0
        self.form = self.forms[self.turn]
        self.draw(screen, self.color)

    def can_rotate(self, field):
        if self.turn < len(self.forms) - 1:
            turn_next = self.turn + 1
        else:
            turn_next = 0

        next_form = self.forms[turn_next]
        for y in range(len(next_form)):
            for x in range(len(next_form[y])):
                if next_form[y][x] == FULL:
                    if field.glass[self.y + y][self.x + x] != EMPTY:
                        return False
        return True

    def print_figure(self, field):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    field.glass[self.y + y][self.x + x] = self.color


field = Field(WIDTH, HEIGHT, color_glass)
figure_random = random.choice(FORMS)
figure = Figure(field, screen, figure_random, 0)
SPEED = 400
# создается очередь из событий, проверяется каждый SPEED миллисекунд
pygame.time.set_timer(pygame.KEYDOWN, SPEED)

pygame.display.set_caption('My game')

pygame.mouse.set_visible(0)

done = True

while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen.fill(color_glass)
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if figure.can_move_right(field):
                    figure.move_right(screen)
            elif event.key == pygame.K_LEFT:
                if figure.can_move_left(field):
                    figure.move_left(screen)
            elif event.key == pygame.K_SPACE:
                pygame.time.set_timer(pygame.KEYDOWN, SPEED // 10)
            elif event.key == pygame.K_UP:
                if figure.can_rotate(field):
                    figure.rotate(screen)
            else:
                if figure.can_move_down(field):
                    figure.move_down(screen)
                else:
                    figure.print_figure(field)
                    field.delete_rows()
                    field.draw(screen)
                    if field.glass_is_full():
                        done = False
                    else:
                        pygame.time.set_timer(pygame.KEYDOWN, SPEED)
                        figure = Figure(field, screen, random.choice(FORMS), 0)
    pygame.display.flip()

pygame.quit()
