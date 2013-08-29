import math
import pygame
from Source import GameData

######################
class Bullet(pygame.sprite.Sprite):
    #Цвет пули = цвету танка
    images = []
    #инициализируем
    def __init__(self,colour,x,y,angle):
        #как спрайт
        pygame.sprite.Sprite.__init__(self, self.containers)
        #цвет пули
        self.image = self.images[colour]
        #помещаем в прямоугольник и нужные координаты, переданные из танка
        self.rect = self.image.get_rect()
        newpos = self.rect.move((x, y))
        self.rect = newpos
        self.colour = colour
        self.angle = angle

    def update(self):
        # заставляем пулю лететь, с такой-то скоростью
        xoffset = math.cos(self.angle * math.pi / 180) * GameData.bulletspeed
        yoffset = - math.sin(self.angle * math.pi / 180) * GameData.bulletspeed
        newpos = self.rect.move((xoffset, yoffset))
        self.rect = newpos
        self.x = self.rect.left
        self.y = self.rect.top
