import pygame
import random
from Source import GameData

#################
# Копия танка на дисплее в панели очков
class TankCopy(pygame.sprite.Sprite):
    #подгружаем картинки для спрайта "копия танка"
    images = []
    #инициализируем
    def __init__(self,colour):
        #делаем элементом спрайт
        pygame.sprite.Sprite.__init__(self, self.containers)
        #присваиваем картинку копии танчика=спрайту
        self.image = self.images[colour * 6]
        #помещаем в прямоугольник
        self.rect = self.image.get_rect()
        #помещаем туда танчик
        newpos = self.rect.move((815,200 + colour * 75))
        self.rect = newpos
        #заволим переменную цвета
        self.colour = colour
        #копию танка вначале под рандомным углом ставим
        self.angle = int(random.random()*360)
        self.direction = int(random.random()*2)
        if self.direction == 0:
            self.direction = -1
    #апдэйт копии танчика заключается,в его вращении
    def update(self):
        #увеличиваем значение угла в заданном дирекшене
        self.angle = self.angle + (int(GameData.angle / 2) * self.direction)
        #если значение угла больше 360,то зануляем
        if self.angle > 360:
            self.angle = 0

        self.image = self.images[(self.colour * 6) + GameData.animstep ]
        #создаём переменную original= копия image,
        self.original = self.image
        center = self.rect.center
        # и вращаем её transform.rotate на self.angle
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=center)
        #помещаем влево и верх прямоугольника
        self.x = self.rect.left
        self.y = self.rect.top
