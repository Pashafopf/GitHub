import pygame

########################
class Gear(pygame.sprite.Sprite):
    """индикатор скорости"""
    images = []
    #инициализация
    def __init__(self):
        #как объект спрайта
        pygame.sprite.Sprite.__init__(self, self.containers)
        #вначале на нейтрал
        self.image = self.images[2]
        #помещаем на экране влевый нижний угол
        self.rect = self.image.get_rect()
        newpos = self.rect.move((880, 640))
        self.rect = newpos

    #простой апдэйт
    def update(self):
        self.image = self.images[self.gear + 2]
