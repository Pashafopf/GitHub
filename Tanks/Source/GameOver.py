import pygame
from Source import GameData

########################
class GameOver(pygame.sprite.Sprite):
    """окно Game Over"""

   #конструктор класса
    def __init__(self):
        #инициализируем спрайт
        pygame.sprite.Sprite.__init__(self, self.containers)
        #заносим в спрайт картинку, подгруженную из главного класса
        self.image = self.images[0]
        # картинку помещаем в прямоугольник
        self.rect = self.image.get_rect()
        # этой переменной присваиваем список(координаты верхнего левого угла) параметров
        newpos = self.rect.move((100, 250))
        #прямоугольник вместе с картинкой помещаем в эту позицию
        self.rect = newpos
        self.count = 0
    #прорисовываем(апдэйтим) анимацию
    def update(self):
        self.image = self.images[int( GameData.animstep)]