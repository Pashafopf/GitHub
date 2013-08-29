import pygame
from Source import GameData


###############
class Thermometer(pygame.sprite.Sprite):
    """Максимальный нагрев пушки или макс. число пуль от одного танка,которое может быть на экране"""
    #список картинок для спрайта "Термометр"
    images = []
    #инициализируем
    def __init__(self):
        #это спрайт
        pygame.sprite.Sprite.__init__(self, self.containers)
        #самый холодный термометр (images[0]) помещаем, куда надо и всё
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        newpos = self.rect.move((825, 630))
        self.rect = newpos
        self.temperature = 0
    #апдэйтим
    def update(self):

        #в соответствии с формулой в скобках подгружаем нужную картинку термометра
        self.image = self.images[int(self.temperature * 5 / GameData.maxbullets)]
