import pygame
import random
from Source import GameData

#######################
class Explosion(pygame.sprite.Sprite):
    #Взрыв танка!

    animcycle = 44
    images = []
    #инициализация
    def __init__(self, actor):

        #как спрайт
        pygame.sprite.Sprite.__init__(self, self.containers)

        #рандомно выбираем,какую анимацию сейчас показвать
        self.imageset = int(random.random()*3)
        if self.imageset == 0:
            self.image = self.images0[0]
        elif self.imageset == 1:
            self.image = self.images1[0]
        else:
            self.image = self.images2[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = 0

    #апдэйт = с каждым циклом анимации просто рисуем новую картинку из выбранной череды
    def update(self):
        self.life = self.life + 1
        if self.imageset == 0:
            self.image = self.images0[self.life]
        elif self.imageset == 1:
            self.image = self.images1[self.life]
        else:
            self.image = self.images2[self.life]
        if self.life == self.animcycle:

            #если переходим в другое состояние игры,то сразу стираем весь зрыв
            if (GameData.gamestate == "fighting") or (GameData.gamestate == "splash"):
                self.kill()
            else:
                self.life = 0
                self.imageset = int(random.random()*3)
