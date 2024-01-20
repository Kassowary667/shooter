import pygame, random

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
clock.tick(70)
scr = pygame.display.set_mode((1000, 600))  # Створення вікна гри
pygame.display.set_caption("Shooter")
pygame.display.set_icon(pygame.image.load("rocket.png"))
P = False
F = False
A = True
B = True
O = True
FB = False
W = 0
EB = False
BL = False
bg_y = -1200
bg_change = 0.25
G_O = pygame.image.load("game_over.png")
G_O = pygame.transform.scale(G_O, (1000, 600)).convert_alpha()
VICTORY = pygame.image.load("Victory.png")
VICTORY = pygame.transform.scale(VICTORY, (1000, 600)).convert_alpha()
pygame.mixer.music.set_volume(0.7)
sound = pygame.mixer.Sound("fire.ogg")
sound_2 = pygame.mixer.Sound("enemy_burn.wav")
sound_3 = pygame.mixer.Sound("boss_burn.wav")
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play(-1)
blue_lst = []

print(7**6)

class Main:  # Створення класу
    def __init__(self, image_PATH, speed, x, y, a, b, HP):
        self.image_PATH = image_PATH
        self.speed = speed
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image_PATH), (a, b)).convert_alpha()
        self.square = self.image.get_rect(center=(self.x, self.y))
        self.HP = HP


hero = Main("rocket.png", [15, 0], 500, 450, 80, 140, 3)

bg = pygame.image.load("galaxy.jpg")  # Створюємо задній фон
bg_new = pygame.transform.scale(bg, (1000, 1800)).convert_alpha()
hp = pygame.image.load("HP.png")
health = pygame.transform.scale(hp, (75, 75)).convert_alpha()

score = 4
enemy_list = []


def enemy_load():
    global score
    if score == "BOSS":
        enemy_boss_1 = Main("ufo.png", [5, 0], 500, 100, 300, 150, 15)
        enemy_list.append(enemy_boss_1)
        return None
    elif score == "REAL BOSS":
        boss = Main("boss.png", [7.5, 0], 500, 100, 500, 250, 30)
        enemy_list.append(boss)
        return None
    while score > 0:
        a = random.randint(1, 3)
        if a == 1 and score > 0:
            enemy = Main("asteroid.png", [0.2, random.gauss(0.15, 0.03)], random.randint(50, 900), -50, 100, 100, 1)
            enemy_list.append(enemy)
            score -= 1
        elif a == 2 and score > 1:
            enemy_2 = Main("newenemy.png", [0.3, random.gauss(0.17, 0.02)], random.randint(50, 900), -50, 100, 150,3)
            enemy_list.append(enemy_2)
            score -= 2
        elif a == 3 and score > 2:
            enemy_3 = Main("elite_rocket.png", [1, random.gauss(0.2, 0.02)], random.randint(50, 900), -50, 100, 200, 5)
            enemy_list.append(enemy_3)
            score -= 3
            


enemy_load()


while True:  # Цикл гри
    hp_x = 10
    hp_y = 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # При натисканні хрестика закриваємо гру
            quit()
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            hero.x -= hero.speed[0]
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            hero.x += hero.speed[0]
        elif key[pygame.K_w]:
            bullet = Main("bullet.png", [0, 5], hero.x, hero.y - 50, 25, 25, None)
            P = True
            A = True
    scr.blit(bg_new, (0, bg_y))
    #if bg_y == -1200:
        #bg_change = -bg_change
    if bg_y == -600:
        bg_y = -1200
    scr.blit(hero.image, (hero.x, hero.y))
    bg_y += bg_change
    for i in range(hero.HP):
        scr.blit(health, (hp_x, hp_y))
        hp_x += 90
    for i in enemy_list:
        scr.blit(i.image, (i.x, i.y))
        if random.randint(1, 2) == 1:
            i.x += i.speed[0]
        else:
            i.x -= i.speed[0]
        if i.y >= 650:
            while True:
                scr.blit(G_O, (0, 0))
                pygame.display.update()
        i.y += i.speed[1]
        i.square = i.image.get_rect(center=(i.x, i.y))
        hero.square = hero.image.get_rect(center=(hero.x, hero.y))
        if random.randint(1, 3000) == 2 and (i.image_PATH == "newenemy.png" or i.image_PATH == "elite_rocket.png")  and B:
            enemy_bullet = Main("enemy_bullet.png", [0.2, 1.2], i.x, i.y, 25, 50, None)
            EB = True
            B = False
            O = True
        if random.randint(1, 1500) == 2 and i.image_PATH == "ufo.png" and B:
            fireball = Main("laser.png", [2, 1], i.x, i.y, 30, 30, None)
            FB = True
            B = False
            O = True
        if random.randint(1, 750) == 69 and i.image_PATH == "boss.png" and not BL:
            blue_laser = Main("blue_laser.png", [2, 1], i.x - 100, i.y, 50, 50, None)
            blue_lst.append(blue_laser)
            blue_laser = Main("blue_laser.png", [2, 1], i.x + 100, i.y, 50, 50, None)
            blue_lst.append(blue_laser)
            BL = True
            O = True
        if P:
            if bullet.square.colliderect(i.square) and A:
                i.HP -= 1
                bullet.y = -50
                F = True
                A = False
                pygame.mixer.Sound.play(sound)
                if i.HP <= 0:
                    enemy_list.remove(i)
        if EB:
            if enemy_bullet.square.colliderect(hero.square) and O:
                enemy_bullet.y = 620
                hero.HP -= 1
                F = True
                O = False
                pygame.mixer.Sound.play(sound_2)
                if hero.HP <= 0:
                    while True:
                        scr.blit(G_O, (0, 0))
                        pygame.display.update()
        if FB:
            if fireball.square.colliderect(hero.square) and O:
                fireball.y = 650
                hero.HP -= 3
                F = True
                O = False
                pygame.mixer.Sound.play(sound_2)
                if hero.HP <= 0:
                    while True:
                        scr.blit(G_O, (0, 0))
                        pygame.display.update()
        if BL:
            for i in blue_lst:
                if i.square.colliderect(hero.square) and O:
                    i.y = 650
                    hero.HP -= 1
                    enemy_list[0].HP += 3
                    pygame.mixer.Sound.play(sound_3)
                    O = False
                    if hero.HP <= 0:
                        while True:
                            scr.blit(G_O, (0, 0))
                            pygame.display.update()

    if P:
        scr.blit(bullet.image, (bullet.x, bullet.y))
        if bullet.y >= -20:
            bullet.y -= bullet.speed[1]
            bullet.square = bullet.image.get_rect(center=(bullet.x, bullet.y))
    if EB:
        scr.blit(enemy_bullet.image, (enemy_bullet.x, enemy_bullet.y))
        if enemy_bullet.y <= 620:
            enemy_bullet.y -= -enemy_bullet.speed[1]
            enemy_bullet.square = enemy_bullet.image.get_rect(center=(enemy_bullet.x, enemy_bullet.y))
        else:
            B = True
    if FB:
        scr.blit(fireball.image, (fireball.x, fireball.y))
        if fireball.y <= 620:
            fireball.y += fireball.speed[1]
            if random.randint(1, 2) == 1:
                fireball.x += fireball.speed[0]
            elif random.randint(1, 2) == 2:
                fireball.x -= fireball.speed[0]
            fireball.square = fireball.image.get_rect(center=(fireball.x, fireball.y))
        else:
            B = True
    if BL:
        for i in blue_lst:
            scr.blit(i.image, (i.x, i.y))
            if i.y <= 620:
                i.y += i.speed[1]
                if random.randint(1, 2) == 1:
                    i.x += i.speed[0]
                elif random.randint(1, 2) == 2:
                    i.x -= i.speed[0]
                i.square = i.image.get_rect(center=(i.x, i.y))
                if blue_lst[0].y > 620 and blue_lst[1].y > 620:
                    blue_lst = []
                    BL = False

    if len(enemy_list) == 0:
        if W == 0:
            score = 8
            enemy_load()
            W = 1
        elif W == 1:
            score = 10
            enemy_load()
            W = 2
        elif W == 2:
            score = 13
            enemy_load()
            W = 3
        elif W == 3:
            score = "BOSS"
            enemy_load()
            W = 4
        elif W == 4:
            score = 17
            enemy_load()
            W = 5
        elif W == 5:
            score = 20
            enemy_load()
            W = 6
        elif W == 6:
            score = "REAL BOSS"
            enemy_load()
            W = 7
        elif W == 7:
            while True:
                scr.blit(VICTORY, (0, 0))
                pygame.display.update()
    if hero.x >= 1000:
        hero.x = 920
    elif hero.x <= 0:
        hero.x = 1
    if i.image_PATH == "ufo.png":
        if random.randint(1, 3000) == 1:
            score = 5
            enemy_load()

    pygame.display.update()  # Оновлення вікна гри
