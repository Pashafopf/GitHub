import pygame
from Source import GameData
from Source import StringOption
from Source import NumericalOption

#########################
class Options(pygame.sprite.Sprite):
    images = []
    count = 0

    #Окно опций
    #инициализация
    def __init__(self):
        #как спрайт
        pygame.sprite.Sprite.__init__(self, self.containers)

        #картинку помещаем в нужное место в гланом окне

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        newpos = self.rect.move((60, 100))
        self.rect = newpos

    #простой апдэйт
    def update(self):
        self.image = Options.images[self.count]

