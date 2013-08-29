import pygame
import math
import random
from Source import GameData
from Source import TankCopy
from Source import Score
from Source import Bullet

#################
class Tank(pygame.sprite.Sprite):
    """Посути сам танк. Танк игрока - красный."""
    #список подгруженных изображений(сделано в главном классе)
    images = []
    #количество циклов анимации
    animcycle = 6
    #инициализируем
    def __init__(self,colour,respawnpoint, algorithm, visible = True):
        #делаем спрайтом
        pygame.sprite.Sprite.__init__(self, self.containers)
        #подгружаем нужную картинку
        self.image = self.images[colour * 6]
        #помещаем в прямоугольник
        self.rect = self.image.get_rect()
        # в респаун на последнее поля боя с нужным углом
        x = GameData.battleground[GameData.battlegroundnr].respawnpoints[respawnpoint][0] + 6
        y = GameData.battleground[GameData.battlegroundnr].respawnpoints[respawnpoint][1] + 4
        angle = GameData.battleground[GameData.battlegroundnr].respawnpoints[respawnpoint][2]
        #ставим танк спомощью move((x, y))
        newpos = self.rect.move((x, y))
        self.rect = newpos
        #сохраняем здесь цвет, переданный этому танку-спрайту(может и синий,а может и красный)
        self.colour = colour
        #алгоритм
        self.algorithm = algorithm
        #делаем видимым
        self.visible = visible
        #его ориентация в 2D
        self.angle = angle
        #пока он стоит на месте = нулевая передача
        self.gear = 0
        #не стрелял
        self.bullets = 0
        #не умирал
        self.deaths = 0
        #не убивал
        self.kills = 0
        #вначале он отображается и на окне заставки(можно убрать)
        self.state = 0
        #заводим для него очередь команд
        self.command_queue = []
        #распологаем его правильно в респауне, по параметру self.angle ставим спиной к стене
        self.original = self.image
        center = self.rect.center
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=center)
        self.x = self.rect.left
        self.y = self.rect.top
        #передача и нагрев для танка
        self.gun_cooldown = GameData.bulletloadtime
        self.gear_cooldown = GameData.gearcooldown

        # отображение танка на панели очков
        #делаем копию танкатого же цвета
        self.icon_display = TankCopy(self.colour)
        #в пустом цикле
        if pygame.font:
            #отображаем число смертей и число убитых танков
            self.kills_display=Score("kills      : %d","orange",870,190 + self.colour * 75)
            self.deaths_display=Score("deaths : %d","red",870,222 + self.colour * 75)
        # создаём ботов в их респаунах в начале игры
        #если не красныйтанк
        if self.colour != GameData.red:
            #передаём очередь команд
            self.command_queue = []
            #и здесь самый простеший "искусственный интелект" говорящий,как выйти боту из респауна
            for i in range(0,20):
                #вверх
                self.command_queue.append("up")
                #стрельни
                self.command_queue.append("shoot")
            #стой
            self.command_queue.append("flush")

    #перемещение после гибели в респаун, с данными координатами и углом
    def move_to_respawn_point(self, respawnpoint):
        self.x=GameData.battleground[GameData.battlegroundnr].respawnpoints[respawnpoint][0] + 6
        self.y=GameData.battleground[GameData.battlegroundnr].respawnpoints[respawnpoint][1] + 4
        self.angle=GameData.battleground[GameData.battlegroundnr].respawnpoints[respawnpoint][2]
        self.rect.left = self.x
        self.rect.top = self.y        


    #огонь
    def shoot(self):
        #если можно стрелять
        if (self.bullets < GameData.maxbullets) and (self.gun_cooldown == 0):
            #огонь!
            Bullet(self.colour,self.rect.centerx-3,self.rect.centery-3,self.angle)
            #пуль на экране больше на одну
            self.bullets = self.bullets + 1
            #нагрев больше на один
            self.gun_cooldown = GameData.bulletloadtime
    #взрыв танка
    def explode(self):
        #к смерти + 1
        self.deaths += 1
        #передачу в ноль
        self.gear = 0
        #передаем оригинал танка
        self.original = self.image
        #вводим флаг
        flag = 0
        #рандом ставим в респаун
        respawnpoint = int(random.random()*6)
        while respawnpoint in GameData.respawnlist:
            respawnpoint = int(random.random()*6)
        while len(GameData.respawnlist) > 2:
            #поп - уточнить
            dummy = GameData.respawnlist.pop(0)
        #добавляем в листреспаунов нов точку
        GameData.respawnlist.append(respawnpoint)
        #и в эту новую точку танк и помещаем с углом и координатами,передадаём очередь комманд
        self.move_to_respawn_point(respawnpoint)
        self.angle=GameData.battleground[GameData.battlegroundnr].respawnpoints[respawnpoint][2]
        self.rect.left = self.x
        self.rect.top = self.y
        self.command_queue = []
                
    #увеличиваем передачу
    def gear_up(self):
        if (self.gear < 4) and (self.gear_cooldown == 0):
            self.gear = self.gear + 1
            self.gear_cooldown = GameData.gearcooldown

    #уменьшаем передачу
    def gear_down(self):
        if (self.gear > 0) and (self.gear_cooldown == 0):
            self.gear = self.gear - 1
            self.gear_cooldown = GameData.gearcooldown
        elif self.gear_cooldown == 0:
            self.gear = -2
            self.gear_cooldown = GameData.gearcooldown

    #резкий тормоз
    def halt(self):
        self.gear = 0

    #двигаем вправо
    def right(self):
        self.angle = self.angle - GameData.angle
        if self.angle < 0:
            self.angle = 360-GameData.angle
    #двигаем влево
    def left(self):
        self.angle = self.angle + GameData.angle
        if self.angle >= 360:
            self.angle = 0
    #команды в процессе игры
    def process_commands(self, respawn_points):
        #если команд больше 0
        if len(self.command_queue) > 0:
            #действие отправляй в пайпе
            action = self.command_queue.pop(0)
            #действие взрыв = новую очередь
            if action == "flush":
                self.command_queue = []
            #действие вверх = передачу вверх
            if action == "up":
                self.gear_up()
            #действие вниз = передачу вниз
            if action == "down":
                self.gear_down()
            #действие влево = двигай влево
            if action == "left":
                self.left()
            #действие вправо = двигай вправо
            if action == "right":
                self.right()
            #действие тормоз = тормози
            if action == "halt":
                self.halt()
            #действие огонь = огонь
            if action == "shoot":
                if len(pygame.sprite.spritecollide(self, respawn_points, 0)) == 0:
                    self.shoot()
            # танки могут стрелять во время движения
            elif (len(self.command_queue) > 0):
                if self.command_queue[0] == "shoot":
                    if len(pygame.sprite.spritecollide(self, respawn_points, 0)) == 0:
                        dummy = self.command_queue.pop(0)
                        self.shoot()
    #описываем движение танка
    def move(self):        
        # передаём "скорость" умножаем на передачу и спомощьютригонометрии гоним
        xoffset = math.cos(self.angle * math.pi / 180) * self.gear * GameData.tankspeed
        yoffset = - math.sin(self.angle * math.pi / 180) * self.gear * GameData.tankspeed
        # тормоз при ударе об стену
        #для всех стен
        for wall in GameData.battleground[GameData.battlegroundnr].walls:
            if wall.colliderect(self.rect):
                #удар об стену?
                if wall.collidepoint(self.rect.left, self.rect.top):
                    #тормози!
                    if xoffset < 0:
                        xoffset = 0
                    if yoffset < 0:
                        yoffset = 0
                #удар об стену?
                elif wall.collidepoint(self.rect.left, self.rect.bottom):
                    #тормози!
                    if xoffset < 0:
                        xoffset = 0
                    if yoffset > 0:
                        yoffset = -0
                #удар об стену?(в таком-то положении)
                elif wall.collidepoint(self.rect.right, self.rect.top):
                    #тормози!
                    if xoffset > 0:
                        xoffset = -0
                    if yoffset < 0:
                        yoffset = 0
                elif wall.collidepoint(self.rect.right, self.rect.bottom):
                    if xoffset > 0:
                        xoffset = -0
                    if yoffset > 0:
                        yoffset = -0
                elif wall.collidepoint(self.rect.centerx, self.rect.top):
                    if yoffset < 0:
                       yoffset = 0
                elif wall.collidepoint(self.rect.centerx, self.rect.bottom):
                    if yoffset > 0:
                        yoffset = -0
                elif wall.collidepoint(self.rect.left, self.rect.centery):
                    if xoffset < 0:
                        xoffset = 0
                elif wall.collidepoint(self.rect.right, self.rect.centery):
                    if xoffset > 0:
                        xoffset = -0
                else:
                    xoffset = 0
                    yoffset = 0
        # нельзя ездить по воде!(тоже,что и стены по сути)
        for pool in GameData.battleground[GameData.battlegroundnr].water:
            if pool.colliderect(self.rect):
                if pool.collidepoint(self.rect.left, self.rect.top):
                    if xoffset < 0:
                        xoffset = 0
                    if yoffset < 0:
                        yoffset = 0
                elif pool.collidepoint(self.rect.left, self.rect.bottom):
                    if xoffset < 0:
                        xoffset = 0
                    if yoffset > 0:
                        yoffset = -0
                elif pool.collidepoint(self.rect.right, self.rect.top):
                    if xoffset > 0:
                        xoffset = -0
                    if yoffset < 0:
                        yoffset = 0
                elif pool.collidepoint(self.rect.right, self.rect.bottom):
                    if xoffset > 0:
                        xoffset = -0
                    if yoffset > 0:
                        yoffset = -0
                elif pool.collidepoint(self.rect.centerx, self.rect.top):
                    if yoffset < 0:
                       yoffset = 0
                elif pool.collidepoint(self.rect.centerx, self.rect.bottom):
                    if yoffset > 0:
                        yoffset = -0
                elif pool.collidepoint(self.rect.left, self.rect.centery):
                    if xoffset < 0:
                        xoffset = 0
                elif pool.collidepoint(self.rect.right, self.rect.centery):
                    if xoffset > 0:
                        xoffset = -0
                else:
                    xoffset = 0
                    yoffset = 0
        # отбиваем танк при ударе об границу окна
        if  self.x < 3:
            if xoffset < 0:
                xoffset = 1
        if self.x > 759:
            if xoffset > 0:
                xoffset = -1
        if self.y < 3:
            if yoffset < 0:
                yoffset = 1
        if self.y > 724:
            if yoffset > 0:
                yoffset = -1
        # а теперь после всех запрещений об ударах об стену и воду меняем позицию танка в действительности!
        newpos = self.rect.move((xoffset, yoffset))
        self.rect = newpos
    #апдэйт
    def update(self):
        # апдэйте панели очков
        if pygame.font:
            #апдэйт смерте/убийств
            self.kills_display.set_score(self.kills)
            self.deaths_display.set_score(self.deaths)
        if self.visible:
            # теперь используем новую картинку танка
            self.image = self.images[(self.colour * 6) + GameData.animstep ]
            self.original = self.image
            # и вращаем её
            center = self.rect.center
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.angle)
            self.rect = self.image.get_rect(center=center)
            self.x = self.rect.left
            self.y = self.rect.top
        else:
            center = self.rect.center
            self.image = GameData.transparant_sprite
            self.rect = self.image.get_rect(center=center)
            self.x = self.rect.left
            self.y = self.rect.top
