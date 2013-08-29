import pygame
from Source import GameData

#########################
class Logo(pygame.sprite.Sprite):
    """анимированный логотип игры"""
    #конструктор класса
    def __init__(self):
        #инициализируется объект спрайта
        pygame.sprite.Sprite.__init__(self, self.containers)
        #помещаем в переменную здесь image первую картинку из списка
        self.image = self.images[0]
        #Эту картинку помещаем в прямоугольник
        self.rect = self.image.get_rect()
        # переменной newpos присваиваем список(координаты верхнего левого угла) параметров
        newpos = self.rect.move((805, 10))
        #прямоугольник вместе с картинкой помещаем в эту позицию
        self.rect = newpos
    #прорисовываем(апдэйтим) анимацию
    def update(self):
        self.image = self.images[int(GameData.animstep/2)]

