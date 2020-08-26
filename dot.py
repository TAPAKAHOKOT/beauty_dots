from random import randint as rnd
import pygame as pg
import math as m
from settings import Settings

class Dot:
    def __init__(self, settings: Settings, x: int, y: int):
        self.settings = settings

        self.x = rnd(20, self.settings.size - 20)
        self.y = rnd(20, self.settings.size - 20)

        self.x, self.y = x, y

        self.start_x, self.start_y = x, y

        self.speed_x = self.speed_y = 0

        self.v = 1
        self.rad = 2

        self.borders_size = 60
        self.gravity_rad = 20

        self.s_r, self.s_g, self.s_b = 255, 100, 100
        self.r, self.g, self.b = self.s_r, self.s_g, self.s_b

        self.last_poses = [[-100, -100]] * 5

        self.color_chg = lambda col, s: int(col * (0.8 + s / 200))\
                        if 0 < int(col * (0.8 + s / 200)) <= 255 else col

        self.go_back = False
        self.another_col = False

        self.draw()

    def draw(self):

        for pos in self.last_poses:
            x, y = pos

            if not self.another_col:
                self.r = self.color_chg(self.r, (abs(self.speed_x) + abs(self.speed_y)))
                self.g = self.color_chg(self.g, (abs(self.speed_x) + abs(self.speed_y)))
                self.b = self.color_chg(self.b, (abs(self.speed_x) + abs(self.speed_y)))

                self.color = (self.r, self.g, self.b)

            pg.draw.circle(self.settings.screen, self.color,
                                         (int(x), int(y)), self.rad)

        if self.another_col:
            self.another_col = False

        self.r, self.g, self.b = self.s_r, self.s_g, self.s_b

        rect = (int(self.x - self.gravity_rad), int(self.y - self.gravity_rad),
                int(self.gravity_rad * 2), int(self.gravity_rad * 2))

        self.rect = pg.Rect(rect)

    def update_pos(self):

        ind = int(self.y // (self.settings.size // 52))

        if 0 < ind < 52:
            self.s_r, self.s_g, self.s_b = self.settings.test_colors[ind]

        self.x += self.speed_x

        if self.speed_x != 0:
            self.speed_x *= self.settings.f_tr

            if abs(self.speed_x) <= 0.05:
                self.speed_x = 0


        self.y += self.speed_y

        if self.speed_y != 0:
            self.speed_y *= self.settings.f_tr

            if abs(self.speed_y) <= 0.05:
                self.speed_y = 0

        self.last_poses = [[self.x, self.y]] + self.last_poses[:-1]

        if self.go_back:
            self.x += (self.start_x - self.x) / 8
            self.y += (self.start_y - self.y) / 8

            self.speed_x /= 10
            self.speed_y /= 10


    def borders_gravity(self):
        # Отталкивание от стенок границы

        if not (self.borders_size < self.y < self.settings.size - self.borders_size) or\
            not (self.borders_size < self.x < self.settings.size - self.borders_size):

            force = 2

            dist = min([self.x, self.settings.size - self.x])
            if dist < self.borders_size:
                self.speed_x += ((dist == self.x) * 2 - 1) *\
                (1 - dist / self.borders_size) * force * self.v


            dist = min([self.y, self.settings.size - self.y])
            if dist < self.borders_size:
                self.speed_y += ((dist == self.y) * 2 - 1) *\
                (1 - dist / self.borders_size) * force * self.v


    def check_gravity(self, x: int, y: int, gr:int=0, force:int=15):

        if not gr:
            gr = self.gravity_rad

        if m.sqrt((self.x - x)**2 + (self.y - y)**2) <= gr:

            koef_x = (self.x >= x) * 2 - 1
            koef_y =  (self.y >= y) * 2 - 1

            self.speed_x += koef_x * abs(self.x - x) / force * self.v
            self.speed_y += koef_y * abs(self.y - y) / force * self.v
