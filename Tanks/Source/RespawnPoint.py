import pygame
from Source import GameData

######################
class RespawnPoint(pygame.sprite.Sprite):
    """Место, откуда танк начинает движение,после того, как его убили"""
    
    images = []
    #инициализация
    def __init__(self, x, y, angle, visible = True):
        #как спрайт
        pygame.sprite.Sprite.__init__(self, self.containers)
        #картинка для спрайта-респауна
        self.image = self.images[0]
        #помещаем его в нужное место,
        self.rect = self.image.get_rect()
        newpos = self.rect.move((x, y))
        self.rect = newpos
        # под нужным углом
        self.angle = angle
        #и делаем видимым
        self.visible = visible
        center = self.rect.center
        rotate = pygame.transform.rotate
        self.original = self.image
        self.image = rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=center)
        self.x = self.rect.left
        self.y = self.rect.top
    #апдэйт
    def update(self):
        #если видимый
        if self.visible:
            #то, в соответствии с анимацией,меняя картинку
            self.image = self.images[ GameData.animstep ]
            #помещаем в нужное место, так получается анимированный респаун
            self.original = self.image
            center = self.rect.center
            rotate = pygame.transform.rotate
            self.original = self.image
            self.image = rotate(self.original, self.angle)
            self.rect = self.image.get_rect(center=center)
            self.x = self.rect.left
            self.y = self.rect.top
        else:
            self.image = GameData.transparant_sprite
            center = self.rect.center
            self.rect = self.image.get_rect(center=center)
            self.x = self.rect.left
            self.y = self.rect.top
