# здесь подключаются модули
import pygame as pg
from dot import Dot
from settings import Settings
import time
from random import randint as rnd
import math as m
import os


if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (100, 100)

    # здесь определяются константы, классы и функции
    FPS = 30

    # здесь происходит инициация, создание объектов и др.
    pg.init()

    size = 800
    screen = pg.display.set_mode((size, size), flags=pg.DOUBLEBUF | pg.NOFRAME)

    surf = pg.Surface((size, size))
    clock = pg.time.Clock()

    settings = Settings(size, surf)
    settings.screen = screen

    # если надо до цикла отобразить объекты на экране
    pg.display.update()
    pg.font.init()
    fpsfont = pg.font.SysFont('Comic Sans MS', 20)

    x, y = 74, 74
    for _ in range(32):
        for _ in range(32):
            settings.dots.append(Dot(settings, x, y))
            x += 21
        x = 74
        y += 21

    deep_speed_count = 0

    # главный цикл
    while True:
        surf.fill((10, 10, 10))

        # задержка
        clock.tick(FPS)

        # настройка текста
        myfont = pg.font.SysFont('System', int(settings.text_size))
        text = myfont.render(f"Speed is {round(settings.dots[0].v, 1)}",
                                                        True, (255, 255, 255))
        text_surf = pg.Surface(text.get_size(), pg.SRCALPHA)
        text_surf.fill((255, 255, 255, settings.text_alpha))

        if settings.text_alpha >= 20:
            settings.text_alpha -= 20
        else:
            settings.text_alpha = 0

        if settings.text_size >= 61:
            settings.text_size -= 2

        fps = round(clock.get_fps())

        text_fps = fpsfont.render(str(fps), True, (250, 200, 50))

        screen.blit(surf, (0, 0))
        # pg.display.update(surf)

        screen.blit(text_fps, (10, 10))

        text.blit(text_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        text_rect = text.get_rect(center=(settings.size//2, settings.size//2))

        mouse_pos = pg.mouse.get_pos()

        m_rip_rad = 20
        if mouse_pos[0] >= settings.size - m_rip_rad or mouse_pos[0] <= m_rip_rad or\
            mouse_pos[1] >= settings.size - m_rip_rad or mouse_pos[1] <= m_rip_rad:
            mouse_pos = (-1000, -1000)

        m_rect = (int(mouse_pos[0] - settings.gravity_rad * 5), int(mouse_pos[1] - settings.gravity_rad * 5),
                  int(settings.gravity_rad * 10), int(settings.gravity_rad * 10))
        m_rect = pg.Rect(m_rect)

        arr = [k.rect for k in settings.dots]
        for k in m_rect.collidelistall(arr):
            settings.dots[k].check_gravity(mouse_pos[0], mouse_pos[1], gr=100, force=10)

        speed_count = 0

        for ind, dot in enumerate(settings.dots):

            if settings.dots_go_back:
                speed_count += abs(dot.speed_x) + abs(dot.speed_y)

            dot.borders_gravity()

            for i in dot.rect.collidelistall(arr):
                t = settings.dots[i]
                if t != dot:
                    dot.check_gravity(t.x, t.y)

            dot.update_pos()

            dot.draw()

        settings.screen.blit(text, text_rect)

        if speed_count == 0 and settings.dots_go_back:
            deep_speed_count += 1

            if deep_speed_count >= 5:
                deep_speed_count = 0
                settings.dots_go_back = False

                for dot in settings.dots:
                    dot.go_back = False

        # цикл обработки событий
        for i in pg.event.get():
            if i.type == pg.MOUSEBUTTONDOWN:

                if i.button == 4:
                    for dot in settings.dots:
                        if dot.v < 1.5 :
                            dot.v += 0.1
                            if dot.v > 1.5:
                                dot.v = 1.5

                        settings.text_alpha = 155
                        settings.text_size = 80

                elif i.button == 5:
                    for dot in settings.dots:
                        if 0.11 < dot.v :
                            dot.v -= 0.1

                        settings.text_alpha = 155
                        settings.text_size = 80

            elif i.type == pg.KEYDOWN:
                if i.key == 113 or i.key == 27:
                    exit()
                elif i.key == 32:
                    if settings.dots_go_back:
                        settings.dots_go_back = False
                    else:
                        settings.dots_go_back = True

                    for dot in settings.dots:

                        if settings.dots_go_back:
                            dot.go_back = True
                        else:
                            dot.go_back = False

                else:
                    print(i.key)

        # --------
        # изменение объектов и многое др.
        # --------

        # обновление экрана
        pg.display.update()
