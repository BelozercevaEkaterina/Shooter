from pygame import *
from random import randint
 
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
 
img_back = "back.jpeg" #фон игры
img_hero = "MF.png" #герой
img_lazer = "lazer.png" #пуля
img_enemy = "TF.png" #враг
 
score = 0 #сбито кораблей
lost = 0 #пропущено кораблей

 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        lazer = Lazer(img_lazer, self.rect.centerx, self.rect.top, 15, 20, -15)
        lazers.add(lazer)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Boss(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


class Lazer(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
win_width = 700
win_height = 500
display.set_caption("ShooterSW")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
player = Player(img_hero, 5, win_height - 100, 80, 100, 10)
enemies = sprite.Group()
for i in range(5):
   enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   enemies.add(enemy)
lazers = sprite.Group()

asteroids = sprite.Group()
for i in range(2):
   asteroid = Boss("DS.png", randint(80, win_width - 80), -40, 180, 180, randint(1, 5))
   asteroids.add(asteroid)


finish = False
run = True
 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    
    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
    
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
    
        player.update()
        enemies.update()
        lazers.update()

        asteroids.update()
    
        player.reset()
        enemies.draw(window)
        lazers.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(enemies, lazers, True, True)
        for c in collides:
            score += 1
            enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            enemies.add(enemy)

        if lost >= 3:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= 10:
            finish = True
            window.blit(win, (200,200)) 

        

        display.update()
    time.delay(50)
 
