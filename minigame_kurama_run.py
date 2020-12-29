import pygame
import sys
import os
from random import randint

FPS = 60
pygame.init()
size = WIDTH, HEIGHT = 1300, 650
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Pregrada(pygame.sprite.Sprite):
    image = load_image("bomb.png")

    def __init__(self, group, group1):
        global k
        super().__init__(group, group1)
        self.image = Pregrada.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 50
        self.rect.y = HEIGHT - self.rect.height - 100
        self.mask = pygame.mask.from_surface(self.image)
        k = 0

    def update(self):
        global k
        if self.rect.x >= - self.rect.width:
            self.rect.x -= 7
        else:
            self.rect.x = WIDTH + randint(0, 100)
            while abs(pregrada1.rect.x - pregrada.rect.x) < 300:
                self.rect.x = WIDTH + randint(300, 1000)
            k += 1


class Fox(pygame.sprite.Sprite):

    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(group)
        self.schet = 0
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        #self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 3
        self.rect.y = HEIGHT - self.rect.height - 100
        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        global isjump, jump_counter
        if jump_counter >= - 25:
            self.rect.y -= jump_counter
            jump_counter -= 1
        else:
            jump_counter = 25
            isjump = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.schet += 1
        if self.schet % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


def start_mini_game_1():
    global isjump, jump_counter, pregrada, pregrada1
    running_game = True
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    pregrada_sprites = pygame.sprite.Group()
    all_minigame_sprites = pygame.sprite.Group()
    fox = Fox(load_image("pygame-8-1.png"), 8, 1, 240, 191, all_minigame_sprites)
    pregrada = Pregrada(all_minigame_sprites, pregrada_sprites)
    pregrada1 = Pregrada(all_minigame_sprites, pregrada_sprites)
    isjump = False
    jump_counter = 25

    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                isjump = True
        screen.blit(fon, (0, 0))
        if isjump:
            fox.jump()
        all_minigame_sprites.draw(screen)
        if pygame.sprite.collide_mask(fox, pregrada) or pygame.sprite.collide_mask(fox, pregrada1):
            running_game = False
            game_end()
        all_minigame_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


def game_end():
    tre = True
    while tre:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                terminate()
                # ..... Выход на начальный экран
        font = pygame.font.Font(None, 30)
        vivod = [f"Игра окончена. Вы набрали {k if k < 100 else 100} опыта и {0 if k < 100 else k - 100} монет",
                 "Нажмите esc, чтобы вернуться на главный экран"]
        text_coord = 50
        for line in vivod:
            string_rendered = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            pygame.display.flip()


start_mini_game_1()
