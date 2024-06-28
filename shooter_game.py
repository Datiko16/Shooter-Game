#Создай собственный Шутер!
from time import time as timer
from pygame import *
from random import *



finish = False
lost = 0
score = 0
health = 3
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 50)




class GameSprite(sprite.Sprite):
    def __init__(self, player_image, width, height, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = -50
            self.speed = randint(2, 4)
            lost += 1


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))

background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
rocket = Player('rocket.png', 80, 100, 310, 400, 5)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', 80, 50, randint(80, 620), -50, randint(1, 3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', 80, 50, randint(80, 620), -50, randint(2, 4))
    asteroids.add(asteroid)

clock = time.Clock()

'''mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()'''

rel_time = False
num_fire = 0

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    rocket.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True



    collides = sprite.groupcollide(monsters, bullets, True, True)
    
    sprite.groupcollide(asteroids, bullets, False, True)

    if health == 3:
        color_health = (50, 205, 50)
    elif health == 2:
        color_health = (255, 127, 0)
    else:
        color_health = (255, 0, 0)

    if finish != True:
        text_lost = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_score = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        text_health = font2.render(str(health), 1, color_health)
        rocket.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        window.blit(background, (0, 0))
        window.blit(text_lost, (10, 50))
        window.blit(text_score, (10, 25))
        window.blit(text_health, (650, 25))
        rocket.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        if rel_time == True:
           now_time = timer() 
       
           if now_time - last_time < 3: 
               reload = font2.render('Wait, reload...', 1, (150, 0, 0))
               window.blit(reload, (260, 460))
           else:
               num_fire = 0  
               rel_time = False 

        for collide in collides:
            monster = Enemy('ufo.png', 80, 50, randint(80, 620), -50, randint(1, 3))
            monsters.add(monster)
            score += 1
        
        if score >= 10:
            text_win = font2.render('YOU WIN!', 1, (0, 255 , 50))
            window.blit(text_win, (300, 225))
            finish = True 

        if sprite.spritecollide(rocket, monsters, True) or sprite.spritecollide(rocket, asteroids, True):
            health -= 1
        
        if health == 0:
            text_lose = font2.render('YOU LOSE', 1, (255, 0, 0))
            window.blit(text_lose, (300, 225))                
            finish = True

    clock.tick(60)
    display.update()