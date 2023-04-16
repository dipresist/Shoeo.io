from pygame import *
from random import randint
font.init()
mixer.init()

mw = display.set_mode((750, 680))
BG = transform.scale(image.load('galaxy.jpg'), (750, 680))
display.set_caption('Space Shooter')
clock = time.Clock()
mixer.music.load('space.ogg')
shoot = mixer.Sound('fire.ogg')
lost = 0
lost_txt = font.SysFont('Verdana', 20).render('Пропущено:' + str(lost), True, (200, 200, 200))

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, w, h, pic, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 700:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullets.add(Bullet(self.rect.centerx, self.rect.top, 30, 50, 'bullet.png', 15))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 670:
            global lost
            lost += 1
            self.kill()
            enemies.add(Enemy(randint(0, 700), 0, 70, 40, 'ufo.png', randint(3, 5)))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

hero = Player(300, 580, 50, 100, 'rocket.png', 10)
enemies = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    enemies.add(Enemy(randint(0, 700), 0, 70, 40, 'ufo.png', randint(3, 5)))

run = True
finish = False
#mixer.music.play()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
    if not finish:
        mw.blit(BG, (0, 0))
        enemies.draw(mw)
        enemies.update()
        hero.reset()
        hero.update()
        bullets.draw(mw)
        bullets.update()
        lost_txt = font.SysFont('Verdana', 20).render('Пропущено:' + str(lost), True, (200, 200, 200))
        mw.blit(lost_txt, (5, 5))
        if lost >= 10:
            finish = True
        sprite.groupcollide(bullets, enemies, True, True)
    display.update()
    clock.tick(60)
