import pygame
import sys
import os
import sqlite3

# ----------
con = sqlite3.connect('game_database.db')
cur = con.cursor()
# ----------

FPS = 60
pygame.init()
size = WIDTH, HEIGHT = 1300, 650
screen_shop = pygame.display.set_mode(size)


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


def draw_shop():
    global text_x, text_h, landscapes_w, landscapes_y, socks_w, socks_y, hats_w, hats_y
    fon = pygame.transform.scale(load_image('shop.jpg'), (WIDTH, HEIGHT))
    screen_shop.blit(fon, (0, 0))
    font, color = pygame.font.Font('data/SourceCodePro-Light.ttf', 50), pygame.Color('black')
    texts = ['Магазин', 'Пейзажи', 'Носки', 'Шапки']

    screen_shop.blit(pygame.font.Font('data/SourceCodePro-Light.ttf', 30).render(f'У вас {money} монет', True, color),
                     (990, 10))

    magazin = font.render(texts[0], True, pygame.Color('red'))
    text_x, magazin_y = WIDTH // 2 - magazin.get_width() // 2, 0
    magazin_w, text_h = magazin.get_width(), magazin.get_height()
    screen_shop.blit(magazin, (text_x, magazin_y))

    landscapes = font.render(texts[1], True, color)
    text_x, landscapes_y = WIDTH // 2 - magazin.get_width() // 2, magazin_y + 100
    landscapes_w, text_h = magazin.get_width(), magazin.get_height()
    screen_shop.blit(landscapes, (text_x, landscapes_y))

    socks = font.render(texts[2], True, color)
    text_x, socks_y = WIDTH // 2 - magazin.get_width() // 2, landscapes_y + 200
    socks_w, text_h = magazin.get_width(), magazin.get_height()
    screen_shop.blit(socks, (text_x, socks_y))

    hats = font.render(texts[3], True, color)
    text_x, hats_y = WIDTH // 2 - magazin.get_width() // 2, socks_y + 200
    hats_w, text_h = magazin.get_width(), magazin.get_height()
    screen_shop.blit(hats, (text_x, hats_y))


def draw_shop_section(what, lk1, lk2, lk3, price):
    global second_x, second_y, second_w, second_h, third_x, third_y, third_w, third_h, is_bought1, is_bought2, s, t, \
        font1
    font, font1, color = pygame.font.Font('data/SourceCodePro-Light.ttf', 100), \
                         pygame.font.Font('data/SourceCodePro-Light.ttf', 30), pygame.Color('black')
    surf = pygame.Surface((WIDTH, HEIGHT))

    pict1 = pygame.transform.scale(load_image(lk1), (400, 200))
    pict2 = pygame.transform.scale(load_image(lk2), (400, 200))
    pict3 = pygame.transform.scale(load_image(lk3), (400, 200))

    fon = pygame.transform.scale(load_image('1.jpg'), (WIDTH, HEIGHT))
    surf.blit(fon, (0, 0))

    surf.blit(pict1, (0, 100))
    surf.blit(pict2, (445, 100))
    surf.blit(pict3, (885, 100))

    surf.blit(pygame.font.Font('data/SourceCodePro-Light.ttf', 30).render(f'У вас {money} монет', True, color),
              (990, 10))

    if cur.execute(f"""SELECT is_bought FROM shop WHERE name = '{lk1}' """).fetchone()[0] == 'нет':
        surf.blit(font1.render(f'Купить за {price} монет', True, color), (20, 310))
    else:
        surf.blit(font1.render(f'Уже куплено', True, color), (20, 310))

    if cur.execute(f"""SELECT is_bought FROM shop WHERE name = '{lk2}' """).fetchone()[0] == 'нет':
        second_x, second_y = 465, 310
        second = font1.render(f'Купить за {price + 300} монет', True, color)
        s = 'no'
        surf.blit(second, (465, 310))
        surf.blit(second, (second_x, second_y))
        second_w, second_h = second.get_width(), second.get_height()
    else:
        second_x, second_y = 465, 310
        s = 'yes'
        second = font1.render('Уже куплено', True, color)
        surf.blit(second, (second_x, second_y))
        second_w, second_h = second.get_width(), second.get_height()

    if cur.execute(f"""SELECT is_bought FROM shop WHERE name = '{lk3}' """).fetchone()[0] == 'нет':
        third_x, third_y = 905, 310
        t = 'no'
        third = font1.render(f'Купить за {price + 600} монет', True, color)
        surf.blit(third, (third_x, third_y))
        third_w, third_h = third.get_width(), third.get_height()
    else:
        third_x, third_y = 905, 310
        t = 'yes'
        third = font1.render(f'Уже куплено', True, color)
        surf.blit(third, (third_x, third_y))
        third_w, third_h = third.get_width(), third.get_height()

    text = font.render(what, True, color)
    text_x, text_y = WIDTH // 2 - text.get_width() // 2, 0
    surf.blit(text, (text_x, text_y))
    screen_shop.blit(surf, (0, 0))


def shop_section(what, lk1, lk2, lk3, price):
    global money
    clock = pygame.time.Clock()
    running_section = True
    click, flag_buy = 0, False

    while running_section:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running_section = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                buy_x, buy_y = event.pos
                if second_x < buy_x < second_x + second_w and second_y < buy_y < second_y + second_h \
                        and s == 'no':
                    click = 1
                    flag_buy = True
                elif third_x < buy_x < third_x + third_w and third_y < buy_y < third_y + third_h and t == 'no':
                    click = 2
                    flag_buy = True

            if keys[pygame.K_ESCAPE] and (click == 1 or click == 2):
                flag_buy = False

            elif keys[pygame.K_SPACE] and click == 1:
                if price + 300 <= money:
                    money = money - (price + 300)
                    cur.execute(f"""UPDATE shop SET is_bought = 'да' WHERE name = '{lk2}'""")
                    cur.execute(f"""INSERT INTO hranilishe(name) VALUES('{lk2}')""")
                    con.commit()
                    flag_buy = False

            elif keys[pygame.K_SPACE] and click == 2:
                if price + 600 <= money:
                    money = money - (price + 600)
                    cur.execute(f"""UPDATE shop SET is_bought = 'да' WHERE name = '{lk3}'""")
                    cur.execute(f"""INSERT INTO hranilishe(name) VALUES('{lk3}')""")
                    con.commit()
                    flag_buy = False

        draw_shop_section(what, lk1, lk2, lk3, price)

        if flag_buy:
            vivod = ['Нажмите ПРОБЕЛ, чтобы подвердить покупку',
                     'Для отмены нажмите ESC. Если у вас недостаточно средств,',
                     'вам будет недоступно первое действие.']
            text_coord = 450
            for line in vivod:
                string_rendered = font1.render(line, True, pygame.Color('red'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = WIDTH // 5
                text_coord += intro_rect.height
                screen_shop.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)


def shop():
    global money
    money = 5000  # ПОТОМ ИЗМЕНИТЬ!!!
    running_shop = True
    clock = pygame.time.Clock()
    screen_shop.fill('white')
    while running_shop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_shop = False
            if event.type == pygame.MOUSEBUTTONUP:
                x1, y1 = event.pos
                if text_x < x1 < text_x + landscapes_w and landscapes_y < y1 < landscapes_y + text_h:
                    shop_section('Пейзажи', 'shop_fon_land.jpg', 'shop_fon_christmas.jpg', 'shop_fon_throne.jpg', 1000)
                elif text_x < x1 < text_x + socks_w and socks_y < y1 < socks_y + text_h:
                    shop_section('Носки', 'shop_socks_oridginal.jpg', 'shop_socks_christmas.jpg', 'shop_socks_king.jpg',
                                 500)
                elif text_x < x1 < text_x + hats_w and hats_y < y1 < hats_y + text_h:
                    shop_section('Шапки', 'shop_hat_oridginal.jpg', 'shop_hat_christmas.jpg', 'shop_hat_king.jpg', 500)
        draw_shop()
        pygame.display.flip()
        clock.tick(FPS)


shop()
